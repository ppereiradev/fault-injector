from threading import Thread
import subprocess
import thread
import time
import datetime
import numpy
import argparse
import pandas as pd
import numpy as np 

#e.g. 
# python fault_injector.py --component nginx --monitoring-interval 5 --fault-rate 10 --repair-rate 5
# python fault_injector.py -c nginx -i 5 -f 10 -r 5

#function fault injection in the application
def fault_injection_application(app_names,fault, repair, fault_command, repair_command):
	global killapp

	while 1:
		fault_time = numpy.random.exponential(fault, 1)
		print app_names + " UP, next FAULT will be in: " + str(fault_time) + "s"
		time.sleep(fault_time)
		if killapp == True: break
		output = subprocess.check_output(['bash','-c', fault_command])
		repair_time = numpy.random.exponential(repair, 1)
		print app_names + " DOWN, next REPAIR will be in: " + str(repair_time) + "s"
		time.sleep(repair_time)
		if killapp == True: break
		output = subprocess.check_output(['bash','-c', repair_command])

#function fault injection in the OS
def fault_injection_os(fault, repair, fault_command, repair_command):
	global killapp
	global killos
	global fault_app
	global repair_app
	global password
	global ip_address
	global app_name
	global command_stop_app
	global command_start_app 

	if is_app_alive(app_name, password, ip_address) == '0':
		if is_os_alive(ip_address) == '0':
			pass
		for i in range(len(app_name)):
			if not ("service" in command_start_app[i] or "start" in command_start_app[i] or "systemctl" in command_start_app[i]):
				tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root \"" + command_start_app[i] + " . &>/dev/null &\""))
			else:
				 tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root " + command_start_app[i]))
			
			tapps.daemon = True
			tapps.start()
			tapplications.append(tapps)

	while True:
		fault_time = numpy.random.exponential(fault, 1)
		print "OS UP, next FAULT will be: " + str(fault_time) + "s"
		time.sleep(fault_time)

		if is_os_alive(ip_address) == '0':
			killapp = True
			break

		killapp = True
		subprocess.Popen(fault_command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

		repair_time = numpy.random.exponential(repair, 1)
		print "OS DOWN, next REPAIR will be: " + str(repair_time) + "s"
		time.sleep(repair_time)
		if killos == True: break
		subprocess.Popen(repair_command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
		killapp = False
		
		if is_os_alive(ip_address) == '0':
			pass
		for i in range(len(app_name)):
			if not ("service" in command_start_app[i] or "start" in command_start_app[i] or "systemctl" in command_start_app[i]):
				tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root \"" + command_start_app[i] + " . &>/dev/null &\""))
			else:
				 tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root " + command_start_app[i]))
			
			tapps.daemon = True
			tapps.start()
			tapplications.append(tapps)

