import unittest

from hyde.utils.validate import isEmail

class TestValidate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rightEmail(self):
        e = 'git@gmail.com'
        self.assertTrue(isEmail(e))

    def test_wrongEmail1(self):
        e = 'gmail.com'
        self.assertFalse(isEmail(e))

    def test_wrongEmail2(self):
        e = 'a'
        self.assertFalse(isEmail(e))

    def test_wrongEmail3(self):
        e = 'git@.com'
        self.assertFalse(isEmail(e))

    def test_wrongEmail4(self):
        e = 'git@a'
        self.assertFalse(isEmail(e))

    def test_wrongEmail5(self):
        e = '@a'
        self.assertFalse(isEmail(e))

    def test_wrongEmail6(self):
        e = '@'
        self.assertFalse(isEmail(e))

    def test_wrongEmail7(self):
        e = ''
        self.assertFalse(isEmail(e))
