import json
from time import sleep
from random import choice, randint
import multiprocessing

def processItem(item, return_dict):
	sleep(randint(0, 10))
	return_dict[item] = {'Passed' : True, 'extraData' : 'goesHere'}

# The List of Elements that you want to run thru a function
items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# Multiprocessing Manager Dict allows for multiprocessing jobs to return values to the main process, allowing for one Json Tree to be simultaneously constructed by multiple processes 
manager = multiprocessing.Manager()
return_dict = manager.dict()
# This is a list of the current Running Jobs
jobs = []
# This is a dictionary matching the item to the job
jobsDict = {}
# This is a list of the Jobs that have already been joined
joinedJobs = []
for item in items:
	itemAdded = False
	while itemAdded == False:
		# The integer 6 can be replaced with any desired concurrent process count, using 6, 6 processes would be immediately started and 1 additional process will be started as soon as another completes and is joined to the main process
		if len(jobs) < 6:
			print(f'Starting Job - {item}')
			# a process is started and added to the list of currently running Jobs.
			proc = multiprocessing.Process(target=processItem, args=(item, return_dict))
			jobs.append(proc)
			jobsDict[item] = proc
			proc.start()
			itemAdded = True
		else:
			sleep(.5)
		print('Current Running Jobs', jobs)
		if len(return_dict) > 0:
			for elem in return_dict:
				# This check ensures that a Job has completed, and has not yet been joined
				if return_dict[elem]['Passed'] == True and elem not in joinedJobs:
					try:
						# The Job is joined, freeing up memory + cpu, and is appended to the JoinedJobs List and removed from the Jobs (Current Running Jobs) List
						jobsDict[elem].join()
						print(f'Joined Process - {elem}')
						joinedJobs.append(elem)
						jobs.remove(jobsDict[elem])
					except Exception as e:
						print(e)
						
# Remaining Jobs are Joined
for proc in jobs:
	proc.join()
	print(f'Joined Job - {proc}')
print(return_dict)
