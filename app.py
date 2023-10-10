import os, subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox


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




    def __init__(self, root):

        super().__init__(root)
        root.title('CPSA UI Revamp')
        root.geometry("720x405")
        root.option_add('*tearOff', False)
        root.minsize(405, 375)

        self.cwd = ''
        try:
            v = self.__checkCPSAVersion()
            self.version = v.stderr.decode('ascii')[5]
        except:
            NOINSTALLATION = f""" No CPSA v4.x installtion was detected.  You may have an older version installed, or none at all.
                                \nGo to this link to install: https://hackage.haskell.org/package/cpsa and click below to close this program."""
            messagebox.showerror(title='Configuration Error!', message=NOINSTALLATION)
            # root.destroy()   TODO: Close the app at this line
            



        menubar = Menu(root)
        root['menu'] = menubar

        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Select project directory...', command=lambda: self.__openProjectDirectory(parent=root))

        self.pack()
        


def main():
    root = Tk()
    app = App(root)
    app.mainloop()
    


if __name__ == '__main__':
    main()