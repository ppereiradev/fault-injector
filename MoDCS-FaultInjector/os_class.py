import multiprocessing as mp
import subprocess
from time import sleep
import numpy as np
from application_class import Application

class OperatingSystem:
    def __init__(self, fault, repair, password, ip_address):
        self.process = None
        self.fault = fault
        self.repair = repair
        self.password = password
        self.ip_address = ip_address
        self.apps = None

    def fault_repair_job(self, app_names, app_fault, app_repair):
        
        while True:
            # setting up one process for each application
            self.apps = self._util_app_processes(app_names, app_fault, app_repair)
            [a.run() for a in self.apps]

            # calculating a random exponential time
            fault_time = np.mean(np.random.exponential(self.fault))
            # time is in second
            print("Operating System is  UP, next FAULT will be in:", fault_time, "seconds")
            sleep(fault_time)
            
            # calculating a random exponential time
            repair_time = np.mean(np.random.exponential(self.repair))
            
            # we considering the wlan0 interface, chenge it if necessary
            #fault_command = "sshpass -p " + self.password + " ssh -f -o StrictHostKeyChecking=no " + self.ip_address + " -l root \"ifconfig wlan0 down && sleep " + str(int(repair_time)) + " && ifconfig wlan0 up &>/dev/null &\""
            
            '''
            OBS: we use the fault_command is a command that deactivates and activates the network interface of the other computer.
                 This command is composed of two Linux commands with a interval between them, the interval is the repair_time.
            '''
            #subprocess.Popen(fault_command, shell=True, stdout=subprocess.PIPE)
            
            # killing all applications
            [a.terminate() for a in self.apps] 

            print("Operating System is DOWN, next REPAIR will be in:", repair_time,"seconds")
            sleep(repair_time)

    def run(self, app_names, app_fault, app_repair):
        self.process = mp.Process(target=self.fault_repair_job, args=(app_names, app_fault, app_repair,))
        self.process.start()

    def _util_app_processes(self, app_names, app_fault, app_repair):
        apps = []
        for i in range(len(app_names)):
            apps.append(Application(app_names[i], app_fault[i], app_repair[i], self.password, self.ip_address))
        return apps

    def terminate(self):
        [a.terminate() for a in self.apps]
        self.process.join()
        self.process.kill()

