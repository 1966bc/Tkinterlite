# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  Tkinterlite
# authors:  Giuseppe Costanzi (1966bc)
# licence:  GPL-3.0-or-later, see LICENSE
# -----------------------------------------------------------------------------
"""The list of categories. Everything but the names is in ui.list_window."""

import ui.category

from ui.list_window import ListWindow


class UI(ListWindow):
    TABLE = "categories"
    CAPTION = "category"
    DIALOG = ui.category.UI