def fault_injection_hw(fault, repair, fault_command, repair_command):
	global killapp
	global killos
	global fault_os
	global repair_os
	global password
	global ip_address
	global address_mac

	# if is_os_alive(ip_address) == '0':
	# 	time.sleep(900)
	# 	tos = Thread(target=fault_injection_os, args=(float(fault_os),float(repair_os),
	# 		"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root shutdown -h now",
	# 		"sudo wakeonlan " + address_mac))
	# 	tos.daemon = True
	# 	tos.start()
	
	while True:
		fault_time = numpy.random.exponential(fault, 1)
		print "HARDWARE UP, next FAULT will be: " + str(fault_time) + "s"
		time.sleep(fault_time)
		if is_os_alive(ip_address) != '0':
			killos = True
			killapp = True
			subprocess.Popen(fault_command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
			
		repair_time = numpy.random.exponential(repair, 1)
		print "HARDWARE DOWN, next REPAIR will be: " + str(repair_time) + "s"
		time.sleep(repair_time)
		if is_os_alive(ip_address) == '0':
			subprocess.Popen(repair_command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
			killos = False
			killapp = False

			tos = Thread(target=fault_injection_os, args=(float(fault_os),float(repair_os),
				"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root shutdown -h now",
				"sudo wakeonlan " + address_mac))
			tos.daemon = True
			tos.start()
		
#monitor
def monitor(app_names, monitor_time, password, ip_address):
	while True:	
		output = verify_service(app_names, password, ip_address)
		if output=='0':
			with open("monitoramento.txt", "a") as myfile:
				data = datetime.datetime.now()
				print str(data)  + " service D 1"
				myfile.write(str(data)  + " service D 1" + "\n")
		elif output!='0':
			with open("monitoramento.txt", "a") as myfile:
				data = datetime.datetime.now()
				print str(data)  + " service U 1"
				myfile.write(str(data) + " service U 1" + "\n")
		time.sleep(monitor_time)


def verify_service(app_names, password, ip_address):
	command = "ping -w 1 " +  ip_address + " | grep received | awk '{print $4}'"
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

	if output != '0':
		#command = "sshpass -p " + password + " ssh -o StrictHostKeyChecking=no " + ip_address + " -l root \"if systemctl status " + service_name + ".service | grep \'Active: active\' > /dev/null;then echo 1;else echo 0;fi\""
		for i in range(len(app_names)):
			command = "sshpass -p " + password + " ssh -o StrictHostKeyChecking=no " + ip_address + " -l root \"top -n1 -b | grep " + app_names[i] + " | wc -l\""
			output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
			
			if output == '0':
				break 
		return output
	else:
		return '0'

def is_app_alive(app_names, password, ip_address):
	output = '0'
	for i in range(len(app_names)):
		command = "sshpass -p " + password + " ssh -o StrictHostKeyChecking=no " + ip_address + " -l root \"top -n1 -b | grep " + app_names[i] + " | wc -l\""
		output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
		if output == '0': break 
	return output

def is_os_alive(ip_address):
	command = "ping -w 1 " +  ip_address + " | grep received | awk '{print $4}'"
	return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

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

print """
    __  ___      _____   _________   _____        _           __            
   /  |/  /____ / __  \ / ___/___/  /_  _/___    (_)__  _____/ /_____  _____
  / /|_/ / __  / /  \  / / / /__     / // __ \  / / _ \/ ___/ __/ __ \/ ___/
 / /  / / /_/ / /___/ / /__(__  /  _/ // / / / / /  __/ /__/ /_/ /_/ / /    
/_/  /_/\____/_______/\___/____/  /___/_/ /_/_/ /\___/\___/\__/\____/_/     
                                           /___/                            """


print("[1] FAULT INJECTOR")
print("[2] STATISTICAL ANALYSIS")
operation = raw_input("option: ")


if operation == '1':
	n_applications = raw_input("Number of Applications: ")
	app_name = []
	command_stop_app = []
	command_start_app = []

	for i in range(int(n_applications)):
		app_name.append(raw_input(str(i + 1) + "- Application Name: "))
		#command_stop_app.append(raw_input("Command to stop Application[" + str(i + 1) + "]: "))
		command_start_app.append(raw_input("Command to start Application[" + str(i + 1) + "]: "))

	password = args["password"]
	ip_address = args["ip_address"]

	killapp = False
	fault_app = raw_input("Application Fault Time: ")
	repair_app = raw_input("Application Repair Time: ")

	killos = False
	fault_os = raw_input("OS Fault Time: ")
	repair_os = raw_input("OS Repair Time: ")

	fault_hw = raw_input("Hardware Fault Time: ")
	repair_hw = raw_input("Hardware Repair Time: ")

	address_mac = subprocess.Popen("sshpass -p " + password + " ssh -o StrictHostKeyChecking=no " + ip_address + " -l root cat /sys/class/net/" + args["network_interface"] + "/address", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

	try:
		print("\n\nSTARTING MONITOR...")
		tmonitor = Thread(target=monitor, args=(app_name,args["monitoring_interval"],password,ip_address))
		tmonitor.daemon = True
		tmonitor.start()
		print("MONITOR STARTED!\n\n")

		tapplications = []

		for i in range(len(app_name)):
			if not ("service" in command_start_app[i] or "start" in command_start_app[i] or "systemctl" in command_start_app[i]):
				tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root \"" + command_start_app[i] + " . &>/dev/null &\""))
			else:
				 tapps = Thread(target=fault_injection_application, args=(app_name[i],float(fault_app),float(repair_app),
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root killall " + app_name[i],
						"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root " + command_start_app[i]))
			
			tapps.daemon = True
			tapps.start()
			tapplications.append(tapps)

		tos = Thread(target=fault_injection_os, args=(float(fault_os),float(repair_os),
				"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root shutdown -h now",
				"sudo wakeonlan " + address_mac))
		tos.daemon = True
		tos.start()
		
		thw = Thread(target=fault_injection_hw, args=(float(fault_hw),float(repair_hw),
				"sshpass -p " + password + " ssh -n -o StrictHostKeyChecking=no " + ip_address + " -l root shutdown -h now",
				"sudo wakeonlan " + address_mac))
		thw.daemon = True
		thw.start()

		
	except Exception as e:
		print "erro" + str(e)

	while True:
		pass

elif operation == '2':


	data = pd.read_csv('monitoramento.txt', sep=" ", header=None)

	cont_u = 0
	cont_d = 0

	for i  in range(len(data[4])):
		if data[3][i] == 'U':
			cont_u += 1
		else:
			cont_d += 1

	else:
		print("Invalid input!")