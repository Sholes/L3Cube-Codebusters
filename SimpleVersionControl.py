#Implementation of SVC
import sys
import difflib
import re
import os
import textwrap
list1=[]
j=1
if len(sys.argv) == 1:
    print "enter choice \n 1)Appending a new line at the end of the file \n 2)Deleting any existing line"
    choice=input()
    if(choice==1):                                                 #appending a line
         
        fod=open("file1.txt","r")                               
        max2=len(fod.readlines())                                  #count no of lines 
        if(max2<20):                                               #set max no of lines as 20
            fd=open("file1.txt","a")
            print "enter the string to be appended"
            astr=raw_input()
            appendstring="\n"+astr
            fd.write("\n")
            fd.write(textwrap.fill(appendstring[0:10], width=10))  #to set max char per line as 10
            fd=open("file1.txt","rb")
            contentsnow=fd.read()
            print contentsnow
            fd.close()
        else:
            print "Limit of file reached"
    else:                                                           #deleting a line by line number
        print "the contents of the file are:"
        fd1=open("file1.txt","r")
        contentsnow1=fd1.readlines()
        print contentsnow1
        print "enter line number to be deleted"
        deleteit=input()
        fd1.close()
        del contentsnow1[deleteit:deleteit+1]
        print contentsnow1
        fout=open("file1.txt","w")
        fout.writelines(contentsnow1)
        fout.close()

    
else:                                                                #to commit and display
    str1= sys.argv[1]
                                    
    searchobject=re.search("txt", str1, re.M|re.I)                  #pattern matching to check if file name or version number given
    if searchobject:
        flag=1
    else:
        flag=0

    if(flag==1):                                                     #committing changes
        
        
        DIR = 'C:\\Users\\admin\\workspace\\L3cube-SVC\\version'
        j=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        fo = open(str1, "rb+")
        a=os.path.getsize(str1)
        flag1=1;
        if(a!=0):                                                    #checking for empty file
            if(j!=0):                                                #creating first version                                  
                for i1 in range (1,int(j+1)):                        #to check if same file exists
                    file1 = DIR+"\\"+"file"+str(i1)+".txt"
                    diff = difflib.ndiff(open(file1).readlines(),open(str1).readlines())
                    delta = ''.join(x[2:] for x in diff if x.startswith('- '))
                    
                    if (delta==""):
                        print "There exists a file with the same content!"
                        flag1=0
                        break
                    else:
                        flag1=1
            if (flag1==1):                                             #to commit the file
                inputfromfile = fo.read(100);
                filenamenew=DIR+"\\"+"file"+str(j+1)+".txt"
                fo2=open(filenamenew,"wb+")
                fo2.write(inputfromfile)
                fo.close()
                fo2.close()
                print "File committed successfully!"
        else:
            print "File has no contents"        
    else:                                                               #for version display
        DIR = 'C:\\Users\\admin\\workspace\\L3cube-SVC\\version'
        version=int(str1)
        nooffiles=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        if(version<=nooffiles):                                         #checking if version exists or not
            filenamenew=DIR+"\\"+"file"+str(version)+".txt"   
            fo1 = open(filenamenew, "rb+")
            inputfromfile1 = fo1.read(100);
            print "The contents from version ",version,"is :"
            print inputfromfile1
            fo1.close()
        else:
            print "This version does not exist!"
