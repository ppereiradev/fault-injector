import datetime
import argparse
from hardware_class import Hardware
import time



if __name__ == '__main__':
    ''''
    -i  interval for collecting samples
    -p  password to connect the ssh server
    -n  network interface
    -a  ip address of the computer

    Ex: python3 main.py -i 5 -p 12345 -n wlan0 -a 192.168.0.1
    '''
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--monitoring-interval", required=True, type=float,
        help="how long the interval for collecting samples will be in seconds")
    ap.add_argument("-p", "--password", required=True,
        help="the root password to connect remotely to the computer that the faults will be injected in")
    ap.add_argument("-n", "--network-interface", required=True,
        help="the network interface of the computer that the faults will be injected in")
    ap.add_argument("-a", "--ip-address", required=True,
        help="the ip address to connect remotely to the computer that the faults will be injected in")
    args = vars(ap.parse_args())

    print("""
        __  ___      _____   _________   _____        _           __            
       /  |/  /____ / __  \ / ___/___/  /_  _/___    (_)__  _____/ /_____  _____
      / /|_/ / __  / /  \  / / / /__     / // __ \  / / _ \/ ___/ __/ __ \/ ___/
     / /  / / /_/ / /___/ / /__(__  /  _/ // / / / / /  __/ /__/ /_/ /_/ / /    
    /_/  /_/\____/_______/\___/____/  /___/_/ /_/_/ /\___/\___/\__/\____/_/     
                                            /___/                            """)

    print("[1] FAULT INJECTOR")
    print("[2] STATISTICAL ANALYSIS")
    operation = input("option: ")

    if operation == '1':
        n_applications = input("Number of Applications: ")
        app_names = []

        fault_app = []
        repair_app = []

        for i in range(int(n_applications)):
            app_names.append(input(str(i + 1) + "- Application Name: "))
            fault_app.append(int(input(str(app_names[-1]) + " Fault Time: ")))
            repair_app.append(int(input(str(app_names[-1]) + " Repair Time: ")))


        fault_os = int(input("OS Fault Time: "))
        repair_os = int(input("OS Repair Time: "))

        fault_hw = int(input("Hardware Fault Time: "))
        repair_hw = int(input("Hardware Repair Time: "))

        password = args["password"]
        ip_address = args["ip_address"]

        try:
            hardware = Hardware(int(fault_hw), int(repair_hw), password, ip_address)
            hardware.run(fault_os, repair_os, app_names, fault_app, repair_app)
            while True:
                pressed = input("\n\n\nmain process; to quit press q!\n\n\n")
                if pressed == 'q':
                    hardware.terminate()
                    break
                time.sleep(1)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

    elif operation == '2':


        data = pd.read_csv('monitoramento_raspberry.txt', sep=" ", header=None)

        cont_u = 0
        cont_d = 0

        for i  in range(len(data[4])):
            if data[3][i] == 'U':
                cont_u += 1
            else:
                cont_d += 1

        else:
            print("Invalid input!")