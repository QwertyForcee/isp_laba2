import re
import sys

def _dump_str(v):
    if sys.version_info < (3,) and hasattr(v, 'decode') and isinstance(v, str):
        v = v.decode('utf-8')
    v = "%r" % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or v.startswith('"'):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    v = v.split("\\x")
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        v[0] = v[0].replace("\\\\", "\\")
        # No, I don't know why != works and == breaks
        joinx = v[0][i] != "\\"
        while v[0][:i] and v[0][i] == "\\":
            joinx = not joinx
            i -= 1
        if joinx:
            joiner = "x"
        else:
            joiner = "u00"
        v = [v[0] + joiner + v[1]] + v[2:]
    return str('"' + v[0] + '"')

def _dump_float(v):
    return "{}".format(v).replace("e+0", "e+").replace("e-0", "e-")

class TomlEncoder:
    
    def __init__(self, _dict=dict, preserve=False):
        self._dict = _dict
        self.preserve = preserve
        self.dump_funcs = {
            str: _dump_str,
            list: self.dump_list,
            int: lambda v: v,
            float: _dump_float
        }    
    
    def dump_list(self, v):
        retval = "["
        for u in v:
            retval += " " + str(self.dump_value(u)) + ","
        retval += "]"
        return retval    

    def dump(self,obj,f):
        d = self.dumps(obj)
        f.write(d)
        return d

    def dumps(self,o, encoder=None):
        """Stringifies input dict as toml
        Args:
            o: Object to dump into toml
            encoder: The ``TomlEncoder`` to use for constructing the output string
        Returns:
            String containing the toml corresponding to dict
        """

        retval = ""
        if encoder is None:
            encoder = TomlEncoder(o.__class__)
        addtoretval, sections = self.dump_sections(o, "")
        retval += addtoretval
        outer_objs = [id(o)]
        while sections:
            section_ids = [id(section) for section in sections.values()]
            for outer_obj in outer_objs:
                if outer_obj in section_ids:
                    raise ValueError("Circular reference detected")
            outer_objs += section_ids
            newsections = encoder.get_empty_table()
            for section in sections:
                addtoretval, addtosections = encoder.dump_sections(
                    sections[section], section)

                if addtoretval or (not addtoretval and not addtosections):
                    if retval and retval[-2:] != "\n\n":
                        retval += "\n"
                    retval += "[" + section + "]\n"
                    if addtoretval:
                        retval += addtoretval
                for s in addtosections:
                    newsections[section + "." + s] = addtosections[s]
            sections = newsections
        return retval

    def get_empty_table(self):
        return self._dict()

    def _dump_str(v):
        if sys.version_info < (3,) and hasattr(v, 'decode') and isinstance(v, str):
            v = v.decode('utf-8')
        v = "%r" % v
        if v[0] == 'u':
            v = v[1:]
        singlequote = v.startswith("'")
        if singlequote or v.startswith('"'):
            v = v[1:-1]
        if singlequote:
            v = v.replace("\\'", "'")
            v = v.replace('"', '\\"')
        v = v.split("\\x")
        while len(v) > 1:
            i = -1
            if not v[0]:
                v = v[1:]
            v[0] = v[0].replace("\\\\", "\\")
            # No, I don't know why != works and == breaks
            joinx = v[0][i] != "\\"
            while v[0][:i] and v[0][i] == "\\":
                joinx = not joinx
                i -= 1
            if joinx:
                joiner = "x"
            else:
                joiner = "u00"
            v = [v[0] + joiner + v[1]] + v[2:]
        return str('"' + v[0] + '"')

    def dump_value(self, v):
        # Lookup function corresponding to v's type
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None and hasattr(v, '__iter__'):
            dump_fn = self.dump_funcs[list]
        # Evaluate function (if it exists) else return v
        return dump_fn(v) if dump_fn is not None else self.dump_funcs[str](v)

    def dump_sections(self, o, sup):
        retstr = ""
        if sup != "" and sup[-1] != ".":
            sup += '.'
        retdict = self._dict()
        arraystr = ""
        for section in o:
            section = str(section)
            qsection = section
            if not re.match(r'^[A-Za-z0-9_-]+$', section):
                qsection = _dump_str(section)
            if not isinstance(o[section], dict):
                arrayoftables = False
                if isinstance(o[section], list):
                    for a in o[section]:
                        if isinstance(a, dict):
                            arrayoftables = True
                if arrayoftables:
                    for a in o[section]:
                        arraytabstr = "\n"
                        arraystr += "[[" + sup + qsection + "]]\n"
                        s, d = self.dump_sections(a, sup + qsection)
                        if s:
                            if s[0] == "[":
                                arraytabstr += s
                            else:
                                arraystr += s
                        while d:
                            newd = self._dict()
                            for dsec in d:
                                s1, d1 = self.dump_sections(d[dsec], sup +
                                                            qsection + "." +
                                                            dsec)
                                if s1:
                                    arraytabstr += ("[" + sup + qsection +
                                                    "." + dsec + "]\n")
                                    arraytabstr += s1
                                for s1 in d1:
                                    newd[dsec + "." + s1] = d1[s1]
                            d = newd
                        arraystr += arraytabstr
                else:
                    if o[section] is not None:
                        retstr += (qsection + " = " +
                                   str(self.dump_value(o[section])) + '\n')
            elif self.preserve and isinstance(o[section], InlineTableDict):
                retstr += (qsection + " = " +
                           self.dump_inline_table(o[section]))
            else:
                retdict[qsection] = o[section]
        retstr += arraystr
        return (retstr, retdict)


