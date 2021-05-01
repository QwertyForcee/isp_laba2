import unittest
from json_serializer import JsonSerializer

class TestJsonSerializer(unittest.TestCase):
    def test_func(self):
        def reverse(s):
            return s[::-1]
            data = JsonSerializer().dumps(test_func)
            obj = JsonSerializer().loads(data)
            self.assertEqual(obj("12345"),test_func("12345"))
            self.assertEqual(obj("1"),test_func("1"))

if __name__ == '__main__':
    unittest.main()