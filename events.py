# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The Observer pattern, written by hand.

Whoever changes something says so, and whoever shows it is told. The two do
not know each other: a dialog that saves a category does not know that the
main window has a combo box of categories, and it does not need to. It says
"categories changed", and every window that asked to be told redraws itself.

    events.subscribe("categories", self.on_categories)   # when a window opens
    events.notify("categories", category_id)             # when a row is saved
    events.unsubscribe("categories", self.on_categories) # when it closes
"""


class Events:
    """Who wants to be told, for each event, and the telling."""

    #: The events that exist, one per table a window shows. A name not in
    #: this list is a typo, and it is refused where it is written rather
    #: than being an event nobody ever hears.
    NAMES = ("products", "categories", "suppliers")

    def __init__(self, log):
        #: The log, for the trace (--trace).
        self.log = log
        #: event name -> the callbacks to call, in the order they asked
        self.subscribers = {}

    def __str__(self):
        return "class: {0}\nevents: {1}".format(self.__class__.__name__, ", ".join(self.NAMES))

    def subscribe(self, event, callback):
        """Ask to be told. A window does this when it opens."""
        self.check(event)
        callbacks = self.subscribers.setdefault(event, [])
        if callback not in callbacks:
            callbacks.append(callback)
        self.log.trace("{0}: {1}".format(event, self.get_names(callbacks)))

    def unsubscribe(self, event, callback):
        """Stop being told. A window that forgets this is told after it is gone."""
        self.check(event)
        callbacks = self.subscribers.get(event, [])
        if callback in callbacks:
            callbacks.remove(callback)
        self.log.trace("{0}: {1}".format(event, self.get_names(callbacks)))

    def notify(self, event, row_id=None):
        """Tell everyone who asked that this event happened.

        row_id is the row that was written, so that a list can land on it;
        None when there is no such row, after a delete. The callbacks are
        called on a copy of the list, because one of them may unsubscribe
        while it is being told.
        """
        self.check(event)
        callbacks = list(self.subscribers.get(event, []))
        self.log.trace("{0}, row_id={1} -> {2}".format(event, row_id, self.get_names(callbacks)))
        for callback in callbacks:
            callback(row_id)

    def get_names(self, callbacks):
        """The callbacks as the trace shows them: module.method."""
        return ["{0}.{1}".format(callback.__self__.__class__.__module__, callback.__name__)
                for callback in callbacks]

    def check(self, event):
        """Refuse an event that is not in NAMES."""
        if event not in self.NAMES:
            raise ValueError("unknown event: {0}; the events are {1}".format(event,
                                                                             ", ".join(self.NAMES)))
