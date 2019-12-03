import PySimpleGUI as sg
from model import Person

class CreatePersonUI:
    def __init__(self, service):
        self.layout = [
            [sg.Text("请填写人员信息")],
            [sg.Text("姓名", size=(16, 1) ), sg.InputText(key="name")],
            [sg.Text("性别", size=(16, 1)), sg.InputCombo(['男', '女'], default_value='男', key="sex", size=(8, 1))],
            [sg.Text("身份证", size=(16, 1)), sg.InputText(key="idcard")],
            [sg.Submit(button_text="提交", key="submit"), sg.Cancel(button_text="重置", key="cancel")]
        ]
        self.service = service
        self.person = None
        self.window = sg.Window("新建人员", self.layout)

    def show(self):
        window = self.window
        while True:
            event, values = window.read()
            print(event, values)
            if event == "submit":
                self.person = Person(None, values['name'], values['sex'], values['idcard'], None, None)
                self.update()
                sg.popup_ok("提交成功")
                break
            elif event == "cancel":
                window.Element("name").Update(value="")
                window.Element("sex").Update(value="")
                window.Element("idcard").Update(value="")
            else:
                break
        window.Close()
    
    def update(self):
        self.service.add(self.person)