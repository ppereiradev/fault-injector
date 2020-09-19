import multiprocessing as mp
import subprocess
from time import sleep
import numpy as np
from os_class import OperatingSystem

class Hardware:
    def __init__(self, fault, repair, password, ip_address):
        self.process = None
        self.fault = fault
        self.repair = repair
        self.password = password
        self.ip_address = ip_address
        self.opsystem = None

    def fault_repair_job(self, os_fault, os_repair, app_names, app_fault, app_repair):
        while True:
            # setting up OS process
            self.opsystem = OperatingSystem(os_fault, os_repair, self.password, self.ip_address)
            self.opsystem.run(app_names, app_fault, app_repair)

            fault_time = np.mean(np.random.exponential(self.fault))
            # time is in second
            print("Hardware is  UP, next FAULT will be in:", fault_time, "seconds")
            sleep(fault_time)
            
            repair_time = np.mean(np.random.exponential(self.repair))
            # we considering the wlan0 interface, chenge it if necessary
            #fault_command = "sshpass -p " + self.password + " ssh -f -o StrictHostKeyChecking=no " + self.ip_address + " -l root \"ifconfig wlan0 down && sleep " + str(int(repair_time)) + " && ifconfig wlan0 up &>/dev/null &\""
            '''
            OBS: we use the fault_command is a command that deactivates and activates the network interface of the other computer.
                 This command is composed of two Linux commands with a interval between them, the interval is the repair_time.
            '''
            #subprocess.Popen(fault_command, shell=True, stdout=subprocess.PIPE)

            # killing operating system process
            self.opsystem.terminate()


            print("Hardware is DOWN, next REPAIR will be in:", repair_time, "seconds")
            sleep(repair_time)

    def run(self, os_fault, os_repair, app_names, app_fault, app_repair):
        self.process = mp.Process(target=self.fault_repair_job, args=(os_fault, os_repair, app_names, app_fault, app_repair, ))
        self.process.start()
    
    def terminate(self):
        if self.opsystem is not None: 
            self.opsystem.terminate()
        self.process.join()
        self.process.kill()


