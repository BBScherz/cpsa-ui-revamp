import tkinter
from format_translators import translation

class Role(object):



    def __init__(self, name=None):
        self.name = name
        self.messages = []
        self.translatedMessages = []
        self.sending = []

    def addMessage(self, m, sending):
        self.messages.append(m)
        self.sending.append(sending)

    def translateMessages(self):
        for idx, m in enumerate(self.messages):

            is_sending = self.sending[idx]
            if is_sending:
                # print(m.sender.get(), 'sending', m.contents.get(), 'to', m.recip.get())
                self.translatedMessages.append(translation.translate(m.contents.get(), is_sending))

            if not is_sending:
                # print(m.recip.get(), 'receives', m.contents.get(), 'to', m.sender.get())
                self.translatedMessages.append(translation.translate(m.contents.get(), is_sending))