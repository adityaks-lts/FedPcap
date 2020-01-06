import subprocess as sp
import os.path
from os import path
import sys
import time

class colors:
    GREEN = '\033[92m'
    STOP = '\033[0m'
    RED='\033[31m'

def options():
    print colors.GREEN + "1. " + colors.STOP + "Top 10 Visited Sites"
    print colors.GREEN + "2. " + colors.STOP + "User-Agents"
    print colors.GREEN + "3. " + colors.STOP + "Connections"
    print colors.GREEN + "4. " + colors.STOP + "String Search"
    print colors.GREEN + "5. " + colors.STOP + "IP List"
    print colors.GREEN + "6. " + colors.STOP + "Ports list"
    print colors.RED + "(q) " +colors.STOP + "Quit"
    
    command = raw_input("Enter command> ")

    if str(command) == "1":
        sites()
        options()
    elif str(command) == "2":
        ua()
        options()
    elif str(command) == "3":
        conn()
        options()
    elif str(command) == "4":
        global grep
        grep = raw_input("Enter your query string >")
        search()
        options()
    elif str(command) == "5":
        ip()
        options()
    elif str(command) == "6":
        portList()
        options()
    elif str(command) == "q":
        sys.exit()
    elif str(command) != "1" or "2" or "3" or "4" or "5" or "6" or "q":
        print colors.RED + "Invalid command" + colors.STOP
        time.sleep(1)
        options()

def main():
    print """ 
 _______  _______        _  _______           _______  _______ 
(  ____ \(  ____ \      | |(  ____ )         (  ___  )(  ____ )
| (    \/| (    \/      | || (    )| ______  | (   ) || (    )|
| (__    | (__     _____| || (____)|/  ____| | (___) || (____)|
|  __)   |  __)   | |   | ||  _____)| (      |  ___  ||  _____)
| (      | (      | |   ) || (      | |      | (   ) || (      
| )      | (____/\| (__/  /| )      | (____/\| )   ( || )      
|/       (_______/(______/ |/       (_______/|/     \||/        

"""

    print "Enter the file name or (q) to quit> "
    global fileName
    fileName = raw_input()

    if path.isfile(str(fileName)) == True:
        time.sleep(1)
        options()
    elif str(fileName) == "q":
        sys.exit()
    else:
        print colors.RED + "Wrong filename" + colors.STOP
        time.sleep(1)
        main()

def ip():
    ipList = sp.check_output(['tshark -r {} -T fields -e ip.dst -e ip.src | sort | uniq'.format(fileName)], shell=True)
    print str(ipList)

def sites():
    topSites = sp.check_output(['tshark -r {} -Y http.request -T fields -e http.host | sort | uniq -c | sort -rn | head'.format(fileName)],shell=True)
    print str(topSites)

def ua():
    userAgent = sp.check_output(['tshark -r {} -Y http.request -T fields -e http.user_agent | sort | uniq -c'.format(fileName)],shell=True)
    print str(userAgent)

def portList():
    ports = sp.check_output(['tshark -r {} -Y "tcp" -T fields -e tcp.srcport -e tcp.dstport | sort | uniq -c'.format(fileName)],shell=True)
    print str(ports)

def search():
    searchString = sp.check_output(['ngrep -I {} | grep "{}"'.format(fileName,grep)],shell=True)
    print str(searchString)

def conn():
    connection = sp.check_output(['tshark -r {} | sort'.format(fileName)],shell=True)
    print str(connection)

main()
