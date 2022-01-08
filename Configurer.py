import sys
#import os
#import subprocess
import paramiko
import ipaddress

from paramiko.client import AutoAddPolicy

#This function will ask for the host names as IP addresses then return a list of the hosts given to the program
def getHosts():
    print("Please type host names: ")
    host = sys.stdin.readline().strip() #read host from console input
    hosts = [] #create list called hosts
    while host != "Done": #while the input is not "Done" do this
        if not ipaddress.ip_address(host): #if the input does not match a typical IPv4 addressing scheme then throw an error and exit
            print("Error: given host is not a valid IP address")
            quit()
        if host in hosts: #if the host is already present in the list then throw and error and exit
            print("Error: this host is a duplicate IP address")
            quit()
        hosts.append(host) #add the given host to the list
        host = sys.stdin.readline().strip() #read in a new host
    print("Finished reading hosts")
    print(hosts)
    return hosts

#This function will ask for the commands to be used on each of the hosts that were given in the previous step
def getCommands():
    print("Please type commands to be applied to all given hosts")
    command = sys.stdin.readline().strip() #read in a new command from the console
    commands = [] #create a list called commands
    while command != "Done": #while the input is not "Done" do this
        commands.append(command) #add the command to the list
        command = sys.stdin.readline().strip() #read in a new command from the console
    print("Finished reading commands")
    print(commands)
    return commands        


#running the script:
hosts = getHosts() #obtain the hosts
commands = getCommands() #obtain the commands
#for every host in the hosts list, ssh into that host and run all the commands
print("Input username: ")
username = sys.stdin.readline().strip()
print("Input password: ")
password = sys.stdin.readline().strip()
for host in hosts:
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(AutoAddPolicy)
    connection.connect(host, username=username, password=password, timeout=10) #SSH into the host
    connection.load_system_host_keys()
    for command in commands: #For every command in the commands variable
        stdin, stdout, stderr = connection.exec_command(command, len(command), 5) #Run the command and catpture the output from the console
        if "'%' invalid input error" in stderr or "SHELL PARSER FAILURE:" in stderr: #Check for errors from the output
            print("Error: command failed to run")
            print("Output from console: %s", stdout)
            print("Error from console: %s", stderr)
            quit()
        print(stdout)
print("Successfully completed all commands for every host")

