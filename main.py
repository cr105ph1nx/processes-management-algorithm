# Imports each and every method and class
# of module tkinter and tkinter.ttk
from tkinter import *
from time import sleep
from threading import Thread
PYTHONUNBUFFERED = "yes"

ALIVE = True
CLOCK_TOP = 1
LATENCY = 6
SUM_PRIORITIES = 14138
KILO = 1024
DICT_PROCESSES = {
    # "COLOR": [PRIORITY, T_CPU, QUANTUM, EXECUTION_VALUE]
    "white": [9548, 0, 0, 0],
    "red": [3121, 0, 0, 0],
    "green": [1024, 0, 0, 0],
    "blue": [335, 0, 0, 0],
    "yellow": [110, 0, 0, 0],
}
CURRENT_PROCESS = ""


def getTOP():
    print("CURRENT PROCESS: ", CURRENT_PROCESS.upper())
    for process in DICT_PROCESSES:
        array = DICT_PROCESSES[process]
        print(
            f"-{process.upper()}: CPU: {array[1]} \t\t EXEC_VALUE: {array[3]}")
    print("\n")


def appendNewProcess():
    global CURRENT_PROCESS
    # Initialize value of min_exec_value
    process = list(DICT_PROCESSES.keys())[0]
    min_exec_value = DICT_PROCESSES[process][3]

    for process in DICT_PROCESSES:
        # Get array of data
        array = DICT_PROCESSES[process]
        exec_value = array[3]
        if exec_value == 0:
            CURRENT_PROCESS = process
            break
        else:
            if(exec_value <= min_exec_value):
                min_exec_value = exec_value
                CURRENT_PROCESS = process


def calculateT_CPU(quantum):
    # Get array of data
    array = DICT_PROCESSES[CURRENT_PROCESS]
    # Replace old T_CPU
    array[1] = array[1] + quantum
    # Replace array of data
    DICT_PROCESSES[CURRENT_PROCESS] = array


class calculateExecValue(object):
    def __init__(self, interval=CLOCK_TOP):
        self.interval = interval

        thread2 = Thread(target=self.run, args=())
        thread2.daemon = True
        thread2.start()

    def stop(self):
        self._is_running = False

    def run(self):
        while ALIVE:
            #  Execution value of a process (i) = time spent in CPU * 1024/ priority of process (i).
            for process in DICT_PROCESSES:
                # Get array of data
                array = DICT_PROCESSES[process]
                # Calculate new EXEC_VALUE
                exec_value = array[1]*KILO/array[0]
                # Replace old EXEC_VALUE
                array[3] = exec_value
                # Replace array of data
                DICT_PROCESSES[process] = array
            sleep(self.interval)


def fetchCurrentQuantum():
    return DICT_PROCESSES[CURRENT_PROCESS][2]


def fillQuantums():
    # Quantum of process (i) = latency * priority of process (i) / sum of priorities
    for process in DICT_PROCESSES:
        # Get array of data
        array = DICT_PROCESSES[process]
        # Calculate new EXEC_VALUE
        quantum = LATENCY*array[0]/SUM_PRIORITIES
        # Replace old EXEC_VALUE
        array[2] = quantum
        # Replace array of data
        DICT_PROCESSES[process] = array


def startTimer():
    global thread
    thread.start()


def endTimer():
    global ALIVE
    ALIVE = False

    print("TIMER CANCELLED.\n")


class start(object):
    def __init__(self, interval=0.01):
        self.interval = interval
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def stop(self):
        self._stop_event.set()

    def run(self):
        global circles_frame
        global CURRENT_PROCESS
        thread_exec_value = calculateExecValue()
        while ALIVE:
            # Append process to memory
            appendNewProcess()
            # Update circles frame
            circles_frame = light_current_process(circles_frame)
            circles_frame.pack(anchor=NW)
            # Get state of processes
            getTOP()
            # Fetch quantum of current process
            quantum = fetchCurrentQuantum()
            sleep(quantum)
            # Update T_CPU
            calculateT_CPU(quantum)


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
                       height="2", command=lambda: startTimer())
    ok_button.pack(side=TOP, padx=5, pady=5)
    # Add cancel button
    cancel_button = Button(frame, text='Arreter', width="30",
                           height="2", command=lambda: endTimer())
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
    global thread
    thread = Thread(target=start)
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
