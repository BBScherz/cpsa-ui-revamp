import os, subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

from components import Messages as ms
from components import Roles as role
from components import Protocol as pr
from format_translators.translation import createHerald

class App(Frame):

    ####################################################################
    # runcommand                                                       #
    # A helper function that facilitates shell commands for CPSA       #
    # Inputs: command -> a list or string representing a shell command #
    #         project_directory -> determines what directory the       #
    #                              command should execute in           #
    # Outputs: CompletedProcess object or NoneType                     #
    ####################################################################
    def __runcommand(self, command, project_directory=None):
        try:
            if project_directory:
                return subprocess.run(command, cwd=self.cwd, capture_output=True)    
            else:
                return subprocess.run(command, capture_output=True)
        except:
            print('The current operation could not be completed.')


    ##############################################################################
    # createProjectWindow                                                        #
    # Creates a popup window when the selected directory does not have a project #
    # Inputs: parent -> the parent window to overlay the creation popup widget   #
    # Outputs: None                                                              #
    ##############################################################################
    def __createProjectWindow(self, parent):
        pop = Toplevel(parent)
        pop.title('No Project Detected!')
        NOTICE = f"""No valid CPSA project was detected in this directory.\n
                    Would you like to create one?
                    """
        Label(pop, text=NOTICE).pack()

        execute = ['cpsa4init']
        cbtn = ttk.Button(pop, text='Create Project', command=lambda: self.__runcommand(execute, project_directory=True)).pack()


    ###########################################################
    # checkCPSAVersion                                        #
    # Automatically checks which version of CPSA is installed #
    # Inputs: None                                            #
    # Outputs: v -> a CompletedProcess object used later      #
    ###########################################################
    def __checkCPSAVersion(self):
        v = self.__runcommand('cpsa4 -v')
        return v


    ################################################################
    # openProjectDirectory                                         #
    # Allows users to select a folder where a CPSA project exists  #
    # Inputs: Parent -> the parent widget where a project creation #
    #         window is overlayed (passed to createProjectWindow)  #
    ################################################################
    def __openProjectDirectory(self, parent):
        self.cwd = fd.askdirectory()
        if not os.path.exists(self.cwd + '/cpsa4.mk'):
            self.__createProjectWindow(parent)
        self.__createWorkArea()
        


    def __algebraSelect(self, f):
        alg_frame = Frame(f)
        alg_label = Label(alg_frame, text="Select Type of Algebra")
        alg_label.pack(side=TOP)
 
        b = Radiobutton(alg_frame, text="Basic", variable=self.alg_type, value=1)
        b.pack(side=LEFT)
        dh = Radiobutton(alg_frame, text="Diffie-Hellman", variable=self.alg_type, value=0)
        dh.pack(side=LEFT)

        alg_frame.pack()
    

    def __createNewMessage(self, f):

        created = ms.Message(id=self.mid_counter)
        new_message_frame = Frame(f, name=str(self.mid_counter))

        msg_num = Label(new_message_frame, text=f"Message {self.mid_counter + 1}: ")
        msg_send = Entry(new_message_frame, textvariable=created.sender, width=8)
        arrow = Label(new_message_frame, text='\u2192')
        msg_recv = Entry(new_message_frame, textvariable=created.recip, width=8)
        msg_content = Entry(new_message_frame, textvariable=created.contents)
        rem_msg = Button(new_message_frame, text='X', command= lambda: self.__removeMessage(f=new_message_frame, message=created))

        msg_num.pack(side=LEFT, padx=10)
        msg_send.pack(side=LEFT, padx=10)
        arrow.pack(side=LEFT)
        msg_recv.pack(side=LEFT, padx=10)
        msg_content.pack(side=LEFT, padx=10)
        rem_msg.pack(side=LEFT, padx=10)
        new_message_frame.grid(row=self.msg_count, column=0, pady=15)
        
        self.messages[self.mid_counter] = created
        self.mid_counter += 1
        self.msg_count +=1

        self.menubar.entryconfigure('Create', state='active')
        # print('msg counter:', self.msg_count)
        # for m in list(self.messages.keys()):
        #     print(self.messages[m].sender.get(), self.messages[m].recip.get(), self.messages[m].contents.get())
        
        
    def __removeMessage(self, f, message):
        
        try:
            f.destroy()
        except:
            messagebox.showerror(title='Cannot Delete Message!', message='There was an error deleting this message.')
            pass

        
        try:
            del self.messages[message.id]
            self.msg_count -= 1
        except KeyError as e:
            messagebox.showerror(title='Cannot Delete Message!', message='There was an error deleting this message. It seems this message does not exist.')
            pass

        if self.msg_count == 0:
            self.menubar.entryconfigure('Create', state='disabled')



    def __heraldName(self, f):
        name_frame = Frame(f)
        name_label = Label(name_frame, text="Herald Title")
        name_label.pack(side=TOP)
 
        h = Entry(name_frame, textvariable=self.herald_name)
        h.pack(side=LEFT)

        name_frame.pack()




    def __createWorkArea(self):
        area = Frame(self.master)
        
        self.__heraldName(area)
        self.__algebraSelect(area)
        
        
        message_space = Canvas(area, highlightbackground='black')
        scroll = Scrollbar(message_space, orient=VERTICAL, command=message_space.yview)
        # scroll.pack(side=RIGHT, fill=Y)
        message_space.config(scrollregion=message_space.bbox(ALL))
        message_space.config(yscrollcommand=scroll.set)
        
        new = ttk.Button(area, text=f"Create New Message +", command=lambda: self.__createNewMessage(message_space)).pack()
        sep = Label(area, text='Sender\tRecipient\tContents', font=('Helvetica 12 underline')).pack()


        message_space.pack(side=BOTTOM, expand=True)
        scroll.grid(column=1, sticky=NS)
        area.pack()
        

    def __compile(self, parent):
        roles = {}

        project_herald = createHerald(title=self.herald_name, algebra=self.alg_type)
        # print(project_herald)



        try:
            for m in list(self.messages.values()):

                sender = m.sender.get()
                recipient = m.recip.get()
                if sender not in roles.keys() and recipient:
                    r = role.Role(name=sender)
                    roles[sender] = r

                if recipient not in roles.keys() and sender:
                    r = role.Role(name=recipient)
                    roles[recipient] = r

        except:
            messagebox.showerror('Role Error!', 'A sender or recipient field was left blank.  Make sure all fields are valid and try again')

        print(len(roles))

        for m in list(self.messages.values()):
            sender = m.sender.get()
            recipient = m.recip.get()

            roles[sender].addMessage(m=m, sending=True)
            roles[recipient].addMessage(m=m, sending=False)

        for r in list(roles.values()):
            r.translateMessages()
        al = 'basic' if self.alg_type.get() == 1 else 'diffie-hellman'
        protocol = pr.Protocol(roles = list(roles.values()), algebra=al, name=self.herald_name.get())
        print(protocol.proto)



        
            





    def __init__(self, root):

        super().__init__(root)
        root.title('CPSA UI Revamp')
        root.iconbitmap('assets/icon.ico')
        root.geometry("720x405")
        root.option_add('*tearOff', False)
        root.minsize(405, 375)

        self.cwd = ''
        self.valid_project = False
        self.alg_type = IntVar()
        self.herald_name = StringVar()
        self.project_name = StringVar()
        self.mid_counter = 0
        self.msg_count = 0
        self.messages = {}
        try:
            v = self.__checkCPSAVersion()
            self.version = v.stderr.decode('ascii')[5]
        except:
            NOINSTALLATION = f""" No CPSA v4.x installtion was detected.  You may have an older version installed, or none at all.
                                \nGo to this link to install: https://hackage.haskell.org/package/cpsa and click below to close this program."""
            messagebox.showerror(title='Configuration Error!', message=NOINSTALLATION)
            # root.destroy()   TODO: Close the app at this line


        self.menubar = Menu(root)
        root['menu'] = self.menubar

        menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Select project directory...', command=lambda: self.__openProjectDirectory(parent=root))

        menu_compile = Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_compile, label='Create', state='disabled')
        menu_compile.add_command(label='Compile...', command=lambda: self.__compile(parent=root))

        self.pack()
        


def main():
    root = Tk()
    app = App(root)
    app.mainloop()
    


if __name__ == '__main__':
    main()