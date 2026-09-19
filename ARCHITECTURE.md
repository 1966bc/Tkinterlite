# Tkinterlite — Architecture

How a small desktop application in Python, Tkinter and SQLite is put together, with the standard
library only. Tkinterlite started in 2017 as a study; this document describes it after the 2026
refactoring, and keeps the old design beside the new one, because the difference between the two
is the most useful thing the project has to teach. To follow the program while it runs, method
by method, read [HOW_IT_WORKS.md](HOW_IT_WORKS.md).

## The big picture

```
                  App (tk.Tk)
                   │ creates one
                   ▼
                Engine ──────────────────────────────┐
     ┌─────────┬────┴────┬──────────┬──────────┐     │
     ▼         ▼         ▼          ▼          ▼     │ handed down:
    log      config      db       tools      events  │ self.engine = parent.engine
   (Log)   (Config)   (DBMS)    (Tools)    (Events)  │
                                                     ▼
                              Main ──► Categories ──► Category
                                   ──► Suppliers  ──► Supplier
                                   ──► Product
```

| module       | class    | one job                                                        |
|--------------|----------|----------------------------------------------------------------|
| `engine.py`  | `Engine` | owns the parts below; paths, icons, messages                   |
| `dbms.py`    | `DBMS`   | SQLite: read, write, statements built from the schema          |
| `tools.py`   | `Tools`  | widgets: styles, builders (tree, list, combo, entry, text)     |
| `events.py`  | `Events` | the Observer: who changed what, told to whoever shows it       |
| `windows.py` | `Windows` | one open window per name: the Singleton pattern, by name      |
| `log.py`     | `Log`    | the log file, rotated                                          |
| `config.py`  | `Config` | `tkinterlite.ini`                                              |
| `clock.py`   | `Clock`  | a thread that feeds the status bar through a queue             |
| `ui/list_window.py`, `ui/dialog.py` | `ListWindow`, `Dialog` | what every list, every form share |
| `ui/app.py`  | `App`    | the root window: engine, clock, the error net, version and date |
| `ui/main.py` | `Main`   | the main window: the products                                  |
| `ui/*.py`    | `UI`     | one window each, saying only what is its own                   |

`Log`, `Config`, `Events` and `Windows` are written by hand on purpose. The standard library
has `logging` and `configparser`, and their docstrings say so. This is a project for learning,
and a forty-line class shows what those modules do underneath.

## From a mixin to composition

### Before: Engine *was* everything

```python
class Engine(DBMS, Tools, Clock):
    def __init__(self):
        super().__init__()
```

With multiple inheritance, Engine *was* a database, *was* a box of widget helpers and *was* a
clock, all at once. Every method of the three classes landed in one object, and every window
reached it from the root of the widget tree:

```python
self.nametowidget(".").engine.read(True, sql, ())
self.nametowidget(".").engine.center_me(self)
```

It worked. What it cost:

- **Nobody could tell who did the work.** `engine.read` and `engine.center_me` sit side by side,
  and finding where `read` lives means opening three files.
- **The MRO was a trap.** Python looks methods up in the order
  `Engine → DBMS → Tools → Clock → Thread`. `super().__init__()` reached `DBMS.__init__`, which
  did not call `super()` in turn, so `Clock.__init__` and `Thread.__init__` never ran. Engine was
  a `Thread` left half built: `engine.start()` raises
  `RuntimeError: thread.__init__() not called`. The real clock was a second object, made by
  `get_clock()`.
- **The dependencies were hidden.** `DBMS.read` called `self.on_log(...)`, which `DBMS` does not
  have: it was in Engine, and it worked only because at run time `self` happened to be an Engine.
  `DBMS` could not be used, or tested, on its own.
- **It could only grow.** Whatever was new went into Engine. This is what is called a God Object.

### After: Engine *has* its parts

```python
class Engine:
    def __init__(self, log):
        self.log = log
        self.config = Config(self.get_file("tkinterlite.ini"))
        self.db = DBMS(self.get_file("northwind.sl3"), log)
        self.tools = Tools()
        self.events = Events()
        self.windows = Windows()
```

```python
self.engine.db.read(True, sql, ())
self.engine.tools.center_me(self)
```

- **The call says who works.** `self.engine.db.read` reads like a sentence.
- **No MRO.** Each part is built by its own `__init__`, completely.
- **Dependencies are written down.** `DBMS(database, log)` says in its constructor that it needs
  a log; nothing arrives from nowhere.
- **Each part is tested alone.** `DBMS` on a database in memory, `Events` without a window,
  `Config` on a temporary file (`tests/`).
- **Engine stays thin.** It coordinates, and keeps only what is its own.

The rule to take away: inherit only when *is a* is true said aloud. `Main` *is a* `ttk.Frame`,
so it inherits from it. Engine *is a* database? No, it *has* one. That is why the usual advice is
*favour composition over inheritance*.

Windows do not look Engine up any more either: each one receives it from the window that opens it,
`self.engine = parent.engine`.

## Inheritance where it belongs: `ListWindow` and `Dialog`

Composition did not banish inheritance: it put it where *is a* is true. The lists of categories
and suppliers were the same window written twice, and so were their dialogs. Now they are one
`ListWindow` and one `Dialog`, and each module says only what is its own:

```python
class UI(ListWindow):                  class UI(Dialog):
    TABLE = "categories"                   NAME = "category"
    CAPTION = "category"                   TABLE = "categories"
    DIALOG = ui.category.UI
                                           def init_fields(self): ...
                                           def set_values(self, row): ...
                                           def get_values(self): ...
```

