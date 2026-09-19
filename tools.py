# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""Widget helpers: theme, factories, validation, cursor.

One job: helping to build widgets.
"""

import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk


class Tools:
    """Appearance and behaviour shared by every window."""

    # --- palette ------------------------------------------------------------
    # Meaning first, hue second: the names say what a colour is for, so a
    # change of taste does not turn into a search for '255, 160, 122'.
    BACKGROUND = (240, 240, 237)
    FOREGROUND = (0, 0, 0)
    WHITE = (255, 255, 255)
    MANDATORY = (0, 0, 255)
    EMPHASIS = (255, 0, 0)              # a field set apart from the others
    DISCARDED = (140, 140, 140)         # row taken out of the archive (enable 0)

    # The chrome: edges, troughs and hovers, the widget saying what it is and
    # whether it is under the pointer. They are the ones 'clam' would otherwise
    # pick for itself.
    BORDER = (169, 169, 165)            # the outline of anything with an edge
    TROUGH = (222, 222, 218)            # scrollbar channel
    HOVER = (228, 231, 235)             # under the pointer
    PRESSED = (205, 209, 214)           # while the mouse is down
    FOCUS = (58, 110, 165)              # where the keyboard is
    SELECTED = (51, 103, 158)           # the chosen row, the selected text
    UNAVAILABLE = (150, 150, 150)       # a control that is disabled

    # --- field widths -------------------------------------------------------
    # Named for what the field holds, in characters, which is what ttk asks
    # for. A width written once per form is a width decided once per form.
    FIELD_CODE = 16      # a thing with a shape: a code, a quantity, a price
    FIELD_NAME = 32      # a thing with a name: a product, a supplier, a person

    #: Every button in a button column is at least this wide. Negative, because
    #: ttk reads a negative width as a minimum: never narrower than eight
    #: characters, never wider than its own words.
    BUTTON_WIDTH = -8

    def __str__(self):
        return "class: {0}".format(self.__class__.__name__)

    # --- theme --------------------------------------------------------------

    def get_rgb(self, red, green, blue):
        """An (r, g, b) triple as the hex string tkinter expects."""
        return "#{0:02x}{1:02x}{2:02x}".format(red, green, blue)

    def set_style(self, theme):
        """Configure every style the application uses.

        Meant for 'clam': it exists on Windows and on Linux and looks the same
        on both, and it is the only built-in theme whose colours are settable
        at all - 'default' and 'alt' draw most of their edges themselves.
        """
        self.style = ttk.Style()

        if theme in self.style.theme_names():
            self.style.theme_use(theme)
        else:
            raise ValueError("unknown ttk theme: {0}".format(theme))

        background = self.get_rgb(*self.BACKGROUND)
        foreground = self.get_rgb(*self.FOREGROUND)
        white = self.get_rgb(*self.WHITE)
        border = self.get_rgb(*self.BORDER)
        trough = self.get_rgb(*self.TROUGH)
        hover = self.get_rgb(*self.HOVER)
        pressed = self.get_rgb(*self.PRESSED)
        focus = self.get_rgb(*self.FOCUS)
        selected = self.get_rgb(*self.SELECTED)
        unavailable = self.get_rgb(*self.UNAVAILABLE)

        # The row height comes from the font rather than from a number, so a
        # machine set to large text gets taller rows instead of clipped ones.
        base = font.nametofont("TkDefaultFont")
        row_height = base.metrics("linespace") + 8

        # The root style: a colour set here reaches widgets nobody thought to
        # name. lightcolor and darkcolor are clam's bevel; set to the
        # background they disappear and one line of bordercolor is left.
        self.style.configure(".",
                             background=background,
                             foreground=foreground,
                             fieldbackground=white,
                             bordercolor=border,
                             lightcolor=background,
                             darkcolor=background,
                             troughcolor=trough,
                             selectbackground=selected,
                             selectforeground=white,
                             font="TkDefaultFont")

        self.style.map(".", foreground=[("disabled", unavailable)])

        self.set_classic(self.style.master)

        self.style.configure("App.TFrame", background=background)
        self.style.configure("App.TLabel", padding=2, anchor=tk.W)

        # A button answers the pointer: without a map nothing on the screen
        # ever acknowledges the mouse.
        self.style.configure("App.TButton",
                             padding=(6, 5), anchor=tk.CENTER,
                             borderwidth=1, relief=tk.SOLID)
        self.style.map("App.TButton",
                       background=[("pressed", pressed),
                                   ("active", hover),
                                   ("disabled", background)],
                       bordercolor=[("pressed", focus),
                                    ("active", focus),
                                    ("focus", focus),
                                    ("disabled", border)],
                       lightcolor=[("pressed", pressed), ("active", hover)],
                       darkcolor=[("pressed", pressed), ("active", hover)])

        # The dotted rectangle inside a focused button says what the border
        # already says, now that the border changes colour.
        self.style.layout("App.TButton",
                          self.get_layout_without("App.TButton", "focus"))

        self.style.configure("App.TLabelframe",
                             relief=tk.SOLID, borderwidth=1, padding=8,
                             bordercolor=border,
                             lightcolor=background, darkcolor=background)
        self.style.configure("App.TLabelframe.Label",
                             background=background, padding=(2, 0))

        # On the base names, so every field gets them without asking. A named
        # style such as App.TEntry still inherits from these.
        self.style.configure("TEntry",
                             padding=(6, 4),
                             fieldbackground=white,
                             lightcolor=white, darkcolor=white,
                             insertcolor=foreground)
        self.style.map("TEntry",
                       bordercolor=[("focus", focus)],
                       lightcolor=[("focus", focus)],
                       darkcolor=[("focus", focus)],
                       fieldbackground=[("disabled", background),
                                        ("readonly", background)])

        self.style.configure("TCombobox",
                             padding=(6, 4),
                             arrowsize=13, arrowcolor=foreground,
                             lightcolor=white, darkcolor=white)
        # foreground is mapped here because clam maps it for this class and
        # its map replaces the root's: without it a focused readonly combo is
        # white on white, and a disabled one is black.
        self.style.map("TCombobox",
                       bordercolor=[("focus", focus)],
                       lightcolor=[("focus", focus)],
                       darkcolor=[("focus", focus)],
                       foreground=[("readonly", "focus", foreground),
                                   ("disabled", unavailable)],
                       fieldbackground=[("readonly", white),
                                        ("disabled", background)],
                       arrowcolor=[("disabled", unavailable)])

        self.style.configure("TSeparator", background=border)

        self.style.configure("App.TRadiobutton", padding=4)
        self.style.configure("App.TCheckbutton", padding=4)
        for name in ("App.TRadiobutton", "App.TCheckbutton"):
            self.style.configure(name,
                                 indicatorbackground=white,
                                 indicatorforeground=foreground,
                                 focuscolor=background)
            self.style.map(name,
                           background=[("active", background)],
                           indicatorbackground=[("pressed", hover),
                                                ("disabled", background)],
                           bordercolor=[("focus", focus)])

        self.style.configure("Mandatory.TEntry",
                             foreground=self.get_rgb(*self.MANDATORY))
        # The two fields of the product form that are set apart.
        self.style.configure("Product.TEntry",
                             foreground=self.get_rgb(*self.MANDATORY))
        self.style.configure("Package.TEntry",
                             foreground=self.get_rgb(*self.EMPHASIS))

        self.style.configure("TScrollbar",
                             troughcolor=trough, background=border,
                             bordercolor=trough, arrowcolor=foreground,
                             borderwidth=0, relief=tk.FLAT,
                             arrowsize=13, width=13)
        self.style.map("TScrollbar",
                       background=[("pressed", focus), ("active", pressed)])

        # The status bar carries colours only. Its relief is written where
        # the window builds it: `borderwidth=1, relief=tk.SUNKEN` on the frame.
        self.style.configure("StatusBar.TFrame",
                             bordercolor=background,
                             darkcolor=border, lightcolor=background)
        # The named font and not a size, so it grows with the rest.
        self.style.configure("StatusBar.TLabel",
                             padding=(6, 4), border=0, relief=tk.FLAT,
                             font="TkDefaultFont")

        # The name of the application, in the About window: the default
        # family, larger and bold, so it grows with the rest of the text.
        self.style.configure("Title.TLabel",
                             font=(base.cget("family"), base.cget("size") + 6, "bold"))
        # Something that opens when clicked: the colour of the keyboard focus,
        # underlined, the way a link has looked since the first browsers.
        self.style.configure("Link.TLabel",
                             foreground=focus,
                             font=(base.cget("family"), base.cget("size"), "underline"))

        # Tk 8.6.8 ignores tag colours in a Treeview
        # (bugs.python.org/issue36468, fixed in Tk 8.6.10): the map has to be
        # filtered or every row is drawn in the default colour.
        self.style.map("Treeview",
                       foreground=self.get_fixed_map("foreground"),
                       background=self.get_fixed_map("background"))

        # A few pixels of air make sixty rows a list instead of a block of text.
        self.style.configure("Treeview",
                             rowheight=row_height,
                             background=white, fieldbackground=white,
                             borderwidth=1, relief=tk.SOLID)

        # Not TkHeadingFont, which is bold: a heading is already told apart by
        # its background, its border and by not scrolling away.
        self.style.configure("Treeview.Heading",
                             background=background,
                             padding=(6, 5),
                             borderwidth=1, relief=tk.SOLID,
                             bordercolor=border,
                             font=(base.cget("family"), base.cget("size")))
        self.style.map("Treeview.Heading",
                       background=[("active", hover)],
                       relief=[("pressed", tk.SUNKEN)])

        # The dotted rectangle again, around the focused row, on top of the
        # tag colour that carries the meaning.
        self.style.layout("Item", self.get_layout_without("Item", "focus"))

    def set_classic(self, root):
        """Colour the widgets ttk cannot reach.

        A menu, a text, a listbox and the listbox a combobox drops are
        classic Tk widgets with no style engine behind them. They are set
        through the option database, Tk's own 'unless told otherwise': a
        widget built with an explicit colour keeps it.

        Only widgets created after this runs are affected, so it must run
        before any window exists.
        """
        if root is not None:
            background = self.get_rgb(*self.BACKGROUND)
            foreground = self.get_rgb(*self.FOREGROUND)
            white = self.get_rgb(*self.WHITE)
            selected = self.get_rgb(*self.SELECTED)
            unavailable = self.get_rgb(*self.UNAVAILABLE)

            for pattern, value in (
                    ("*Menu.background", background),
                    ("*Menu.foreground", foreground),
                    ("*Menu.activeBackground", selected),
                    ("*Menu.activeForeground", white),
                    ("*Menu.disabledForeground", unavailable),
                    ("*Menu.selectColor", foreground),
                    ("*Menu.activeBorderWidth", "0"),
                    ("*Menu.relief", "flat"),
                    ("*Menu.borderWidth", "1"),
                    ("*Text.background", white),
                    ("*Text.foreground", foreground),
                    ("*Text.selectBackground", selected),
                    ("*Text.selectForeground", white),
                    ("*Text.insertBackground", foreground),
                    ("*Text.highlightThickness", "0"),
                    ("*Text.borderWidth", "1"),
                    ("*Text.relief", "solid"),
                    ("*Listbox.background", white),
                    ("*Listbox.foreground", foreground),
                    ("*Listbox.selectBackground", selected),
                    ("*Listbox.selectForeground", white),
                    ("*Listbox.activeStyle", "none"),
                    ("*Listbox.highlightThickness", "0"),
                    ("*Listbox.borderWidth", "1"),
                    ("*Listbox.relief", "solid"),
                    # More specific than the line above, so it wins where the
                    # two disagree: a popdown draws its own border.
                    ("*TCombobox*Listbox.background", white),
                    ("*TCombobox*Listbox.foreground", foreground),
                    ("*TCombobox*Listbox.selectBackground", selected),
                    ("*TCombobox*Listbox.selectForeground", white),
                    ("*TCombobox*Listbox.borderWidth", "0")):
                root.option_add(pattern, value)

    def get_layout_without(self, style_name, element):
        """This style's layout with one element taken out of it.

        Removing a node means putting its children where it was: the focus
        ring wraps the padding that holds the label, so dropping the branch
        would drop the text as well. The layout is read from the theme, not
        copied here, so it cannot go stale when Tk changes.
        """
        def prune(layout):
            kept = []
            for name, options in layout:
                options = dict(options)
                children = options.get("children")
                if children:
                    options["children"] = prune(children)
                if name.split(".")[-1] == element:
                    kept.extend(options.get("children", []))
                else:
                    kept.append((name, options))
            return kept

        return prune(self.style.layout(style_name))

    def get_fixed_map(self, option):
        """Style map for `option` without the entries Tk 8.6.8 mishandles."""
        style = ttk.Style()
        return [element for element in style.map("Treeview", query_opt=option)
                if element[:2] != ("!disabled", "!selected")]

    # --- geometry -----------------------------------------------------------

    def hide_me(self, container):
        """Take a window off the screen while it is being built.

        The other half of center_me: a Toplevel is mapped the moment it is
        created, and without this it shows up empty in a corner, fills in and
        then jumps to the middle.
        """
        container.withdraw()

    def center_me(self, container, over=None):
        """Centre a window over the one that opened it, and show it.

        Over the parent by default, because that is where the eye is. The
        window is kept whole on the screen, title bar included.
        """
        container.update_idletasks()
        width = container.winfo_reqwidth()
        height = container.winfo_reqheight()

        parent = over
        if parent is None:
            parent = container.master
        if (parent is not None and parent.winfo_exists()
                and parent.winfo_width() > 1):
            x = parent.winfo_rootx() + (parent.winfo_width() - width) / 2
            y = parent.winfo_rooty() + (parent.winfo_height() - height) / 2
        else:
            x = (container.winfo_screenwidth() - width) / 2
            y = (container.winfo_screenheight() - height) / 2

        x = max(0, min(int(x), container.winfo_screenwidth() - width))
        y = max(0, min(int(y), container.winfo_screenheight() - height))
        container.geometry("+{0:d}+{1:d}".format(x, y))

        # On a window that was never hidden this does nothing.
        container.deiconify()

    # --- widget factories ---------------------------------------------------

    def get_tree(self, container, columns, show=None):
        """Build a Treeview with its scrollbar.

        columns is a sequence of six-part specifications:

            (identifier, heading, anchor, stretch, minwidth, width)

        The first one is always '#0', the implicit column, and it carries the
        row identifier rather than data.
        """
        for spec in columns:
            if len(spec) != 6:
                raise ValueError(
                    "column specification needs six parts "
                    "(identifier, heading, anchor, stretch, minwidth, width), "
                    "got {0!r}".format(spec))

        headers = [spec[1] for spec in columns][1:]

        if show is None:
            tree = ttk.Treeview(container)
        else:
            tree = ttk.Treeview(container, show=show)

        tree["columns"] = headers

        for identifier, heading, anchor, stretch, minwidth, width in columns:
            tree.heading(identifier, text=heading, anchor=anchor)
            tree.column(identifier, anchor=anchor, stretch=stretch,
                        minwidth=minwidth, width=width)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        scrollbar.configure(command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.set_tree_tags(tree)
        return tree

    def get_listbox(self, container):
        """Build a Listbox with its scrollbar, packed into container.

        exportselection=False keeps the selection when text is selected in
        another widget: without it, selecting a word in the dialog opened
        from the list clears the row the dialog is about.
        """
        listbox = tk.Listbox(container, exportselection=False)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return listbox

    def get_entry(self, container, variable, kind="text"):
        """Build an Entry for text, or for a number checked at every keystroke.

        kind is "text", "integer" or "float". A number field refuses the key
        that would not leave a number behind, so nothing else can be typed;
        it is narrower, and centred.
        """
        entry = ttk.Entry(container, textvariable=variable)

        if kind == "text":
            entry.configure(width=self.FIELD_NAME)
        elif kind == "integer":
            entry.configure(width=self.FIELD_CODE, justify=tk.CENTER, validate="key",
                            validatecommand=self.get_validate_integer(entry))
        elif kind == "float":
            entry.configure(width=self.FIELD_CODE, justify=tk.CENTER, validate="key",
                            validatecommand=self.get_validate_float(entry))
        else:
            raise ValueError("unknown kind of entry: {0}".format(kind))

        return entry

    def get_combo(self, container):
        """Build a readonly Combobox: a value is chosen from the list, never typed.

        One line, but the rule it carries lives here once: a combo that can
        be typed into accepts a supplier that does not exist, and every form
        then has to check for it.
        """
        return ttk.Combobox(container, style="App.TCombobox", state="readonly")

    def get_text(self, container):
        """Build a Text with its scrollbar, packed into container, for reading.

        Wrapped at word boundaries. It is filled with set_text, which leaves
        it disabled: shown, selectable, not editable.
        """
        text = tk.Text(container, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return text

    def set_text(self, text, content):
        """Put content in a Text built by get_text, and leave it read-only."""
        text.configure(state=tk.NORMAL)
        text.delete("1.0", tk.END)
        text.insert("1.0", content)
        text.configure(state=tk.DISABLED)

    def get_button_column(self, container, buttons, window=None):
        """A column of buttons, all the same width.

        buttons is a sequence of (label, command) in the order they appear;
        the closing one goes last. Each gets the first free letter of its
        label underlined and bound to Alt, so no button in a window is left
        without an accelerator and no two share one.

        window is what the bindings are made on, because the Toplevel and not
        the frame has the focus; it defaults to the container's own window.
        """
        column = ttk.Frame(container, style="App.TFrame")
        target = window
        if target is None:
            target = container.winfo_toplevel()
        taken = set()

        for label, command in buttons:
            underline = self.get_underline(label, taken)
            ttk.Button(column, style="App.TButton", text=label,
                       width=self.BUTTON_WIDTH,
                       underline=underline, command=command).pack(
                           fill=tk.X, padx=5, pady=5)
            if underline >= 0:
                letter = label[underline].lower()
                taken.add(letter)
                # A binding receives an event, a button command nothing: both
                # make the same call, so the keyboard and the mouse cannot
                # reach different handlers.
                target.bind("<Alt-{0}>".format(letter),
                            lambda evt, run=command: run())

        return column

    def get_underline(self, label, taken):
        """Which letter of this label to underline, or -1 for none.

        The first letter nobody in this window has claimed. Letters only: an
        underlined digit or dot is an accelerator nobody can guess.
        """
        found = -1
        for index, character in enumerate(label):
            if (found < 0 and character.isalpha()
                    and character.lower() not in taken):
                found = index
        return found

    def set_selected(self, tree, iid):
        """Put the focus back on a row, and scroll it into view.

        Called after a list has been read again, when the selection is lost.
        A row that is no longer there leaves the list as it is: landing on the
        wrong row is worse than landing on none, because the next thing
        pressed acts on it.
        """
        if iid and tree.exists(iid):
            tree.selection_set(iid)
            tree.focus(iid)
            tree.see(iid)
            tree.focus_set()

    # --- combo boxes and lists ----------------------------------------------

    def set_combo(self, combo, captions):
        """Fill a readonly combo box, and say nothing about what is chosen.

        The ids that go with the captions are the caller's to keep, in a
        dictionary of position to key: the box holds captions[i] and the
        caller holds ids[i]. Keyed by position and not by caption, because a
        caption can change meaning and a primary key cannot. A dictionary and
        not a list, because an empty box answers -1, which a list reads as
        the last row.
        """
        combo.configure(values=list(captions))

    def get_index(self, ids, value):
        """The position that stands for `value`, or -1 when it holds none."""
        found = -1
        for index, held in ids.items():
            if found < 0 and held == value:
                found = index
        return found

    def get_combo_id(self, combo, ids):
        """The id behind the chosen caption, or None when none is chosen."""
        return ids.get(combo.current())

    def set_combo_id(self, combo, ids, value):
        """Show the caption that stands for `value`, or nothing at all.

        A value the list does not hold empties the box rather than leaving
        what was in it, which would be read back as the record's own value.
        """
        index = self.get_index(ids, value)
        if index >= 0:
            combo.current(index)
        else:
            combo.set("")

    def set_list(self, listbox, captions, enabled=None):
        """Fill a listbox, and say nothing about what is selected.

        The same arrangement as the combo boxes: the caller keeps the ids by
        position. `enabled` is the rows' enable flags in the same order, and
        the disabled ones are drawn in grey, one item at a time, because a
        Listbox has no tags.
        """
        listbox.delete(0, tk.END)
        for index, caption in enumerate(captions):
            listbox.insert(tk.END, caption)
            if enabled is not None and not enabled[index]:
                listbox.itemconfigure(
                    index, foreground=self.get_rgb(*self.DISCARDED))

    def get_list_id(self, listbox, ids):
        """The id behind the selected line, or None when none is selected."""
        selection = listbox.curselection()
        found = None
        if selection:
            found = ids.get(selection[0])
        return found

    def set_list_id(self, listbox, ids, value):
        """Select the line that stands for `value`, or leave none selected."""
        listbox.selection_clear(0, tk.END)
        index = self.get_index(ids, value)
        if index >= 0:
            listbox.selection_set(index)
            listbox.activate(index)
            listbox.see(index)

    def set_count(self, variable, count):
        """How many rows the list is showing, said the same way everywhere."""
        variable.set("Items: {0}".format(count))

    def get_enable_tags(self, enable):
        """The tags of a row by whether it is enabled: grey when not."""
        tags = ()
        if not enable:
            tags = ("discarded",)
        return tags

    def set_tree_tags(self, tree):
        """The row colours, defined once for every list in the application."""
        # The foreground and not the background: a disabled row is not a
        # warning, it is a row that is no longer current.
        tree.tag_configure("discarded",
                           foreground=self.get_rgb(*self.DISCARDED))

    # --- input validation ---------------------------------------------------

    def get_widgets(self, container):
        """Every descendant of a container, depth first.

        Recursive, so a field does not escape validation merely because
        someone wrapped it in one more frame.
        """
        found = []
        for child in container.winfo_children():
            found.append(child)
            found.extend(self.get_widgets(child))
        return found

    def get_invalid_field(self, container):
        """First field that fails, as (widget, reason), or None if all pass.

        A field that is not on the form at the moment is skipped - see
        is_out_of_the_form.
        """
        invalid = None
        for widget in self.get_widgets(container):
            if (invalid is None
                    and isinstance(widget, (ttk.Entry, tk.Entry))
                    and not self.is_out_of_the_form(widget)):
                value = widget.get().strip()
                if not value:
                    invalid = (widget, "empty")
                elif (isinstance(widget, ttk.Combobox)
                      and value not in widget.cget("values")):
                    invalid = (widget, "not_in_list")
        return invalid

    def is_out_of_the_form(self, widget):
        """Whether a field is not asked of the user at the moment.

        Disabled, or removed from its geometry manager. READONLY does not
        count: it is how a combo box says 'choose, do not type', and it still
        has to be chosen. Asked of the manager and not of the screen, because
        every field of a window still withdrawn is not viewable.
        """
        if isinstance(widget, ttk.Widget):
            disabled = widget.instate(("disabled",))
        else:
            disabled = str(widget.cget("state")) == tk.DISABLED

        removed = widget.winfo_manager() == ""
        return disabled or removed

    def get_clean_text(self, value):
        """A typed value without the spaces a person does not see.

        Leading and trailing ones, and any run inside collapsed to one: a name
        typed with two spaces would pass a UNIQUE constraint as a new name.
        """
        text = ""
        if value:
            text = " ".join(value.split())
        return text

    def on_fields_control(self, container, title):
        """True when every field is filled and every choice is a legal one."""
        messages = {"empty": "Please fill in every field.",
                    "not_in_list": "Choose a value from the list."}
        invalid = self.get_invalid_field(container)
        is_valid = invalid is None

        if not is_valid:
            widget, reason = invalid
            messagebox.showwarning(title, messages[reason], parent=container)
            widget.focus()

        return is_valid

    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer),
                "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float),
                "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

    #: What a number looks like on the way to being one. A field that refused
    #: them would refuse the first keystroke of every negative number and of
    #: every value written .5
    INCOMPLETE_INTEGER = ("", "-", "+")
    INCOMPLETE_FLOAT = ("", "-", "+", ".", "-.", "+.")

    def validate_integer(self, action, index, value_if_allowed, prior_value,
                         text, validation_type, trigger_type, widget_name):
        """Allow the keystroke only when the field stays a valid integer."""
        allowed = True
        if action == "1" and value_if_allowed not in self.INCOMPLETE_INTEGER:
            try:
                int(value_if_allowed)
            except ValueError:
                allowed = False
        return allowed

    def validate_float(self, action, index, value_if_allowed, prior_value,
                       text, validation_type, trigger_type, widget_name):
        """Allow the keystroke only when the field stays a valid number.

        The comma is read as a decimal point rather than refused: it is the
        key the numeric keypad gives on an Italian keyboard.
        """
        allowed = True
        candidate = value_if_allowed.replace(",", ".")
        if action == "1" and candidate not in self.INCOMPLETE_FLOAT:
            try:
                float(candidate)
            except ValueError:
                allowed = False
        return allowed

    # --- cursor -------------------------------------------------------------

    BUSY_CURSOR = "watch"

    def busy(self, caller):
        """Anything slower than an eyeblink is wrapped in busy/not_busy.

        The cursor is set on the root and on everything inside the caller:
        set on one widget it shows over that widget alone, and the pointer is
        always over a button, the one just clicked.
        """
        for widget in self.get_busy_widgets(caller):
            widget.config(cursor=self.BUSY_CURSOR)
        caller.update()

    def not_busy(self, caller):
        for widget in self.get_busy_widgets(caller):
            widget.config(cursor="")
        caller.update()

    def get_busy_widgets(self, caller):
        """The caller, the root, and everything inside the caller."""
        widgets = [caller, caller.nametowidget(".")]
        widgets.extend(self.get_widgets(caller))
        return widgets


def main():
    foo = Tools()
    root = tk.Tk()
    root.title("Tools")
    foo.set_style("clam")

    frame = ttk.Frame(root, style="App.TFrame", padding=8)
    columns = (("#0", "id", tk.W, False, 0, 0),
               ("#1", "Product", tk.W, True, 160, 200),
               ("#2", "Stock", tk.CENTER, True, 60, 60),
               ("#3", "Price", tk.CENTER, True, 60, 60))
    tree = foo.get_tree(frame, columns)
    tree.insert("", tk.END, iid="1", text="1",
                values=("Chai", "39", "18.0"))
    tree.insert("", tk.END, iid="2", text="2",
                values=("Chang", "17", "19.0"), tags=foo.get_enable_tags(0))
    frame.pack(fill=tk.BOTH, expand=1)

    foo.center_me(root)
    root.mainloop()


if __name__ == "__main__":
    main()
