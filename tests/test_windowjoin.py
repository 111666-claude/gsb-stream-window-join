import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windowjoin import core, samples


class WindowJoinTest(unittest.TestCase):
    def test_no_events(self):
        self.assertEqual(len(core.Joiner(10).feed(samples.ev(1, "a", "k", 1), core.Counter())), 0)

    def test_same_stream_no_join(self):
        joiner = core.Joiner(10)
        joiner.feed(samples.ev(1, "a", "k", 10), core.Counter())
        self.assertEqual(len(joiner.feed(samples.ev(2, "a", "k", 12), core.Counter())), 0)

    def test_basic_join(self):
        joiner = core.Joiner(10)
        joiner.feed(samples.ev(1, "a", "k", 10), core.Counter())
        self.assertEqual(len(joiner.feed(samples.ev(2, "b", "k", 15), core.Counter())), 1)

    def test_empty_key_join(self):
        joiner = core.Joiner(10)
        joiner.feed(samples.ev(1, "a", "x", 10), core.Counter())
        self.assertEqual(len(joiner.feed(samples.ev(2, "b", "x", 15), core.Counter())), 1)

    def test_window_stored(self):
        self.assertEqual(core.Joiner(7).window, 7)

    def test_counter_counts(self):
        joiner = core.Joiner(10)
        joiner.feed(samples.ev(1, "a", "k", 10), core.Counter())
        counter = core.Counter()
        joiner.feed(samples.ev(2, "b", "k", 12), counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
