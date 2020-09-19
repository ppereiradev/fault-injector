import multiprocessing as mp
import subprocess
from time import sleep
import numpy as np

class Application:
    def __init__(self, name, fault, repair, password, ip_address):
        self.process = None
        self.name = name
        self.fault = fault
        self.repair = repair
        self.password = password
        self.ip_address = ip_address

    def fault_repair_job(self):
        while True:
            fault_time = np.mean(np.random.exponential(self.fault))
            # time is in second
            print(self.name, "is  UP, next FAULT will be in:", fault_time, "seconds")
            sleep(fault_time)
            
            repair_time = np.mean(np.random.exponential(self.repair))
            # we considering the wlan0 interface, chenge it if necessary
            #fault_command = "sshpass -p " + self.password + " ssh -f -o StrictHostKeyChecking=no " + self.ip_address + " -l root \"ifconfig wlan0 down && sleep " + str(int(repair_time)) + " && ifconfig wlan0 up &>/dev/null &\""
            '''
            OBS: we use the fault_command is a command that deactivates and activates the network interface of the other computer.
                 This command is composed of two Linux commands with a interval between them, the interval is the repair_time.
            '''
            #subprocess.Popen(fault_command, shell=True, stdout=subprocess.PIPE)

            print(self.name, "is DOWN, next REPAIR will be in:", repair_time, "seconds")
            sleep(repair_time)

    def run(self):
        self.process = mp.Process(target=self.fault_repair_job)
        self.process.daemon = True
        self.process.start()   

    def terminate(self):
        self.process.kill()
