'''
.Write a program to list duplicate files from hard drive
------------------------------------------------------------------------
The aim of this assignment is to list all the duplicate files from the hard drive and give user option to remove them or merge them.
'''


import os
import difflib          
import filecmp

                                                                #create a file with names of all file in a directory and subdirectories
a = open("output.txt", "w")
mypath="C:\\Users\\Lenovo\\Downloads\\Documents\\test_cases"
for path, subdirs, files in os.walk(mypath):
    for filename in files:
            f = os.path.join(path, filename)
            a.write(str(f)+"\n")
a.close()

fd=open("output.txt","r")
datalist=fd.readlines()                                        #create a list of name of files
#print (datalist)

datalist2=[]
datalist_size=[]

#calculate file size 
for i in datalist:
    datalist2.append(str(i).strip())                           #create a list containing size of files in accordance to datalist
    datalist_size.append(os.path.getsize(str(i).strip())) 
   # print(str(i).strip()) 
    
#array of file names and file size separately
#print(datalist2) 
#print(datalist_size)

#creating a tuple
zipped=list(zip(datalist2,datalist_size))
#print(zipped)

#soring of tupple
zipped.sort(key = lambda t: t[1])
#print(zipped)

file_sizes=[x[1] for x in zipped]
file_names=[x[0] for x in zipped]
#print (file_sizes)
#print (file_names)
flags=[0 for x in range(len(file_sizes))]                                              #flag array to track duplicate files

#duplicate files
h=len(file_names)
for i in range(h-1):
    for j in range(i+1,h):
        if (file_sizes[i]+100)>file_sizes[j]:
            if (filecmp.cmp(file_names[i], file_names[j], shallow=False)) == True:      #if two files are excatly the same then set the flag for it
                flags[j]=1
            
#for DELETE
k=0 
for i in range(h):
    if flags[i]==1:
        os.remove(file_names[i-k])                                                      #delete files whose flag is set in flags array
        del file_names[i-k]
        del file_sizes[i-k]     
        k+=1  

txtfile_names=[]
txtfile_sizes=[]
for x in file_names:
    if x.endswith(".txt"):
        txtfile_names.append(x)                                                         #get file names and thier respective sizes of all '.txt' files from file_names
        txtfile_sizes.append(os.path.getsize(x))


h=len(txtfile_sizes)
flags2=[0 for x in range(h)]
#print(txtfile_names,txtfile_sizes)
#print (len(txtfile_sizes))

#Merging of two similar files 
old_text=[]
for i in range(h-1):
    if flags2[i]==0:
        for j in range(i+1,h):
            if flags2[j]==0:
                if (txtfile_sizes[i]+100) >= txtfile_sizes[j]:
                    with open(txtfile_names[i],"r") as myfile1:
                        str1=myfile1.read()
                    with open(txtfile_names[j],"r") as myfile2:
                        str2=myfile2.read()
                    diff = difflib.SequenceMatcher(None, str1, str2)                     #calculate the ratio of similarity between two files
                    if diff.ratio() >= 0.7:
                        # print(txtfile_names[i],txtfile_names[j])
                        print(txtfile_names[i])
                        print("compared with")
                        print(txtfile_names[j])
                        print("Percentage of similarity: "+str((diff.ratio()*100)))
                        flags2[i]=1
                        flags2[j]=1
                        lines1 = open(txtfile_names[i], "r").readlines()
                        lines2 = open(txtfile_names[j], "r").readlines()
                        diffSequence = difflib.ndiff(lines1, lines2)       
                        name=input("Enter name of new merged file: ")
                        new_file = open("C:\\Users\\Lenovo\\Downloads\\Documents\\test_cases\\"+name+".txt","w+")
                        ch=input("Choose a merging option: 1)Manual  2)Automatic :")
                        print ("\n ----- Contents of new file ----- \n") 
                        if ch == "1":  
                            for k, line in enumerate(diffSequence):
                                print (line)
                                if line.startswith("? "):                           #create new file containing merged data
                                    print("")
                                else:
                                    old_text.append(str(line))
                            print("")
                            for n in old_text:
                                if str(n).startswith("- "):
                                    print(str(n))
                                    choice=input("This line was present in file1 only. Do you want to include it (y/n) ?")
                                    if choice == "y":
                                        new_file.write(str(n))
                                elif str(n).startswith("+ "):
                                    print(str(n))
                                    choice=input("This line was present in file2 only. Do you want to include it (y/n) ?")
                                    if choice == "y":
                                        new_file.write(str(n))
                                else:
                                    new_file.write(str(n))
                            old_text=[]  
                        if ch == "2":
                            for k, line in enumerate(diffSequence):
                                print (line)
                                if line.startswith("? "):                           #create new file containing merged data
                                    print("")
                                else:
                                    new_file.write(line[2:])
                            new_file.close()            
                                                                           
                            
k=0
for i in range(h):
    if flags2[i]==1:
        os.remove(txtfile_names[i-k])
        del txtfile_names[i-k]                                                      #deleting the original files once they are already used for merging
        del txtfile_sizes[i-k]     
        k+=1  