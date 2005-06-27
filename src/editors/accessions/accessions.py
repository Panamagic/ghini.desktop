#
# accessions.py
#

import gtk

import editors
from tables import tables
import utils

#
# TODO: rather than having an accessions editor and a clones editor
# we should be able to just add clones to and accession in the same editor
# though it may take some custom code, maybe we could attach a children
# editor to any editor based on the clones name and just specify which editor
# would be the child and pop it up
#
class AccessionsEditor(editors.TableEditorDialog):

    visible_columns_pref = "editor.accessions.columns"

    def __init__(self, parent=None, select=None, defaults={}):

        self.sqlobj = tables.Accessions
        
        self.column_data = editors.createColumnMetaFromTable(self.sqlobj) #returns None?

        # set headers
        headers = {"acc_id": "Acc ID",
                   "plantname": "Name",
                   "prov_type": "Provenance Type",
                   "wild_prov_status": "Wild Provenance Status",
                   "ver_level": "Verification Level",           
                   "ver_name": "Verifier's Name",
                   "ver_date": "Verification Date",
                   "ver_lit": "Verification Literature"#,
#                   "wgs": "World Geographical Scheme"
                   }
        self.column_data.set_headers(headers)

        # set default visible
        self.column_data["acc_id"].visible = True 
        self.column_data["plantname"].visible = True
    
        # set visible according to stored prefs
        self.set_visible_columns_from_prefs(self.visible_columns_pref)
            
        editors.TableEditorDialog.__init__(self, "Accessions Editor", select=select,
                                           defaults=defaults)
        

    def get_completions(self, text, colname):
        # get entry and determine from what has been input which
        # field is currently being edited and give completion
        # if this return None then the entry will never search for completions
        # TODO: finish this
        parts = text.split(" ")
        genus = parts[0]
        results = []
        model = None
        maxlen = 0
        if colname == "plantname": #and len(genus) > 2:            
            model = gtk.ListStore(str, int)
            if len(genus) > 2:
                sr = tables.Genera.select("genus LIKE '"+genus+"%'")
                # this is a foreign key so store the the string and id
                model = gtk.ListStore(str, int) 
                for row in sr:
                    for p in row.plantnames:
                        s = str(p)
                        #print s + ": " + str(p.id)
                        if len(s) > maxlen: maxlen = len(s)
                        model.append([s, p.id])
        return model, maxlen
    
        # split the text by spaces
        # if the last item is longer than say 3 then
        #    get completions 
    
    def commit_changes(self):
        if not editors.TableEditorDialog.commit_changes(self):
            return
            
        # need to ask if you want to 
        msg  = "No Plants/Clones exist for this accession %s. Would you like " \
        "to add them now?"
        #values = self.get_table_values(not self.dummy_row)
        values = self.get_table_values()
        for v in values:
            acc_id = v["acc_id"]
            sel = tables.Accessions.selectBy(acc_id=acc_id)
            accession = sel[0]
            if sel.count() > 1:
                raise Exception("AccessionEditor.commit_changes():  "\
                                "more than one accession exists with id: " + acc_id)
            
            if not utils.yes_no_dialog(msg % acc_id):
                continue
            e = editors.editors.Plants(defaults={"accession":sel[0]})    
            e.show()
        return True
    