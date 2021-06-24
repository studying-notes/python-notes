import unittest
import random


class SequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def runTest(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)


class DictValueFormatFunction(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_shuffle(self):
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, list(range(10)))
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))


if __name__ == '__main__':
    unittest.main()
