import xml.etree.ElementTree as Et


class Conversation:
    def __init__(self):
        tree = Et.parse('conversation_tree.xml')
        self.root = tree.getroot()
        self.current_node = tree.getroot()
        for child in self.root:
            print(child.tag)

    def get_node_answer(self):
        answer = self.current_node.text
        for child in self.current_node:
            answer += "<button>"+child.tag+"</button>"
        return "<text>"+answer+"</text>"

    def answer(self, msg):
        for child in self.current_node:
            if msg == child.tag:
                self.current_node = child
                return self.get_node_answer()

    def back_to_start(self):
        self.current_node = self.root
        return self.get_node_answer()

    #def one_step_back(self):
