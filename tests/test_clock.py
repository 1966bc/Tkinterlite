# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for clock.py: the thread, the queue and stopping, without a window."""

import unittest

from clock import Clock


class TestClock(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()

    def tearDown(self):
        # Only a started thread can be joined: some tests never start it.
        self.clock.stop()
        if self.clock.is_alive():
            self.clock.join(timeout=2)

    def test_first_message_comes_at_once(self):
        self.clock.start()
        # get() waits for it: the test does not guess how long a thread takes.
        message = self.clock.queue.get(timeout=2)
        self.assertTrue(message.startswith("Astral date: "))

    def test_drain_takes_everything_and_never_waits(self):
        self.clock.queue.put("one")
        self.clock.queue.put("two")
        self.assertEqual(self.clock.drain(), ["one", "two"])
        self.assertEqual(self.clock.drain(), [])

    def test_stop_ends_the_thread_at_once(self):
        self.clock.start()
        self.clock.stop()
        # Well under the one-second tick: the Event wakes the thread.
        self.clock.join(timeout=0.5)
        self.assertFalse(self.clock.is_alive())

    def test_it_is_a_daemon(self):
        self.assertTrue(self.clock.daemon)


if __name__ == "__main__":
    unittest.main()
