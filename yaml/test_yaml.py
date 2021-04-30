import unittest 
from yaml_serializer import YamlSerializer

class TestYamlSerializer(unittest.TestCase):
    def test_dumps(self):
        obj = type('Example',(object,),{'five':5,'somedata':[123,321,222,111,333]})
        data = YamlSerializer().dumps(obj)
        res = 'type: "class"\nbody: \n  classname: "Example"\n  metaclasses: "(<class \'object\'>,)"\n  attributedict: \n    five: 5\n    somedata: \n      - 123\n      - 321\n      - 222\n      - 111\n      - 333'
        self.assertEqual(res,data)

    def test_dumps_instance(self):
        class Player:
            nickname = 'Player'
            team = 'Red'
            def about(self):
                return f"{self.nickname}#{self.team}"

        obj=Player()
        obj.nickname = 'FeedORfeed'
        obj.team = 'Green'

        YamlSerializer().dump(obj,open('player.yaml','w'))
        data = YamlSerializer().dumps(obj)
        res = YamlSerializer().loads(data)
        self.assertEqual(obj.nickname,res.nickname)
        self.assertEqual(obj.team,res.team)
        self.assertEqual(obj.about(),res.about())

    def test_loads(self):
        data = 'type: "class"\nbody: \n  classname: "Example"\n  metaclasses: "(<class \'object\'>,)"\n  attributedict: \n    five: 5\n    somedata: \n      - 123\n      - 321\n      - 222\n      - 111\n      - 333'
        obj = YamlSerializer().loads(data)
        self.assertEqual(obj.five,5)
        self.assertEqual(obj.somedata,[123,321,222,111,333])
    
    def test_load_func(self):
        obj = YamlSerializer().load(open('useglob.yml'))
        res = obj()
        from dump_test1 import pi
        self.assertEqual(res,pi)

    def test_load_class(self):
        obj = YamlSerializer().load(open('iitpclass.yml'))
        from dump_test1 import Iitp
        self.assertEqual(obj.Student.name,Iitp.Student.name)
        self.assertEqual(obj.Student.av_score,Iitp.Student.av_score)
        self.assertEqual(obj.expel.__code__,Iitp.expel.__code__)


if __name__ == '__main__':
    unittest.main()    