import tkinter
from format_translators import translation

class Role(object):



    def __init__(self, name=None):
        self.name = name
        self.messages = []
        self.translatedMessages = []
        self.sending = []
        self.trace = ''
        self.vars = {}
        self.final = ''

    def addMessage(self, m, sending):
        self.messages.append(m)
        self.sending.append(sending)

    def translateMessages(self):
        for idx, m in enumerate(self.messages):

            is_sending = self.sending[idx]
            if is_sending:
                # print(m.sender.get(), 'sending', m.contents.get(), 'to', m.recip.get())
                self.translatedMessages.append(translation.translateMessage(m.contents.get(), is_sending))

            if not is_sending:
                # print(m.recip.get(), 'receives', m.contents.get(), 'to', m.sender.get())
                self.translatedMessages.append(translation.translateMessage(m.contents.get(), is_sending))
        
        self.trace = translation.createTrace(self.translatedMessages)
        self.final = self.roleTransform()
        # print(self.final)


    def roleTransform(self):

        final_role = f"(defrole {self.name}\n\t"
        final_role += self.trace + '\n)'
        return final_role