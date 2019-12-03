import PySimpleGUI as sg
from service import PersionServiceImpl as psi
from service import DocFileServiceImpl as dsi
from create_doc_ui import CreateDocUI
from create_file_ui import CreateFileUI
from create_person_ui import CreatePersonUI
from person_detail_ui import PersonDetailUI
from doc_detail_ui import DocDetailUI
from db import SimpleDB

# read all person data from database
simple_db = SimpleDB()
simple_db.open(r"doc_management_sqlite3.db")
person_service = psi(simple_db)
doc_file_service = dsi(simple_db)

people = person_service.get_all_by_page(1, 40)

header = ["序号", "姓名", "性别", "身份证","创建时间", "更新时间"]
col_widths = [8, 25, 6, 18, 25, 25]
skip_len = 0
for col_width in col_widths:
    skip_len = skip_len + col_width
skip_len = skip_len - 45
data = []
for person in people:
    elem = [person.id, person.name, person.sex, person.id_card, person.update_time, person.create_time]
    data.append(elem)

right_click_menu_def =  ['&Right', ['查看', '修改', '档案', '!删除']]
layout = [
    [sg.Submit(button_text='刷新列表', key='-REFRESH_PERSON-'),sg.Submit(button_text="添加人员", key='-ADD_PERSON_BTN-'), sg.Text(size=(skip_len, 1)), sg.InputText(default_text="", tooltip="姓名", size=(20, 1), key="-SEARCH_NAME-"), sg.Submit(button_text="搜索", key="-SEARCH_NAME_BTN-")],
    [sg.Table(values=data, headings=header, def_col_width=12, max_col_width=100, col_widths=col_widths, 
        auto_size_columns=False, justification='center', alternating_row_color='lightblue', num_rows=40,
        right_click_menu=right_click_menu_def, key="-MANAGE_TABLE-")]
]
window = sg.Window("档案管理系统", layout, resizable=False, grab_anywhere=False)

while True:
    event, values = window.read()
    print(event, values)
    manage_tab = window.Element('-MANAGE_TABLE-')
    if not event:
        break
    win = None
    need_refresh = False
    if event == "-ADD_PERSON_BTN-":
        win = CreatePersonUI(person_service)
        people = person_service.get_all_by_page(1, 40)
        need_refresh = True
    elif event == "-REFRESH_PERSON-":
        people = person_service.get_all_by_page(1, 40) 
        need_refresh = True 
    elif event == '-SEARCH_NAME_BTN-':
        if '-SEARCH_NAME-' not in values or not values['-SEARCH_NAME-']:
            continue
        print("search by name: ", values['-SEARCH_NAME-'])
        people = person_service.get_by_name(values['-SEARCH_NAME-'])
        need_refresh = True
    else:
        if not manage_tab.SelectedRows:
            sg.popup("请单击选择人员!")
            continue
        elif event == '查看':
            win = PersonDetailUI(people[manage_tab.SelectedRows[0]], True)
        elif event == '修改':
            win = PersonDetailUI(people[manage_tab.SelectedRows[0]], False)
        elif event == '档案':
            win = DocDetailUI(people[manage_tab.SelectedRows[0]], doc_file_service) 
    if win:
        win.show()
    if need_refresh:
        data = []
        for person in people:
            elem = [person.id, person.name, person.sex, person.id_card, person.update_time, person.create_time]
            data.append(elem)
        selected = None
        if len(people) > 0:
            selected = [0]
        window["-MANAGE_TABLE-"].update(values=data, select_rows=selected)
window.Close()

simple_db.close()