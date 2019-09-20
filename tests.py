from haiku import extract_haikus

import unittest

haiku1 = 'snow falls and is white the falling is a process the whiteness is not.'
haiku2 = "how many persons entered the duplication center yesterday? Gee I don't know!"
not_haiku1 = 'snow does not fall at all and is white the falling is a process the whiteness is not. Not at all.'
not_haiku2 = 'a process the whiteness is not.'

class TestDetection(unittest.TestCase):

    def test_positive(self):
        self.assertEqual(len(extract_haikus(haiku1)), 1)
        self.assertEqual(len(extract_haikus(haiku2)), 1)

    def test_negative(self):
        self.assertEqual(len(extract_haikus(not_haiku1)), 0)
        self.assertEqual(len(extract_haikus(not_haiku2)), 0)

if __name__ == '__main__':
    unittest.main()
