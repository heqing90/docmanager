import PySimpleGUI as sg
from model import Document, File, Person
from datetime import datetime as dt
from create_doc_ui import CreateDocUI
from create_file_ui import CreateFileUI

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'



# person = Person(0, "测试","男","000000000000000000", dt.now(), dt.now())

# def gen_files(did):
#     return [File(x, did, "档案文件_{}".format(x), "C:\\Folder\File_{}.pdf".format(x)) for x in range(3)]

# docs = [Document(x, "档案_{}".format(x), 0, gen_files(x)) for x in range(3)]

class DocDetailUI:

    def __init__(self, person, service):
        self.person = person
        self.service = service
        self.doc_tree_data = sg.TreeData()
        self.docs = service.get_doc_by_pid(self.person.id)
        for doc in self.docs:
            self.add_doc('', doc)    
        right_click_menu_def = ['&Right', ['添加档案', '添加文件', '打开文档', '!删除']]
        self.layout = [
            [sg.Text("姓名", size=(12, 1) ), sg.InputText(default_text=person.name, disabled=True)],
            [sg.Text("性别", size=(12, 1)), sg.InputText(default_text=person.sex, disabled=True)],
            [sg.Text("身份证", size=(12, 1)), sg.InputText(default_text=person.id_card, disabled=True)],
            [sg.Tree(data=self.doc_tree_data,
                headings=['文件类型', ],
                auto_size_columns=False,
                num_rows=20,
                col0_width=80,
                key='-TREE-',
                show_expanded=False,
                right_click_menu=right_click_menu_def,
                enable_events=True),
            ]
        ]
        self.window = sg.Window("档案详情", layout=self.layout)

    def add_doc(self, parent, doc):
        self.doc_tree_data.Insert(parent, doc.name, doc.name, values=[], icon=folder_icon) 
        for f in doc.files:
            self.doc_tree_data.Insert(doc.name, f.name, f.path, values=[f.path.split('.')[-1]], icon=file_icon)

    def find_doc_by_name(self, name):
        if not name:
            return None
        for doc in self.docs:
            print(doc)
            if doc.name == name:
                return doc
        return None
            
    def show(self):
        window = self.window
        while True:
            event, values = window.read()
            print(event, values)
            if not event:
                break
            win = None
            if event == "添加档案":
                win = CreateDocUI(self.person, self.service) 
            elif event == "添加文件":
                if not values['-TREE-']:
                    sg.popup("请选择添加文件所在的文档目录！") 
                doc = self.find_doc_by_name(values['-TREE-'][0])
                if not doc:
                    sg.popup("请选择添加文件所在的文档目录！")
                    continue
                win = CreateFileUI(self.person, doc, self.service)
            if win:
                win.show()
                self.doc_tree_data = sg.TreeData()
                self.docs = self.service.get_doc_by_pid(self.person.id)
                for doc in self.docs:
                    self.add_doc('', doc)
                window['-TREE-'].update(values=self.doc_tree_data)
        window.Close()
        