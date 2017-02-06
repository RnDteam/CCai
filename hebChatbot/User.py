import States

class User():
    def __init__(self, ip):
        self.ip = ip
        self.convMemory = {}
        self.CURRENT_STATE = States.States.EntityExtraction
        self.CURRENT_ENTITY = None
        self.CURRENT_ACTION = None
        self.is_clear = True
        self.inputs_arr = []
        self.row_index = 0
        self.index_input_arr = 0
        self.is_mistaken = False
        self.is_input_saved = False
        self.is_input_already_known = False
        self.is_approve_details = False
        self.is_asked_yes_no_question = False
        self.is_wrong_input = False

    def resetUser(self):
        self.CURRENT_STATE = States.States.EntityExtraction
        self.CURRENT_ENTITY = None
        self.CURRENT_ACTION = None
        self.is_clear = True
        self.inputs_arr = []
        self.row_index = 0
        self.index_input_arr = 0
        self.is_mistaken = False
        self.is_input_saved = False
        self.is_input_already_known = False
        self.is_approve_details = False
        self.is_asked_yes_no_question = False
        self.is_wrong_input = False

class UserMessage():
    def __init__(self, user, message):
        self.user = user
        self.message = message