from haiku import extract_haikus

import unittest

haiku1 = 'snow falls and is white the falling is a process the whiteness is not.'
haiku2 = "how many persons entered the duplication center yesterday? Gee I don't know!"
not_haiku1 = 'snow does not fall at all and is white the falling is a process the whiteness is not. Not at all.'
not_haiku2 = 'a process the whiteness is not.'
haiku_part1 = 'snow falls and is white.'
haiku_part2 = 'the falling is a process.'
haiku_part3 = 'the whiteness is not.'
haiku_con = "a contraction can't be skipped. it's not too hard to detect; it doesn't take much."

def concat(*args):
    return ' '.join(args)

class TestDetection(unittest.TestCase):

    def test_positive(self):
        self.assertEqual(len(extract_haikus(haiku1)), 1)
        self.assertEqual(len(extract_haikus(haiku2)), 1)

    def test_negative(self):
        self.assertEqual(len(extract_haikus(not_haiku1)), 0)
        self.assertEqual(len(extract_haikus(not_haiku2)), 0)

    def test_multiple(self):
        self.assertEqual(len(extract_haikus(concat(haiku1, haiku2))), 2)
        self.assertEqual(len(extract_haikus(concat(haiku1, haiku2, haiku1, haiku2))), 4)
        self.assertEqual(len(extract_haikus(concat(haiku1, not_haiku1))), 1)
        self.assertEqual(len(extract_haikus(concat(haiku1, not_haiku1, haiku2))), 2)
        self.assertEqual(len(extract_haikus(concat(not_haiku2, not_haiku1))), 0)
        self.assertEqual(len(extract_haikus(concat(not_haiku2, not_haiku1, not_haiku1, haiku2))), 1)

    def test_multipart(self):
        self.assertEqual(len(extract_haikus(concat(haiku_part1, haiku_part2))), 0)
        self.assertEqual(len(extract_haikus(concat(haiku_part1, haiku_part2, haiku_part3))), 1)
        self.assertEqual(len(extract_haikus(concat(haiku_part1, haiku_part2, haiku_part3, haiku2))), 2)

    def test_contraction(self):
        self.assertEqual(len(extract_haikus(concat(haiku_con))), 1)
        self.assertEqual(len(extract_haikus(concat(haiku_con, haiku_part2))), 1)

if __name__ == '__main__':
    unittest.main()
