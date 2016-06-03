
'''
1. Is Birthday paradox really valid? 
----------------------------------------- 
 
Write a code that verifies - birthday paradox is indeed correct. 
'''




from random import randint

count = 0											#counts number of rooms in which birthdays are repeated 
people, rooms = 23, 1000							#'people' keeps count of number of people in a room. 'room' keeps count number of rooms

for x in range(0,rooms):                        
    a = [randint(1,365) for x in range(people)]	    #assign random birthdays to each person in the room  

    unique=set(a)									#creates a set containing unique birthdays from set 'a'

    if (len(a)!=len(unique)):						#if length of 'unique' set and 'a' set is different then it means atleast one birthday was assigned to two people
        count+=1                					#increment count for each successful experiment

print ("Percentage of sets which had repetition of birthdays  : " , (float(count)/rooms)*100)          