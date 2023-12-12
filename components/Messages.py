import tkinter

class Message(object):

    def __init__(self, id=None, sender=None, recip=None, contents=None):
        self.id = id
        # self.sender = sender
        # self.recip = recip
        # self.contents = contents
        self.sender = tkinter.StringVar()
        self.recip = tkinter.StringVar()
        self.contents = tkinter.StringVar()

    def updateContent(self, c):
        self.contents = c

    