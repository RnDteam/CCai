import States

class User():
    def __eq__(self, other_user):
        if self.CURRENT_STATE == other_user.CURRENT_STATE \
                and self.CURRENT_ENTITY == other_user.CURRENT_ENTITY \
                and self.CURRENT_ACTION == other_user.CURRENT_ACTION \
                and self.is_clear == other_user.is_clear \
                and self.inputs_arr == other_user.inputs_arr \
                and self.row_index == other_user.row_index \
                and self.index_input_arr == other_user.index_input_arr \
                and self.is_mistaken == other_user.is_mistaken \
                and self.is_input_saved == other_user.is_input_saved \
                and self.is_input_already_known == other_user.is_input_already_known \
                and self.is_approve_details == other_user.is_approve_details \
                and self.is_asked_yes_no_question == other_user.is_asked_yes_no_question \
                and self.is_wrong_input == other_user.is_wrong_input:
                    return True
        else:
            return False

    def make_equal(self, other_user):
        self.CURRENT_STATE = other_user.CURRENT_STATE
        self.CURRENT_ENTITY = other_user.CURRENT_ENTITY
        self.CURRENT_ACTION = other_user.CURRENT_ACTION
        self.is_clear = other_user.is_clear
        self.inputs_arr = other_user.inputs_arr
        self.row_index = other_user.row_index
        self.index_input_arr = other_user.index_input_arr
        self.is_mistaken = other_user.is_mistaken
        self.is_input_saved = other_user.is_input_saved
        self.is_input_already_known = other_user.is_input_already_known
        self.is_approve_details = other_user.is_approve_details
        self.is_asked_yes_no_question = other_user.is_asked_yes_no_question
        self.is_wrong_input = other_user.is_wrong_input

    def __init__(self, ip):
        self.ip = ip
        self.convMemory = {
            "איי-פי": ip
        }
        self.resetUser()

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