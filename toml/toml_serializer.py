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
    


class TomlSerializer:
    encoder = TomlEncoder()

    def dump(self,obj,f):
        TomlEncoder().dump(obj,f)
    

    def dumps(self,obj):
        return self.encoder.dumps(obj)
        

