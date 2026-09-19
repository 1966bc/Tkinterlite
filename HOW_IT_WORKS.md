# Tkinterlite — How it works

[ARCHITECTURE.md](ARCHITECTURE.md) says how the program is built and why. This document follows
it while it runs: six things that happen, each traced through the code, file by file and method by
method. Open the files beside it and read along.

1. [Start](#1-start)
2. [One click on a product](#2-one-click-on-a-product)
3. [Edit a product and save it](#3-edit-a-product-and-save-it)
4. [Something goes wrong](#4-something-goes-wrong)
5. [One second of the clock](#5-one-second-of-the-clock)
6. [Exit](#6-exit)

## 1. Start

`python3 tkinterlite.py` runs the function `main()`, defined in **`tkinterlite.py`** itself and
called at its foot by `if __name__ == "__main__": main()` - the entry point, as `main()` is in C.
`main()` makes the log first, so that even a failure to start is written down, and then the
application, `App`:

```python
def main():
    log = Log(os.path.join(PROJECT_DIR, "tkinterlite.log"))
    try:
        app = App("Tkinterlite", log)
    except Exception as exc:
        log.exception("start failed: {0}".format(exc))
        messagebox.showerror("Tkinterlite", ...)
        raise
    app.mainloop()
```

`App` (**`ui/app.py`**) is the root window, a `tk.Tk`. It builds, in this order:

```python
self.engine = Engine(log)
self.engine.tools.set_style(self.engine.config.get("window", "theme"))
self.set_icon()
self.clock = Clock()
self.clock.start()
main = Main(self)
main.on_open()
```

**`Engine(log)`** (`engine.py`) builds its parts. None of them knows the others; Engine holds them:

```python
self.log = log
self.config = Config(self.get_file("tkinterlite.ini"))   # reads the .ini, line by line
self.db = DBMS(self.get_file("northwind.sl3"), log)       # opens the database
self.tools = Tools()                                      # styles and widget builders
self.events = Events()                                    # the Observer's register
self.windows = Windows()                                  # the open windows, one per name
```

- `Config.read` (`config.py`) goes through `tkinterlite.ini` and stops at the first line that is
  not a comment, a `[section]` or a `key = value`, naming it.
- `DBMS.set_connection` (`dbms.py`) connects and sets `row_factory = sqlite3.Row`, so that every row
  read from now on can be asked for a column by name.

**`Tools.set_style("clam")`** (`tools.py`) configures every ttk style the windows will ask for -
`App.TButton`, `App.TLabelframe`, `StatusBar.TLabel`... - and, through `set_classic`, the colours of
the menus, texts and listboxes, which ttk cannot reach.

**`Clock().start()`** (`clock.py`) starts a second thread. From now on it puts the time on a
queue once a second. See [5](#5-one-second-of-the-clock).

**`Main(self)`** (`ui/main.py`) builds the main window: menus, toolbar, status bar, the product
list (`Tools.get_tree`), the filter combo (`Tools.get_combo`), the buttons
(`Tools.get_button_column`, which also binds Alt-R, Alt-A, Alt-E, Alt-C). Then it asks to be told
about changes - this is the Observer:

```python
self.engine.events.subscribe("products", self.on_products_changed)
self.engine.events.subscribe("categories", self.on_combo_changed)
self.engine.events.subscribe("suppliers", self.on_combo_changed)
self.check_clock()
```

**`main.on_open()`** reads the products (`set_products`) and fills the combo (`set_combo_values`).

Last, **`app.mainloop()`**: Tkinter waits for events - a click, a key, a timer - and calls the
methods bound to them, one at a time, forever. Everything below happens inside this loop.

## 2. One click on a product

A click selects a row, and the Treeview fires the virtual event `<<TreeviewSelect>>`, which
`Main.init_ui` bound to `on_select`:

```python
self.lst_products.bind("<<TreeviewSelect>>", self.on_select)
```

`on_select` asks which row is selected. The row's Tk id *is* the product's primary key - it was
inserted with `iid=row["product_id"]` - so it goes straight into the query:

```python
row = self.engine.db.read(False, SELECTED, (int(selection[0]),))
text = "{0}: {1}, {2}".format(row["product"], row["company"], row["category"])
self.selected_text.set(text)
```

`SELECTED` joins products to suppliers and categories. `read(False, ...)` returns one row, read by
column name. `selected_text` is a `tk.StringVar`: the label in the status bar shows it, and changes
by itself when it is set.

## 3. Edit a product and save it

**Open.** A double click calls `Main.on_edit`, which opens the product dialog with the **id** of the
row - never a copy of it - through the register of open windows:

```python
product_id = int(selection[0])
self.engine.windows.replace("product", lambda: ui.product.UI(self, product_id))
```

`Windows.replace` (`windows.py`) closes the product dialog already open, if there is one, through
its own `on_cancel`; then it calls the `lambda`, which builds the new dialog, and calls its
`on_open`.

`ui/product.py` is a `Dialog` (`ui/dialog.py`). Its constructor builds the form: the subclass adds
its fields in `init_fields` (`Tools.get_entry` for text and numbers, `Tools.get_combo` for supplier
and category), the base class adds the Enable check box and the buttons. Then `Dialog.on_open`
reads the row from the database, now:

```python
row = self.get_row()          # SELECT * FROM products WHERE product_id = ?
self.set_values(row)          # the subclass fills its fields
self.enable.set(row["enable"])
```

**Save.** Save (or Alt-S) calls `Dialog.on_save`:

```python
if self.engine.tools.on_fields_control(self.frm_fields, ...):   # every field filled?
    if messagebox.askyesno(..., self.engine.ask_to_save, ...):   # sure?
        self.save()
```

`save` asks the subclass for its values - by name, `{"product": ..., "price": ...}` - and the
database layer for the statement:

```python
sql, args = self.engine.db.get_update(self.TABLE, self.row_id, values)
self.engine.db.write(sql, args)
```

`DBMS.get_update` (`dbms.py`) does not know the table's columns in advance: it asks SQLite,
with `PRAGMA table_info(products)`, which columns there are and which one is the primary key. It
puts the values in that order, refuses a column that is missing or unknown, and returns:

```
UPDATE products SET product = ?, supplier_id = ?, ... WHERE product_id = ?
```

`DBMS.write` runs it and commits. If it fails, it rolls back - see [4](#4-something-goes-wrong).

**Tell.** The dialog closes, and announces what it wrote:

```python
self.on_cancel()
self.engine.events.notify(self.TABLE, saved_id)       # "products", 1
```

`Events.notify` (`events.py`) calls every method that subscribed to `"products"`. Here that is
`Main.on_products_changed`, which reads the list again and lands on the product just saved:

```python
self.on_reset()
self.engine.tools.set_selected(self.lst_products, product_id)
```

Selecting the row fires `<<TreeviewSelect>>` again, and [2](#2-one-click-on-a-product) updates the
status bar. The dialog never touched the main window: it does not even know it exists. Saving a
category works the same way, and there *two* windows are told - the list of categories, which lands
on the row, and the main window, whose combo shows categories.

## 4. Something goes wrong

Say a query names a column that is not there, `SELECT stok FROM products`. In `DBMS.read`:

```python
except lite.Error:
    self.log.error("read failed: {0}".format(sql))
    raise
```

Only database errors are caught, and only to write down the statement - the one thing the traceback
will not show. Then the exception goes on up, through the method that called `read`, up to Tkinter,
which was running that method because of a click. Tkinter passes it to
`App.report_callback_exception` (`ui/app.py`), the one net for every callback:

```python
self.engine.log.exception("{0}: {1}".format(exc.__name__, val))
messagebox.showerror(self.title(), "{0}\n\nDetails in {1}".format(val, self.engine.log.path), ...)
```

`Log.exception` (`log.py`) writes the time, `ERROR`, the name of the method that called it (found
with `inspect.stack()`), the message and the whole traceback (`traceback.format_exc()`). The user
sees what went wrong, the application goes on, and `tkinterlite.log` holds two entries that complete
each other: the statement, then the traceback. Past 1 MB, `Log.rotate` moves the file aside to
`tkinterlite.log.1`, keeping three.

File > Log opens it - or says that it is empty, when nothing has gone wrong yet.

## 5. One second of the clock

Two threads are at work, and only one of them may touch a widget.

The **clock thread** (`Clock.run`, `clock.py`) never does:

```python
self.put_time()
while not self.stopping.wait(1.0):
    self.put_time()                 # puts "Astral date: ..." on a queue.Queue
```

The **main thread** - the one running `mainloop` - looks at the queue every 200 ms, in
`Main.check_clock` (`ui/main.py`):

```python
for message in self.parent.clock.drain():
    self.clock_text.set(message)
self.after(200, self.check_clock)
```

`after(200, ...)` does not wait: it asks Tk to call `check_clock` again in 200 ms and returns at
once, so the main loop goes back to answering clicks. The thread makes data, the queue carries it,
the main loop takes it.

## 6. Exit

Close, Alt-C, the toolbar's exit icon or the window's X all call `App.on_exit`:

```python
if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
    self.engine.db.con.close()
    self.clock.stop()          # sets the Event: the thread wakes and ends at once
    self.destroy()             # the root window goes, and mainloop returns
```

`mainloop()` returns in `main()`, `main()` returns, and the program ends.
