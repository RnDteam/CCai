import xml.etree.ElementTree as Et

mistake_msg = "טעיתי"
startover_msg = "פניה חדשה"


class Conversation:
    def __init__(self):
        tree = Et.parse('conversation_tree.xml')
        self.root = tree.getroot()
        self.current_node = self.root
        self.path = []

    def get_node_answer(self):
        link = self.current_node.attrib.get('link')
        if link is not None:
            self.current_node = self.root.find('.//node[@id="'+str(link)+'"]')
        answer = self.current_node.text
        for child in self.current_node:
            answer += "<button>"+child.attrib.get('value')+"</button>"
        if answer is None:
            return self.back_to_start()
        return "<text>"+answer+"<image>user.png</image>"+"</text>"

    def answer(self, msg):
        if msg == mistake_msg:
            return self.one_step_back()
        elif msg == startover_msg:
            return self.back_to_start()
        for child in self.current_node:
            if msg == child.attrib.get('value'):
                self.path.append(self.current_node)
                self.current_node = child
                return self.get_node_answer()

    def back_to_start(self):
        self.current_node = self.root
        return self.get_node_answer()

    def one_step_back(self):
        if len(self.path) == 0:
            return self.back_to_start()
        self.current_node = self.path.pop()
        return self.get_node_answer()
