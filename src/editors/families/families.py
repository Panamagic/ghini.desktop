#
# families.py
#

import gtk

import editors
from tables import tables

class FamiliesEditor(editors.TreeViewEditorDialog):

    visible_columns_pref = "editor.families.columns"

    def __init__(self, parent=None, select=None, defaults={}):

        self.sqlobj = tables.Families

        self.column_data = editors.createColumnMetaFromTable(self.sqlobj)

        # set headers
        headers = {'family': 'Family',
                   'comments': 'Comments'}
        self.column_data.set_headers(headers)

        # set default visible
        self.column_data["family"].visible = True
        self.column_data["comments"].visible = True
        
        # set visible from stored prefs
        self.set_visible_columns_from_prefs(self.visible_columns_pref)
        
        editors.TreeViewEditorDialog.__init__(self, "Families Editor",
                                              select=select, defaults=defaults)