class TomlDecoder:
    def get_empty_table(self):
        return dict()
        
    def _get_split_on_quotes(self, line):
        doublequotesplits = line.split('"')
        quoted = False
        quotesplits = []
        if len(doublequotesplits) > 1 and "'" in doublequotesplits[0]:
            singlequotesplits = doublequotesplits[0].split("'")
            doublequotesplits = doublequotesplits[1:]
            while len(singlequotesplits) % 2 == 0 and len(doublequotesplits):
                singlequotesplits[-1] += '"' + doublequotesplits[0]
                doublequotesplits = doublequotesplits[1:]
                if "'" in singlequotesplits[-1]:
                    singlequotesplits = (singlequotesplits[:-1] +
                                         singlequotesplits[-1].split("'"))
            quotesplits += singlequotesplits
        for doublequotesplit in doublequotesplits:
            if quoted:
                quotesplits.append(doublequotesplit)
            else:
                quotesplits += doublequotesplit.split("'")
                quoted = not quoted
        return quotesplits
    
    def bounded_string(self, s):
        if len(s) == 0:
            return True
        if s[-1] != s[0]:
            return False
        i = -2
        backslash = False
        while len(s) + i > 0:
            if s[i] == "\\":
                backslash = not backslash
                i -= 1
            else:
                break
        return not backslash

    def _load_array_isstrarray(self, a):
        a = a[1:-1].strip()
        if a != '' and (a[0] == '"' or a[0] == "'"):
            return True
        return False

    def load_array(self, a):
        atype = None
        retval = []
        a = a.strip()
        if '[' not in a[1:-1] or "" != a[1:-1].split('[')[0].strip():
            strarray = self._load_array_isstrarray(a)
            if not a[1:-1].strip().startswith('{'):
                a = a[1:-1].split(',')
            else:
                # a is an inline object, we must find the matching parenthesis
                # to define groups
                new_a = []
                start_group_index = 1
                end_group_index = 2
                open_bracket_count = 1 if a[start_group_index] == '{' else 0
                in_str = False
                while end_group_index < len(a[1:]):
                    if a[end_group_index] == '"' or a[end_group_index] == "'":
                        if in_str:
                            backslash_index = end_group_index - 1
                            while (backslash_index > -1 and
                                   a[backslash_index] == '\\'):
                                in_str = not in_str
                                backslash_index -= 1
                        in_str = not in_str
                    if not in_str and a[end_group_index] == '{':
                        open_bracket_count += 1
                    if in_str or a[end_group_index] != '}':
                        end_group_index += 1
                        continue
                    elif a[end_group_index] == '}' and open_bracket_count > 1:
                        open_bracket_count -= 1
                        end_group_index += 1
                        continue

                    # Increase end_group_index by 1 to get the closing bracket
                    end_group_index += 1

                    new_a.append(a[start_group_index:end_group_index])

                    # The next start index is at least after the closing
                    # bracket, a closing bracket can be followed by a comma
                    # since we are in an array.
                    start_group_index = end_group_index + 1
                    while (start_group_index < len(a[1:]) and
                           a[start_group_index] != '{'):
                        start_group_index += 1
                    end_group_index = start_group_index + 1
                a = new_a
            b = 0
            if strarray:
                while b < len(a) - 1:
                    ab = a[b].strip()
                    while (not self.bounded_string(ab) or
                           (len(ab) > 2 and
                            ab[0] == ab[1] == ab[2] and
                            ab[-2] != ab[0] and
                            ab[-3] != ab[0])):
                        a[b] = a[b] + ',' + a[b + 1]
                        ab = a[b].strip()
                        if b < len(a) - 2:
                            a = a[:b + 1] + a[b + 2:]
                        else:
                            a = a[:b + 1]
                    b += 1
        else:
            al = list(a[1:-1])
            a = []
            openarr = 0
            j = 0
            for i in range(len(al)):
                if al[i] == '[':
                    openarr += 1
                elif al[i] == ']':
                    openarr -= 1
                elif al[i] == ',' and not openarr:
                    a.append(''.join(al[j:i]))
                    j = i + 1
            a.append(''.join(al[j:]))
        for i in range(len(a)):
            a[i] = a[i].strip()
            if a[i] != '':
                nval, ntype = self.load_value(a[i])
                if atype:
                    if ntype != atype:
                        raise ValueError("Not a homogeneous array")
                else:
                    atype = ntype
                retval.append(nval)
        return retval
    

    def load_line(self, line, currentlevel, multikey, multibackslash):
        i = 1
        quotesplits = self._get_split_on_quotes(line)
        quoted = False
        for quotesplit in quotesplits:
            if not quoted and '=' in quotesplit:
                break
            i += quotesplit.count('=')
            quoted = not quoted
        pair = line.split('=', i)
        strictly_valid = _strictly_valid_num(pair[-1])
        if re.compile('([0-9])(_([0-9]))*').match(pair[-1]):
            pair[-1] = pair[-1].replace('_', '')
        while len(pair[-1]) and (pair[-1][0] != ' ' and pair[-1][0] != '\t' and
                                 pair[-1][0] != "'" and pair[-1][0] != '"' and
                                 pair[-1][0] != '[' and pair[-1][0] != '{' and
                                 pair[-1].strip() != 'true' and
                                 pair[-1].strip() != 'false'):
            try:
                float(pair[-1])
                break
            except ValueError:
                pass
            if re.compile(r"([0-9]{2}):([0-9]{2}):([0-9]{2})(\.([0-9]{3,6}))?").match(pair[-1]):
                break
            i += 1
            prev_val = pair[-1]
            pair = line.split('=', i)
            if prev_val == pair[-1]:
                raise ValueError("Invalid date or number")
            if strictly_valid:
                strictly_valid = _strictly_valid_num(pair[-1])
        pair = ['='.join(pair[:-1]).strip(), pair[-1].strip()]
        if '.' in pair[0]:
            if '"' in pair[0] or "'" in pair[0]:
                quotesplits = self._get_split_on_quotes(pair[0])
                quoted = False
                levels = []
                for quotesplit in quotesplits:
                    if quoted:
                        levels.append(quotesplit)
                    else:
                        levels += [level.strip() for level in
                                   quotesplit.split('.')]
                    quoted = not quoted
            else:
                levels = pair[0].split('.')
            while levels[-1] == "":
                levels = levels[:-1]
            for level in levels[:-1]:
                if level == "":
                    continue
                if level not in currentlevel:
                    currentlevel[level] = self.get_empty_table()
                currentlevel = currentlevel[level]
            pair[0] = levels[-1].strip()
        elif (pair[0][0] == '"' or pair[0][0] == "'") and \
                (pair[0][-1] == pair[0][0]):
            pair[0] = _unescape(pair[0][1:-1])
        k, koffset = self._load_line_multiline_str(pair[1])
        if k > -1:
            while k > -1 and pair[1][k + koffset] == '\\':
                multibackslash = not multibackslash
                k -= 1
            if multibackslash:
                multilinestr = pair[1][:-1]
            else:
                multilinestr = pair[1] + "\n"
            multikey = pair[0]
        else:
            value, vtype = self.load_value(pair[1], strictly_valid)
        try:
            currentlevel[pair[0]]
            raise ValueError("Duplicate keys!")
        except TypeError:
            raise ValueError("Duplicate keys!")
        except KeyError:
            if multikey:
                return multikey, multilinestr, multibackslash
            else:
                currentlevel[pair[0]] = value

    def _load_line_multiline_str(self, p):
        poffset = 0
        if len(p) < 3:
            return -1, poffset
        if p[0] == '[' and (p.strip()[-1] != ']' and
                            self._load_array_isstrarray(p)):
            newp = p[1:].strip().split(',')
            while len(newp) > 1 and newp[-1][0] != '"' and newp[-1][0] != "'":
                newp = newp[:-2] + [newp[-2] + ',' + newp[-1]]
            newp = newp[-1]
            poffset = len(p) - len(newp)
            p = newp
        if p[0] != '"' and p[0] != "'":
            return -1, poffset
        if p[1] != p[0] or p[2] != p[0]:
            return -1, poffset
        if len(p) > 5 and p[-1] == p[0] and p[-2] == p[0] and p[-3] == p[0]:
            return -1, poffset
        return len(p) - 1, poffset

    def load(self,f):
        data = f.read()
        return self.loads(data)

    def loads(self,s, _dict=dict):
        """Parses string as toml
        Args:
            s: String to be parsed
            _dict: (optional) Specifies the class of the returned toml dictionary
        Returns:
            Parsed toml file represented as a dictionary
        Raises:
            TypeError: When a non-string is passed
            TomlDecodeError: Error while decoding toml
        """

        implicitgroups = []
        retval = self.get_empty_table()
        currentlevel = retval
        if not isinstance(s, str):
            raise TypeError("Expecting a string")

        if not isinstance(s, str):
            s = s.decode('utf8')

        original = s
        sl = list(s)
        openarr = 0
        openstring = False
        openstrchar = ""
        multilinestr = False
        arrayoftables = False
        beginline = True
        keygroup = False
        dottedkey = False
        keyname = 0
        key = ''
        prev_key = ''
        line_no = 1

        for i, item in enumerate(sl):
            if item == '\r' and sl[i + 1] == '\n':
                sl[i] = ' '
                continue
            if keyname:
                key += item
                if openstring:
                    if item == openstrchar:
                        oddbackslash = False
                        k = 1
                        while i >= k and sl[i - k] == '\\':
                            oddbackslash = not oddbackslash
                            k += 1
                        if not oddbackslash:
                            keyname = 2
                            openstring = False
                            openstrchar = ""
                    continue
                elif keyname == 1:
                    if item.isspace():
                        keyname = 2
                        continue
                    elif item == '.':
                        dottedkey = True
                        continue
                    elif item.isalnum() or item == '_' or item == '-':
                        continue
                    elif (dottedkey and sl[i - 1] == '.' and
                        (item == '"' or item == "'")):
                        openstring = True
                        openstrchar = item
                        continue
                elif keyname == 2:
                    if item.isspace():
                        if dottedkey:
                            nextitem = sl[i + 1]
                            if not nextitem.isspace() and nextitem != '.':
                                keyname = 1
                        continue
                    if item == '.':
                        dottedkey = True
                        nextitem = sl[i + 1]
                        if not nextitem.isspace() and nextitem != '.':
                            keyname = 1
                        continue
                if item == '=':
                    keyname = 0
                    prev_key = key[:-1].rstrip()
                    key = ''
                    dottedkey = False

            if item == "'" and openstrchar != '"':
                k = 1
                try:
                    while sl[i - k] == "'":
                        k += 1
                        if k == 3:
                            break
                except IndexError:
                    pass
                if k == 3:
                    multilinestr = not multilinestr
                    openstring = multilinestr
                else:
                    openstring = not openstring
                if openstring:
                    openstrchar = "'"
                else:
                    openstrchar = ""
            if item == '"' and openstrchar != "'":
                oddbackslash = False
                k = 1
                tripquote = False
                try:
                    while sl[i - k] == '"':
                        k += 1
                        if k == 3:
                            tripquote = True
                            break
                    if k == 1 or (k == 3 and tripquote):
                        while sl[i - k] == '\\':
                            oddbackslash = not oddbackslash
                            k += 1
                except IndexError:
                    pass
                if not oddbackslash:
                    if tripquote:
                        multilinestr = not multilinestr
                        openstring = multilinestr
                    else:
                        openstring = not openstring
                if openstring:
                    openstrchar = '"'
                else:
                    openstrchar = ""
            if item == '#' and (not openstring and not keygroup and
                                not arrayoftables):
                j = i
                comment = ""
                try:
                    while sl[j] != '\n':
                        comment += s[j]
                        sl[j] = ' '
                        j += 1
                except IndexError:
                    break
                if not openarr:
                    self.preserve_comment(line_no, prev_key, comment, beginline)
            if item == '[' and (not openstring and not keygroup and
                                not arrayoftables):
                if beginline:
                    if len(sl) > i + 1 and sl[i + 1] == '[':
                        arrayoftables = True
                    else:
                        keygroup = True
                else:
                    openarr += 1
            if item == ']' and not openstring:
                if keygroup:
                    keygroup = False
                elif arrayoftables:
                    if sl[i - 1] == ']':
                        arrayoftables = False
                else:
                    openarr -= 1
            if item == '\n':
                if openstring or multilinestr:
                    if ((sl[i - 1] == "'" or sl[i - 1] == '"') and (
                            sl[i - 2] == sl[i - 1])):
                        sl[i] = sl[i - 1]
                        if sl[i - 3] == sl[i - 1]:
                            sl[i - 3] = ' '
                elif openarr:
                    sl[i] = ' '
                else:
                    beginline = True
                line_no += 1
            elif beginline and sl[i] != ' ' and sl[i] != '\t':
                beginline = False
                if not keygroup and not arrayoftables:
                    keyname = 1
                    key += item
        
        s = ''.join(sl)
        s = s.split('\n')
        multikey = None
        multilinestr = ""
        multibackslash = False
        pos = 0
        for idx, line in enumerate(s):
            if idx > 0:
                pos += len(s[idx - 1]) + 1


            if not multilinestr or multibackslash or '\n' not in multilinestr:
                line = line.strip()
            if line == "" and (not multikey or multibackslash):
                continue
            if multikey:
                if multibackslash:
                    multilinestr += line
                else:
                    multilinestr += line
                multibackslash = False
                closed = False
                if multilinestr[0] == '[':
                    closed = line[-1] == ']'
                elif len(line) > 2:
                    closed = (line[-1] == multilinestr[0] and
                            line[-2] == multilinestr[0] and
                            line[-3] == multilinestr[0])
                if closed:
                    value, vtype = self.load_value(multilinestr)
                    currentlevel[multikey] = value
                    multikey = None
                    multilinestr = ""
                else:
                    k = len(multilinestr) - 1
                    while k > -1 and multilinestr[k] == '\\':
                        multibackslash = not multibackslash
                        k -= 1
                    if multibackslash:
                        multilinestr = multilinestr[:-1]
                    else:
                        multilinestr += "\n"
                continue
            if line[0] == '[':
                arrayoftables = False
                if line[1] == '[':
                    arrayoftables = True
                    line = line[2:]
                    splitstr = ']]'
                else:
                    line = line[1:]
                    splitstr = ']'
                i = 1
                quotesplits = self._get_split_on_quotes(line)
                quoted = False
                for quotesplit in quotesplits:
                    if not quoted and splitstr in quotesplit:
                        break
                    i += quotesplit.count(splitstr)
                    quoted = not quoted
                line = line.split(splitstr, i)
                groups = splitstr.join(line[:-1]).split('.')
                i = 0
                while i < len(groups):
                    groups[i] = groups[i].strip()
                    if len(groups[i]) > 0 and (groups[i][0] == '"' or
                                            groups[i][0] == "'"):
                        groupstr = groups[i]
                        j = i + 1
                        while ((not groupstr[0] == groupstr[-1]) or
                            len(groupstr) == 1):
                            j += 1
                            if j > len(groups) + 2:
                                raise Exception
                            groupstr = '.'.join(groups[i:j]).strip()
                        groups[i] = groupstr[1:-1]
                        groups[i + 1:j] = []
                    else:
                        if not re.compile(r'^[A-Za-z0-9_-]+$').match(groups[i]):
                            raise Exception
                    i += 1
                currentlevel = retval
                for i in range(len(groups)):
                    group = groups[i]
                    try:
                        currentlevel[group]
                        if i == len(groups) - 1:
                            if group in implicitgroups:
                                implicitgroups.remove(group)
                            elif arrayoftables:
                                currentlevel[group].append(self.get_empty_table()
                                                        )
                            else:
                                raise Exception
                    except TypeError:
                        currentlevel = currentlevel[-1]
                        if group not in currentlevel:
                            currentlevel[group] = self.get_empty_table()
                            if i == len(groups) - 1 and arrayoftables:
                                currentlevel[group] = [self.get_empty_table()]
                    except KeyError:
                        if i != len(groups) - 1:
                            implicitgroups.append(group)
                        currentlevel[group] = self.get_empty_table()
                        if i == len(groups) - 1 and arrayoftables:
                            currentlevel[group] = [self.get_empty_table()]
                    currentlevel = currentlevel[group]
                    if arrayoftables:
                        try:
                            currentlevel = currentlevel[-1]
                        except KeyError:
                            pass
            elif line[0] == "{":
                self.load_inline_object(line, currentlevel, multikey,
                                        multibackslash)
            elif "=" in line:
                ret = self.load_line(line, currentlevel, multikey,
                                        multibackslash)
                if ret is not None:
                    multikey, multilinestr, multibackslash = ret
        return retval
    

    def load_value(self, v, strictly_valid=True):
        if not v:
            raise ValueError("Empty value is invalid")
        if v == 'true':
            return (True, "bool")
        elif v.lower() == 'true':
            raise ValueError("Only all lowercase booleans allowed")
        elif v == 'false':
            return (False, "bool")
        elif v.lower() == 'false':
            raise ValueError("Only all lowercase booleans allowed")
        elif v[0] == '"' or v[0] == "'":
            quotechar = v[0]
            testv = v[1:].split(quotechar)
            triplequote = False
            triplequotecount = 0
            if len(testv) > 1 and testv[0] == '' and testv[1] == '':
                testv = testv[2:]
                triplequote = True
            closed = False
            for tv in testv:
                if tv == '':
                    if triplequote:
                        triplequotecount += 1
                    else:
                        closed = True
                else:
                    oddbackslash = False
                    try:
                        i = -1
                        j = tv[i]
                        while j == '\\':
                            oddbackslash = not oddbackslash
                            i -= 1
                            j = tv[i]
                    except IndexError:
                        pass
                    if not oddbackslash:
                        if closed:
                            raise ValueError("Found tokens after a closed " +
                                             "string. Invalid TOML.")
                        else:
                            if not triplequote or triplequotecount > 1:
                                closed = True
                            else:
                                triplequotecount = 0
            if quotechar == '"':
                escapeseqs = v.split('\\')[1:]
                backslash = False
                for i in escapeseqs:
                    if i == '':
                        backslash = not backslash
                    else:
                        if i[0] not in ['0', 'b', 'f', 'n', 'r', 't', '"'] and (i[0] != 'u' and
                                                     i[0] != 'U' and
                                                     not backslash):
                            raise ValueError("Reserved escape sequence used")
                        if backslash:
                            backslash = False
                for prefix in ["\\u", "\\U"]:
                    if prefix in v:
                        hexbytes = v.split(prefix)
                        v = _load_unicode_escapes(hexbytes[0], hexbytes[1:],
                                                  prefix)
                v = _unescape(v)
            if len(v) > 1 and v[1] == quotechar and (len(v) < 3 or
                                                     v[1] == v[2]):
                v = v[2:-2]
            return (v[1:-1], "str")
        elif v[0] == '[':
            return (self.load_array(v), "array")
        elif v[0] == '{':
            inline_object = self.get_empty_inline_table()
            self.load_inline_object(v, inline_object)
            return (inline_object, "inline_object")
        else:
            itype = "int"
            neg = False
            if v[0] == '-':
                neg = True
                v = v[1:]
            elif v[0] == '+':
                v = v[1:]
            v = v.replace('_', '')
            lowerv = v.lower()
            if '.' in v or ('x' not in v and ('e' in v or 'E' in v)):
                if '.' in v and v.split('.', 1)[1] == '':
                    raise ValueError("This float is missing digits after "
                                     "the point")
                if v[0] not in '0123456789':
                    raise ValueError("This float doesn't have a leading "
                                     "digit")
                v = float(v)
                itype = "float"
            elif len(lowerv) == 3 and (lowerv == 'inf' or lowerv == 'nan'):
                v = float(v)
                itype = "float"
            if itype == "int":
                v = int(v, 0)
            if neg:
                return (0 - v, itype)
            return (v, itype)

