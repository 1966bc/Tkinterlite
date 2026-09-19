# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Tests for events.py: the Observer, without any window."""

import unittest

from events import Events


class QuietLog:
    """Stands in for Log: the trace is off, so trace() says nothing."""

    def trace(self, message):
        pass


class Listener:
    """Stands in for a window: it remembers what it was told."""

    def __init__(self):
        self.told = []

    def on_changed(self, row_id):
        self.told.append(row_id)


class TestEvents(unittest.TestCase):

    def setUp(self):
        self.events = Events(QuietLog())
        self.listener = Listener()

    def test_subscriber_is_told_the_row(self):
        self.events.subscribe("categories", self.listener.on_changed)
        self.events.notify("categories", 7)
        self.assertEqual(self.listener.told, [7])

    def test_only_the_event_subscribed_to(self):
        self.events.subscribe("categories", self.listener.on_changed)
        self.events.notify("suppliers", 3)
        self.assertEqual(self.listener.told, [])

    def test_every_subscriber_is_told(self):
        other = Listener()
        self.events.subscribe("products", self.listener.on_changed)
        self.events.subscribe("products", other.on_changed)
        self.events.notify("products", 1)
        self.assertEqual((self.listener.told, other.told), ([1], [1]))

    def test_subscribing_twice_tells_once(self):
        self.events.subscribe("products", self.listener.on_changed)
        self.events.subscribe("products", self.listener.on_changed)
        self.events.notify("products", 1)
        self.assertEqual(self.listener.told, [1])

    def test_unsubscribed_is_not_told(self):
        self.events.subscribe("products", self.listener.on_changed)
        self.events.unsubscribe("products", self.listener.on_changed)
        self.events.notify("products", 1)
        self.assertEqual(self.listener.told, [])

    def test_no_row_after_a_delete(self):
        self.events.subscribe("products", self.listener.on_changed)
        self.events.notify("products")
        self.assertEqual(self.listener.told, [None])

    def test_unknown_event_is_refused(self):
        with self.assertRaises(ValueError):
            self.events.subscribe("customers", self.listener.on_changed)
        with self.assertRaises(ValueError):
            self.events.notify("categoris", 1)


if __name__ == "__main__":
    unittest.main()
