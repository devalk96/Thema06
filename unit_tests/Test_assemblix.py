import unittest
import socket

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual('assemblix2019', socket.gethostname())

if __name__ == '__main__':
    unittest.main()
