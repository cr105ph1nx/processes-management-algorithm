# Imports each and every method and class
# of module tkinter and tkinter.ttk
from tkinter import *
from utils import fillQuantums, DICT_PROCESSES, CURRENT_PROCESS
from time import sleep


def start():
    global circles_frame, CURRENT_PROCESS
    # Append process to memory
    CURRENT_PROCESS = "red"
    print("process changed")
    circles_frame = light_current_process(circles_frame)
    circles_frame.pack(anchor=NW)


def light_current_process(container):
    # Creates a object of class canvas
    frame = Canvas(container,  height="130")
    # Creates a circle of diameter 80
    (y0, y1) = (20, 130)
    (x0, x1) = (20, 130)
    for process in DICT_PROCESSES:
        if(process == CURRENT_PROCESS):
            frame.create_oval(x0, y0, x1, y1, fill=process, width=0)
        else:
            frame.create_oval(x0, y0, x1, y1, fill="grey", width=0)
        x0 = x1 + 40
        x1 = x0 + (y1-y0)

    # Pack the canvas to the main window and make it expandable
    frame.pack(fill=BOTH)

    return frame


def create_circles_frame(container):
    # Creates a object of class canvas
    frame = Canvas(container,  height="130")
    # Creates a circle of diameter 80
    (y0, y1) = (20, 130)
    (x0, x1) = (20, 130)
    for process in DICT_PROCESSES:
        frame.create_oval(x0, y0, x1, y1, fill="grey", width=0)
        x0 = x1 + 40
        x1 = x0 + (y1-y0)

    # Pack the canvas to the main window and make it expandable
    frame.pack(fill=BOTH)

    return frame


def create_labels_frame(container):
    frame = Frame(container)
    # Add labels
    for process in DICT_PROCESSES:
        array = DICT_PROCESSES[process]
        Label(frame, text=str(round(array[2]*1000))+"ms", width=15,
              padx=15, pady=20).pack(side=LEFT)

    return frame


def create_buttons_frame(container):
    frame = Frame(container)
    # Add ok button
    ok_button = Button(frame, text='Demarrer', width="30",
                       height="2", command=lambda: start())
    ok_button.pack(side=TOP, padx=5, pady=5)
    # Add cancel button
    cancel_button = Button(frame, text='Arreter', width="30", height="2")
    cancel_button.pack(side=BOTTOM, padx=5)

    return frame


class Shape:
    def __init__(self, master=None):
        self.master = master
        # Calls create method of class Shape
        self.create()

    def create(self):
        global circles_frame

        circles_frame = create_circles_frame(self.master)
        circles_frame.pack(anchor=NW)

        labels_frame = create_labels_frame(self.master)
        labels_frame.pack(anchor=NW)

        buttons_frame = create_buttons_frame(self.master)
        buttons_frame.pack(anchor=SE)


if __name__ == "__main__":
    # Fill quantums
    fillQuantums()
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    master = Tk()
    shape = Shape(master)
    # Sets the title to Shapes
    master.title("Simulation d'algorithme de gestion de processus")
    # Sets the geometry and position of window on the screen
    master.geometry("750x300")
    master.columnconfigure(1, weight=1)

    # Infinite loop breaks only by interrupt
    master.mainloop()
