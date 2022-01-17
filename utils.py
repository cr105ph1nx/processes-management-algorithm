import threading
from time import sleep

CLOCK_TOP = 1
LATENCY = 6
SUM_PRIORITIES = 14138
KILO = 1024
DICT_PROCESSES = {
    # "COLOR": [PRIORITY, T_CPU, QUANTUM, EXECUTION_VALUE]
    "white": [9548, 0, 0, 0],
    "green": [1024, 0, 0, 0],
    "red": [3121, 0, 0, 0],
    "blue": [335, 0, 0, 0],
    "yellow": [110, 0, 0, 0],
}
CURRENT_PROCESS = ""


def getTOP():
    print("Current Process: ", CURRENT_PROCESS)
    for process in DICT_PROCESSES:
        array = DICT_PROCESSES[process]
        print(f"-{process}: CPU: {array[1]} \t\t EXEC_VALUE: {array[3]}")
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

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
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


def getDataByColor(color):
    # Fetch array of data from dictionary by color
    array = DICT_PROCESSES[color]
    return array


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


def main():
    # Fill dictionary with the value of quantum respective to each process
    fillQuantums()
    # Update EXEC_VALUE every clock top
    thread_exec_value = calculateExecValue()
    while True:
        # Append process to memory
        appendNewProcess()
        # Fetch quantum of current process
        quantum = fetchCurrentQuantum()
        sleep(quantum)
        # Update T_CPU
        calculateT_CPU(quantum)
        # Get state of processes
        getTOP()


if __name__ == "__main__":
    main()