def _strictly_valid_num(n):
    n = n.strip()
    if not n:
        return False
    if n[0] == '_':
        return False
    if n[-1] == '_':
        return False
    if "_." in n or "._" in n:
        return False
    if len(n) == 1:
        return True
    if n[0] == '0' and n[1] not in ['.', 'o', 'b', 'x']:
        return False
    if n[0] == '+' or n[0] == '-':
        n = n[1:]
        if len(n) > 1 and n[0] == '0' and n[1] != '.':
            return False
    if '__' in n:
        return False
    return True

def _unescape(v):
    """Unescape characters in a TOML string."""
    i = 0
    backslash = False
    while i < len(v):
        if backslash:
            backslash = False
            if v[i] in ['0', 'b', 'f', 'n', 'r', 't', '"']:
                v = v[:i - 1] + _escape_to_escapedchars[v[i]] + v[i + 1:]
            elif v[i] == '\\':
                v = v[:i - 1] + v[i:]
            elif v[i] == 'u' or v[i] == 'U':
                i += 1
            else:
                raise ValueError("Reserved escape sequence used")
            continue
        elif v[i] == '\\':
            backslash = True
        i += 1
    return v
    

from serializer import Serializer

class TomlSerializer(Serializer):
    encoder = TomlEncoder()
    decoder = TomlDecoder()

    def dump(self,obj,f):
        data = self.to_valid_dict(obj)
        self.encoder.dump(data,f)


    def dumps(self,obj):
        data = self.to_valid_dict(obj)
        return self.encoder.dumps(data)

    def load(self,f):
        obj = self.to_valid_obj(self.decoder.load(f))
        return obj

    def loads(self,data):
        obj =self.to_valid_obj( self.decoder.loads(data) )
        return obj

