import PySimpleGUI as sg
import os
from model import File
import shutil

class CreateFileUI:
    def __init__(self, person, doc, service):
        self.person = person
        self.doc = doc
        self.service = service
        self.layout = [
            [sg.Text("添加档案文件")],
            [sg.Text("姓名", size=(16, 1)), sg.InputText(default_text=person.name, disabled=True)],
            [sg.Text("档案名", size=(16, 1)), sg.InputText(default_text=doc.name, disabled=True)],
            [sg.Text("文档名", size=(16, 1)), sg.InputText(key="name")],
            [sg.Text("文件地址",size=(16, 1)), sg.InputText(key="path"), sg.FileBrowse(button_text="浏览")],
            [sg.Submit(button_text="提交", key="submit"), sg.Cancel(button_text="重置", key="reset")]
        ]
        self.window = sg.Window("档案文件", self.layout)

    def make_file_on_disk(self, person, doc, f):
        try:
            subfix = f.path.split(".")
            if len(subfix) > 0:
                subfix = ".{}".format(subfix[-1])
            else:
                subfix = ""
            fn = "{}\\{}\\{}\\{}{}".format(os.getcwd(), person.name, doc.name, f.name, subfix)
            if os.path.exists(fn):
                os.rename(fn, "{}.bak".format(fn))
            else:
                shutil.copyfile(f.path, fn)
            return fn
        except Exception as e:
            print(e)
            return ""            

    def show(self):
        while True:
            window = self.window
            event, values = window.read()
            if event == "submit":
                file = File(None, values['name'], values['path'], self.doc.id) 
                fn = self.make_file_on_disk(self.person, self.doc, file)
                if fn:
                    file.path = fn
                self.service.add_file(file)
                break
            elif event == "reset":
                window.Element("name").Update(value= "")
                window.Element("doc").Update(value= "")
            else:
                break
        window.Close()