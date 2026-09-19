# Tkinterlite — Architecture

How a small desktop application in Python, Tkinter and SQLite is put together, with the standard
library only. Tkinterlite started in 2017 as a study; this document describes it after the 2026
refactoring, and keeps the old design beside the new one, because the difference between the two
is the most useful thing the project has to teach.

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
| `tools.py`   | `Tools`  | widgets: styles, builders (tree, list, combo, text), helpers   |
| `events.py`  | `Events` | the Observer: who changed what, told to whoever shows it       |
| `log.py`     | `Log`    | the log file, rotated                                          |
| `config.py`  | `Config` | `tkinterlite.ini`                                              |
| `ui/*.py`    | `UI`     | one window each                                                |

`Log`, `Config` and `Events` are written by hand on purpose. The standard library has `logging`
and `configparser`, and their docstrings say so. This is a project for learning, and a
forty-line class shows what those modules do underneath.

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

## The Observer: how a save reaches every window

Before, a dialog that saved a category reloaded the list that had opened it, and selected a row by
its position. It knew too much about its parent, and it showed the old values after an Edit, because
it filled itself from a copy of the row kept by the list.

Now a save goes like this:

```
Category.save()
  ├─ db.get_update(...) / db.get_insert(...)   statement built from the schema
  ├─ db.write(sql, args)                        the row is written
  ├─ close the dialog
  └─ events.notify("categories", saved_id)
        ├─► Categories.on_changed(saved_id)    reload, land on the saved row
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
