'''
The birthday paradox concerns the probability that, in a set of n randomly chosen people, some pair of them will have the same birthday.
By the pigeonhole principle,there is 50% probability with 23 people.
'''

from random import randint

count = 0
w, h = 23, 100000

for x in range(0,h):						#loop for each set of 23 people
	a = [randint(1,365) for x in range(w)] 			#assign value to set
	flags=[0 for x in range(366)]				#flags set of 0(false) initially

	for i in range(0,w):					#check for repeated birthdays
		if flags[a[i]]!=0:
			count+=1				#count for total number sets in which repitated birthdays occur
			break					#if atleast one match is found, stop the loop
		else:
			flags[a[i]] = 1

print ((float(count)/h)*100)  					#display the percentage of sets where match is found
