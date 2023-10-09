import sys, os, subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd


class App(Frame):

    def __runcommand(self, command, project_directory=None):
        try:
            if project_directory:
                return subprocess.run(command, cwd=self.cwd, capture_output=True)
                
            else:
                return subprocess.run(command, capture_output=True)

        except:
            print('The current operation could not be completed.')



    def __createProjectWindow(self, parent):

        pop = Toplevel(parent)
        pop.title('No Project Detected!')
        NOTICE = f"""No valid CPSA project was detected in this directory.\n
                    Would you like to create one?
                    """
        Label(pop, text=NOTICE).pack()

        execute = ['cpsa4init']

        cbtn = ttk.Button(pop, text='Create Project', command=lambda: self.__runcommand(execute, project_directory=True)).pack()


    def __checkCPSAVersion(self):
        # execute = ['cpsa4', '-v']
        v = self.__runcommand('cpsa4 -v')
        return v.stderr




    def __openProjectDirectory(self, parent):

        self.cwd = fd.askdirectory()
        if not os.path.exists(self.cwd + '/cpsa4.mk'):
            print('no project detected')
            self.__createProjectWindow(parent)




    def __init__(self, root):

        super().__init__(root)
        root.title('CPSA UI Revamp')
        root.geometry("720x405")
        root.option_add('*tearOff', False)
        root.minsize(405, 375)

        self.cwd = ''
        self.version = self.__checkCPSAVersion().decode('ascii')[5]

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