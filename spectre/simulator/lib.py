
import os
from spectre.psfascii import *
import sys
from subprocess import Popen, PIPE, STDOUT
from config import *
import time

def getVersion():
    try:
        cmd = "{spectre} -version".format(spectre=SPECTRE)
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, env=ENVIRON) 
        stdout = p.communicate()[0].split()
        i = stdout.index('version')
	version = float(stdout[i+1].split('.')[0] + '.' + "".join(stdout[i+1].split('.')[1:]))
	return version
    except:
        raise Exception("can not extract version")		

import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        print self.name + repr(getVersion())
        print "Exiting " + self.name

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-3", 3)
thread4 = myThread(4, "Thread-4", 4)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

#while thread2.isAlive():
#    if not thread1.isAlive():
#        exitFlag = 1
#    pass
#print "Exiting Main Thread"

thread1.run()
thread2.run()
thread3.run()
thread4.run()

