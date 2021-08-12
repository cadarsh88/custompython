from _typeshed import NoneType
from datetime import datetime, timedelta
import random
import numpy as np

# All Disk sizes will be in MBs
"""
Initial Data Disk Size - 100GB
Data Size - 60GB
Free Space - 40GB

Initial Log Disk Size - 50GB
Log Data Size - 20GB
Free Space - 30GB

Data Drive Free Space
- Mon to Fri - Linear Increments - 300MB/day
- Sat and Sun - No Changes

Log Drive Free Space
- Mon to Fri - Random Bursts (0-10) for 2hrs daily 
	     - Day with multiples of 4, random bursts for 2hrs at 50 - 150
- Sat and Sun - No Changes
"""

dataDiskSize = 102400
logDiskSize = 51200

initDataSize = (60*1024)
initLogSize = (20*1024)

global initDataFreeSpace
global initLogFreeSpace
initDataFreeSpace = dataDiskSize-initDataSize
initLogFreeSpace = logDiskSize-initLogSize


def genDataDiskConsumption(starttime, endtime):
    startDateTimeObj = datetime.strptime(starttime, '%m/%d/%Y %I:%M:%S %p')
    endDateTimeObj = datetime.strptime(endtime, '%m/%d/%Y %I:%M:%S %p')
    freeSpaceArray = []
    freeSpaceArray.append(initDataFreeSpace)
    newFreeSpace = initDataFreeSpace
    newDateTimeObj = startDateTimeObj
    #startDateTimeObj += datetime.timedelta(minutes=1)
    while(newDateTimeObj <= endDateTimeObj):
        seedlist = []
        seedlist.append(newDateTimeObj)
        if(newDateTimeObj.strftime("%A") not in ['Saturday', 'Sunday']):
            reduceSpace = 0.208
            newFreeSpace = newFreeSpace-reduceSpace
            seedlist.append(newFreeSpace)
            freeSpaceArray.append(seedlist)
        else:
            seedlist.append(newFreeSpace)
            freeSpaceArray.append(seedlist)
        newDateTimeObj += timedelta(minutes=1)
    return freeSpaceArray


datadrivefreespacearray = genDataDiskConsumption(
    '5/1/2021  12:01:00 AM', '8/1/2021  12:00:00 AM')


def genLogDiskConsumption(starttime, endtime):
    startDateTimeObj = datetime.strptime(starttime, '%m/%d/%Y %I:%M:%S %p')
    endDateTimeObj = datetime.strptime(endtime, '%m/%d/%Y %I:%M:%S %p')
    freeSpaceArray = []
    initialLogFreeSpace = initLogFreeSpace  # 30GB
    freeSpaceArray.append(initialLogFreeSpace)
    newLogSpace = initLogSize  # 20GB
    newDateTimeObj = startDateTimeObj
    randWindowStart = None
    #startDateTimeObj += datetime.timedelta(minutes=1)
    while(newDateTimeObj <= endDateTimeObj):
        seedlist = []
        seedlist.append(newDateTimeObj)
        #throttleStartTime = random.randint(11, 16)
        if(newDateTimeObj.strftime("%A") not in ['Saturday', 'Sunday']):
            winDateTimeObj = newDateTimeObj.strftime("%m/%d/%Y %H:%M:%S")
            winDateTimeObj = datetime.strptime(
                winDateTimeObj, '%m/%d/%Y %H:%M:%S')
            if((int(newDateTimeObj.strftime("%w")) % 4) == 0):
                if(randWindowStart == None):
                    randWindowStart = random.randint(11, 16)  # 13
                    randLogGrowth = random.randint(50, 150)  # 110
                if(winDateTimeObj.hour in range(randWindowStart, randWindowStart+2)):
                    if((winDateTimeObj.minute) % 10 == 0):
                        randSummer = randLogGrowth + \
                            random.randint(0, 25)  # 110+20
                        newLogSpace = newLogSpace + randSummer
                        initialLogFreeSpace = initialLogFreeSpace - randSummer
                    seedlist.append(initialLogFreeSpace)
                    freeSpaceArray.append(seedlist)
                else:
                    #newLogSpace = newLogSpace
                    #initialLogFreeSpace = initialLogFreeSpace - newLogSpace
                    seedlist.append(initialLogFreeSpace)
                    freeSpaceArray.append(seedlist)
            else:
                if(randWindowStart == None):
                    randWindowStart = random.randint(10, 16)  # 13
                    randLogGrowth = random.randint(10, 50)  # 30
                if(winDateTimeObj.hour in range(randWindowStart, randWindowStart+2)):
                    if((winDateTimeObj.minute) % 10 == 0):
                        randSummer = randLogGrowth + \
                            random.randint(0, 10)  # 30+10 = 40
                        newLogSpace = newLogSpace + randSummer  # 20520
                        initialLogFreeSpace = initialLogFreeSpace - randSummer
                    seedlist.append(initialLogFreeSpace)
                    freeSpaceArray.append(seedlist)
                else:
                    #newLogSpace = newLogSpace
                    #initialLogFreeSpace = initialLogFreeSpace - newLogSpace
                    seedlist.append(initialLogFreeSpace)
                    freeSpaceArray.append(seedlist)
                if((winDateTimeObj.hour == randWindowStart+2) and (randWindowStart != None)):
                    randWindowStart = None
        else:
            initialLogFreeSpace = initLogFreeSpace
            newLogSpace = initLogSize
            seedlist.append(initialLogFreeSpace)
            freeSpaceArray.append(seedlist)
        newDateTimeObj += timedelta(minutes=1)
    return freeSpaceArray


logdrivefreespacearray = genLogDiskConsumption(
    '5/1/2021  12:01:00 AM', '8/1/2021  12:00:00 AM')
textfile = open("a_file2.txt", "w")
for element in freespacearray:
    textfile.write(str(element) + "\n")
textfile.close()
