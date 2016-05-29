#Implementation of SVC
import sys
import difflib
import re
import os
list1=[]
j=1
 
str1=sys.argv[1]                                   #to get the command line argument                     
searchobject=re.search("txt", str1, re.M|re.I)     #pattern matching to check if file name or version number given
if searchobject:
    flag=1
else:
    flag=0

if(flag==1):                                       #committing changes
    DIR = 'C:\\Users\\admin\\workspace\\L3cube-SVC\\version'
    j=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    fo = open(str1, "rb+")
    a=os.path.getsize(str1)
    flag1=1;
    if(a!=0):                                      #checking for empty file
        if(j!=0):                                  #creating first version                                  
            for i1 in range (1,int(j+1)):          #to check if same file exists
                file1 = DIR+"\\"+"file"+str(i1)+".txt"
                diff = difflib.ndiff(open(file1).readlines(),open(str1).readlines())
                delta = ''.join(x[2:] for x in diff if x.startswith('- '))
                
                if (delta==""):
                    print "There exists a file with the same content!"
                    flag1=0
                    break
                else:
                    flag1=1
        if (flag1==1):
            inputfromfile = fo.read(100);
            filenamenew=DIR+"\\"+"file"+str(j+1)+".txt"
            fo2=open(filenamenew,"wb+")
            fo2.write(inputfromfile)
            fo.close()
            fo2.close()
            print "File committed successfully!"
    else:
        print "File has no contents"        
else:                                              #for version display
    DIR = 'C:\\Users\\admin\\workspace\\L3cube-SVC\\version'
    version=int(str1)
    nooffiles=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    if(version<=nooffiles):                        #checking if version exists or not
        filenamenew=DIR+"\\"+"file"+str(version)+".txt"   
        fo1 = open(filenamenew, "rb+")
        inputfromfile1 = fo1.read(100);
        print "The contents from version ",version,"is :"
        print inputfromfile1
        fo1.close()
    else:
        print "This version does not exist!"
