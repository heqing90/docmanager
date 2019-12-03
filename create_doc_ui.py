import PySimpleGUI as sg
import os
from model import Document

class CreateDocUI:
    def __init__(self, person, service):
        self.service = service
        self.person = person
        self.layout = [
            [sg.Text("请填写档案目录")],
            [sg.Text("姓名", size=(16, 1)), sg.InputText(default_text=person.name,disabled=True, key="name")],
            [sg.Text("档案名", size=(16, 1)), sg.InputText(key="doc")],
            [sg.Submit(button_text="提交", key="submit"), sg.Cancel(button_text="重置", key="reset")]
        ]
        self.window = sg.Window("档案目录", self.layout)
    
    def make_doc_on_disk(self, person, doc):
        try:
            doc_path = '{}\\{}\\{}'.format(os.getcwd(), person.name, doc.name)
            if not os.path.exists(doc_path):
                print(doc_path)
                os.makedirs(doc_path) 
        except Exception as e:
            print(e)

    def show(self):
        window  = self.window
        while True:
            event, values = window.read()
            if event == "submit":
                doc = Document(None, values['doc'], self.person.id, [])
                doc_id = self.service.add_doc(doc)
                if doc_id > 0:
                    self.make_doc_on_disk(self.person, doc)
                break
            elif event == "reset":
                window.Element("doc").Update(value= "")
            else:
                break
        window.Close()