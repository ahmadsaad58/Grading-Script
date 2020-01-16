import unittest
from Sample import greet, bye

# Unit Test Class
class Test_Sample(unittest.TestCase):
    
    # Test the greet function
    def test_greet(self):
        self.assertEqual(greet("Saad"), "Hello, Saad!", "Should be \'Hello, Saad!\'")

    # Test the bye function
    def test_bye(self):
        self.assertEqual(bye(), "Good Bye!", "Should be \'Good Bye!\'")

if __name__ == '__main__':
    unittest.main()