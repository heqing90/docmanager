import PySimpleGUI as sg
from model import Person
from datetime import datetime as dt

class PersonDetailUI:
    def __init__(self, person, is_change):
        disable = is_change 
        self.layout = [
            [sg.Text("序号", size=(16, 1) ), sg.InputText(default_text=person.id, disabled=True)],
            [sg.Text("姓名", size=(16, 1) ), sg.InputText(default_text=person.name, disabled=disable)],
            [sg.Text("性别", size=(16, 1)), sg.InputCombo(['男', '女'], default_value=person.sex, disabled=disable, size=(8, 1))],
            [sg.Text("身份证", size=(16, 1)), sg.InputText(default_text=person.id_card, disabled=disable)]
        ]
        if not disable:
            self.layout.append([sg.Submit(button_text="修改", key="submit")])
        self.window = sg.Window("人员详情", layout=self.layout)
    
    def show(self):
        window = self.window
        while True:
            event, values = window.read()
            if event == "submit":
                break
            if not event:
                break
        window.Close()