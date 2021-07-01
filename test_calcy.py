import unittest
from unittest import result
from calcy import Calcy

class cal_test(unittest.TestCase):
    
    def setUp(self):
        """ Executed before every test case """
        self.cal = Calcy()

    def test_add(self):
        result = self.cal.sum(5, 6)
        self.assertEqual(result, 11)
    
    def test_sub(self):
        result = self.cal.sub(5, 1)
        self.assertEqual(result, 4)
    
    def test_mul(self):
        result = self.cal.mul(2, 3)
        self.assertEqual(result, 6)

# Execute all the tests when the file is executed
if __name__ == "__main__":
    unittest.main()