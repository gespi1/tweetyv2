'''Purpose of Program:
Send comcast a tweet when internet speeds reach below a certain level'''


import os
import subprocess
import re
import tweet
import sys
from time import sleep

pingRegex = re.compile(r'''
            (\d\.\d{2}\d?)          #ping
            (\s)                    #space
            (ms)                    #ms
''', re.VERBOSE)

downloadRegex = re.compile(r'''
                (Download:)         #Line starts with Download:
                (\s)                #space character
                (\d\d?\d?\.\d{2})   #1-3 whole numbers, .(dot), 2 decimal places
                (\s)                #space character
                (Mbit/s)            #Megabits per second
''', re.VERBOSE)

uploadRegex = re.compile(r'''
                (Upload:)           #Line starts with Upload:
                (\s)                #space character
                (\d\d?\d?\.\d{2})   #1-3 whole numbers, .(dot), 2 decimal places
                (\s)                #space character
                (Mbit/s)            #Megabits per second
''', re.VERBOSE)


#runs speedtest-cli and finds ping,download and upload speed
def check_speedTest():
    try:
        runSpeedTest = subprocess.check_output(os.path.join('/', 'home', 'gespi', 'speedtest-cli')).decode()
    except:
        print('network is off')
        sys.exit(0)
    #print(pingRegex.search(runSpeedTest).groups())
    downSpeed = downloadRegex.search(runSpeedTest).group(3)
    upSpeed = uploadRegex.search(runSpeedTest).group(3)
    #print('down: ' + downSpeed + '\n' + 'up: ' + upSpeed)
    return (downSpeed, upSpeed)

i = 0
downTotal = 0.00
upTotal = 0.00
downSpeedList = []
upSpeedList = []

#runs speedtest-cli 3 times and stores down and up values with lists
while i < 3:
 #print(i)
 downSpeed, upSpeed = check_speedTest()
 downSpeedList.append(downSpeed)
 upSpeedList.append(upSpeed)
 i = i + 1

#Add up both lists to get a total
for itemDown, itemUp in zip(downSpeedList, upSpeedList):
    downTotal = downTotal + float(itemDown)
    upTotal = upTotal + float(itemUp)

#Get averages of download and upload speed
avgDown = downTotal/3
avgUp = upTotal/3

#Find out if averages meet the requirements to send out a tweet
if avgDown < 50.0 and avgUp < 10.0:
    tweet.main("Why pay for 150Mbps when I am receiving %.2fmbps download and %.2fmbps upload on average. "
               "Please fix! #comcast #comcastsucks" % (avgDown, avgUp))
else:
    if avgDown < 40.0:
        tweet.main("Paying for 150Mbps and I am receiving %.2fmbps download on average. Please fix! "
                   "#comcast #xfinity #comcastdoesntcare" % avgDown)
    else:
        sys.exit(0)

