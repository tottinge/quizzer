import unittest

from cork import Cork


class MyTestCase(unittest.TestCase):
    def test_create_a_cork(self):
        cork = Cork(directory='./security')
        pass

if __name__ == '__main__':
    unittest.main()
