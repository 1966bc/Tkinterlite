# Tkinterlite — Conventions

The rules this code is written by.

## Rules

- **English in the code**: identifiers, comments, docstrings, UI text.
- **PEP 8**: 4 spaces, lines up to 100 columns, `lower_case_with_underscores` for functions and
  variables, `CapWords` for classes, `UPPER_CASE` for module constants.
- **Object-oriented**: the logic lives in classes, one responsibility each.
- **Böhm–Jacopini**: only sequence, `if`, loops and assignments. One exit per function: no
  `return` in the middle, no `break`/`continue`. A function that needs several exits is doing
  several things and must be split. `raise` is allowed, for real errors only.
- **One thing per line**: a plain `if`/`else`, never `x if condition else y`.
- **KISS and YAGNI**: the simplest solution that still reads clearly in two years; nothing
  written for an imagined future.
- **Least surprise**: a name promises what the code does, no more. A `get_*` returns and writes
  nothing, no hidden side effects. Windows that do similar things behave the same way.
- **Fail fast, fail safe, never silently**: on error stop near the cause and leave the database
  consistent (rollback). A failed read must not look like "no rows".
- **By hand where it teaches**: where a library is not really needed, a small class written by
  hand shows what it does underneath (`Log`, `Config`, `Events`), and its docstring names the
  library it stands in for.

## Style

- File header block with `project: Tkinterlite`, `authors: Giuseppe Costanzi (1966bc)`,
  `licence: GPL-3.0-or-later, see LICENSE`. No modification date: git keeps it per file. The
  release date, Latin season + Roman year (e.g. `hiems MMXXI`), lives once, in `__date__` next
  to `__version__` in `ui/main.py`.
- Widget prefixes (Hungarian notation?): `lst_`, `cb_`, `txt_`, `lbl_`, `frm_`, `btn_`, `ent_`, `chk_`.
- Widgets used often are built by `Tools`: `get_tree`, `get_listbox`, `get_combo` (readonly),
  `get_entry` (text, integer, float), `get_text`. Buttons come from `get_button_column`, given
  `(label, command)` pairs: it underlines the first free letter and binds it to Alt.
- A list window is a `ui.base.ListWindow`, a one-row form is a `ui.base.Dialog`.
- ttk styles (`App.*`, `StatusBar.TLabel`, ...) are all defined in `Tools.set_style()`.
- `.format()` strings.
- Confirmations through `messagebox`, with the texts held by the engine (`ask_to_save`,
  `ask_to_delete`, `abort`, `no_selected`).
