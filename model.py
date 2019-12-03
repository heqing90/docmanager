class Person:

    def __init__(self, id, name, sex, id_card, update_time, create_time):
        self.id = id
        self.name = name
        self.sex = sex
        self.id_card = id_card
        self.create_time = create_time
        self.update_time = update_time

    def to_string(self):
        return "姓名: {}, 性别: {}, 身份证: {}".format(self.name, self.sex, self.id_card)


class Document:
    def __init__(self, id, name, person_id, files):
        self.id = id
        self.person_id = person_id
        self.name = name
        self.files = files

class File:
    def __init__(self, id, name, path, doc_id):
        self.id = id
        self.doc_id = doc_id
        self.name = name
        self.path = path