A list of categories *is a* list window; a category form *is a* dialog. The base classes do the
rest once: the enable check box, reading the row by id, saving, telling the other windows, the
buttons and their Alt keys. Each class adds a single parent to the chain, and each `__init__`
calls the one above it: the line of inheritance is straight, with nothing left half built.

## The Observer: how a save reaches every window

Before, a dialog that saved a category reloaded the list that had opened it, and selected a row by
its position. It knew too much about its parent, and it showed the old values after an Edit, because
it filled itself from a copy of the row kept by the list.

Now a save goes like this:

```
Dialog.save()                                  in ui/dialog.py, for every dialog
  ├─ db.get_update(...) / db.get_insert(...)   statement built from the schema
  ├─ db.write(sql, args)                        the row is written
  ├─ close the dialog
  └─ events.notify("categories", saved_id)
        ├─► ListWindow.on_changed(saved_id)    reload, land on the saved row
        └─► Main.on_combo_changed(saved_id)    reload the combo
```

The dialog does not know who is listening. The main window does not know who saved. A new window
that shows categories subscribes when it opens and unsubscribes when it closes, and nothing else
changes:

```python
self.engine.events.subscribe("categories", self.on_changed)    # __init__
self.engine.events.unsubscribe("categories", self.on_changed)  # on_cancel
```

A dialog receives the **id** of its row, never a copy, and reads the row itself when it opens:
what it shows is what is in the database.

## One window per name: `windows.py`

Tk gives each window a path from its name, `.categories`. Building a second window with the same
name used to replace the first behind its back: the first never ran its `on_cancel`, so it stayed
subscribed to the Observer, and a half-filled dialog was thrown away without a word.

`Windows` is a register of the open windows, one per name - a dictionary of instances,
`dict_instances`, name → window: the Singleton pattern applied to a name rather than to a class.
Every window is opened through it, with one of two rules:

```python
self.engine.windows.show("categories", lambda: ui.categories.UI(self))       # lists, About
self.engine.windows.replace("product", lambda: ui.product.UI(self, product_id))  # dialogs
```

`show` brings an open window to the front and builds one only when there is none. `replace`
closes the open dialog through its own `on_cancel`, which tidies up after itself, and builds a new
one: a dialog is about one row. The window is passed as a function that builds it, so that nothing
is built when the answer is "it is already open". The register forgets a window on its
`<Destroy>`, however it was closed.

Python allows a Singleton written in `__new__`, which runs before `__init__` and can return the
instance already made. It works, but Python then calls `__init__` again on the old window, and
every subclass must remember to skip it. The register does the same in plain sight.

## Data: by name, from the schema

- Rows are read **by column name**: the connection uses `sqlite3.Row`, so `row["stock"]` and not
  `row[6]`, which changes meaning the day a column is added.
- A dialog gives its values **by name**, `{"company": ..., "enable": ...}`. `DBMS.get_insert` and
  `get_update` put them in the order the table declares, which they ask of the schema with
  `PRAGMA table_info`. A missing or unknown column is refused with the table's name.
- The primary key is the column the schema marks as key, not the first one.

## Errors: they rise, and are caught once

Before, `DBMS.read` caught every exception with a bare `except:`, wrote it to a log and returned
`None`. The error became "no data" and came back later, somewhere else, as a `TypeError`.

Now:

- `DBMS.read` and `write` catch only `sqlite3.Error`, write the statement to the log, roll back a
  write, and `raise` again.
- File readers have no `try` at all: a missing file raises with its path.
- There is one net, at the top: `App.report_callback_exception`, which Tkinter calls for an
  exception in any callback. It writes the traceback to `tkinterlite.log` and shows the message.
  Before the main loop starts, `main()` guards the start the same way.

## The clock: a thread, done right

Tkinter is single-threaded: only the thread running the main loop may touch a widget. A second
thread that calls `label.config(...)` itself works on one machine and freezes on another, which
is why threads in Tkinter are argued about so much. The clock in the status bar shows the pattern
that works (`clock.py`):

```
  clock thread                       main loop (the only one touching widgets)
  ────────────                       ─────────────────────────────────────────
  Clock.run()                        Main.check_clock(), every 200 ms via after()
    put the time ──► queue.Queue ──►   drain it, write the status bar
    wait 1 s on an Event               ask again with after(200, ...)
```

The thread makes data, the queue carries it, the main loop takes it. The thread never touches a
widget, and the main loop never waits for the thread. The thread is a `daemon`, and stops through
a `threading.Event`, which wakes it at once instead of letting it sleep out its second.

For a clock alone, `after(1000, ...)` would do; the thread is there to show the pattern for work
that really blocks, such as reading a slow device or watching a folder. The first version of this
clock had the right idea and paid for it: the queue was read with `after(1, ...)`, a thousand
times a second, and every refresh of the main window started one more such loop.

## Configuration

`tkinterlite.ini`, read by `Config` line by line: `[sections]`, `key = value`, comments. Any
other line stops the program at start, naming the file and the line number.

## Tests

```
python3 -m unittest discover -s tests -v
```

`unittest`, standard library. The tests use a database in memory and temporary files: the real
`northwind.sl3` is never touched. Where a part needs a collaborator, the test passes a small
stand-in (`MemoryLog`, a `Listener`), which composition makes possible: it is only an argument.
