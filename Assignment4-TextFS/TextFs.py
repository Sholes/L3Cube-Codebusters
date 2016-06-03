import os
import sys
import errno

CURRENT_DIR="/home/mydir/Desktop/textfs/"							#Path of directory  
sf=open(CURRENT_DIR+"file",'rw+')									#Open target file in directory	
global file_names 													#Declare global variables			
file_names=[]														
global file_loc
file_loc=[]
end_of_file="!@#$!@#$"												#Define end of file delimiter
sf=open(CURRENT_DIR+"file",'rw+')

def meta_decrement():												#Decrement metadata contents after delete
	sf.seek(0,0)													#Start of file
	meta_sor=sf.readlines()											#Read information

	total_nodes=int(meta_sor[1].split(':')[1])						#Decrement total nodes count
	total_nodes-=1
	t_n_str="S_node_count :"+str(total_nodes)+"\n"
	last_nodes=int(meta_sor[4].split(':')[1])						#Update last inode number		
	last_nodes-=1
	l_n_str="Last_inode_number :"+str(last_nodes)+"\n"
	return [t_n_str,l_n_str]

def delete_file(dest_name,node_size):								#Delete a file
	sf.seek(0,0)													#Start of file 
	meta_sor=sf.readlines()
	dec_str=meta_decrement()										#Decrement metadata contents 
	
	meta_sor[1]=dec_str[0]
	meta_sor[4]=dec_str[1]
	
	line=file_loc[file_names.index(dest_name)]						#Jump to file to be deleted
				
	del meta_sor[line-node_size:line+23]							#delete inode information and file contents from list meta_sor 						
	
	sd=open(CURRENT_DIR+"file",'w')									#Open file in write mode to overwrite the contents with new file contents		

	sd.writelines(meta_sor)											#Write new contents into file after deleting insdie file
	sd.close()														#Close file	
	return "Deleted Successfully"									#Print output
	

def echo_d(dest_name):												#ECHO 				
	sf.seek(0,0)													
	line=file_loc[file_names.index(dest_name)]						#Jump to file location using list of file names  
		
	meta_sor=sf.readlines()											#Read lines and store into a list
	for x in range(line+1,line+20):									#Print till end of file delimiter is reached
		if end_of_file  in  meta_sor[x]:
			break			
		print meta_sor[x],											#Print Output


def get_all_file_names(all_nodes,first_node_add,node_size):			#Get all file names needed to print
	sf.seek(0,0)													
	
	count=0
	i=0
	for x  in range(0,first_node_add-1):							
		sf.readline()
		i+=1
	while(count!=all_nodes):										#Iterate till all file names are recorded
		
		for x in range(0,node_size-1):								#Traverse to name of file field in inode 	
			sf.readline()
			i+=1
		name=sf.readline()
		i+=1
		try:
			file_names.append(name.split(':')[1].split('\n')[0])	#Take names of files from inode of each file
			file_loc.append(i)
			for x in range(0,23):
				sf.readline()
				i+=1
		except:
			count+=1
			continue	
		count+=1
		

def copy(sor_lines,dest_name):										#Copy contents to a file
	sf.seek(0,0)													#Start of file
	line=file_loc[file_names.index(dest_name)]						#Jump to destination file's strat line number  
	meta_sor=sf.readlines()											
	meta_sor[line-3]= "size :"+str(sys.getsizeof(sor_lines))+'\n'	#Set size of destination file to size of source file
		
	for x in xrange(0,len(sor_lines)):								#Copy line by line into list
		line+=1
		meta_sor[line]=sor_lines[x]
		
	meta_sor[line+1]=end_of_file									#Write end of data delimiter into list
	sf.flush()
	sf.seek(0,0)
	sf.writelines(meta_sor)											#Write contents of list into file			
	return "Copy Successfull"										#Print output


def update_metadata(total_nodes,last_node):							#Update metadata
	sf.seek(0,0)													#Start of file
	sf.readline()													#Read current values of metadata
	sf.write("S_node_count :"+str(total_nodes))						#Write new total number of nodes(increment after create)

	sf.readline()
	sf.readline()
	sf.readline()
	sf.write("Last_inode_number :"+str(last_node))					#Update last inode number to the new value
	return 


def create(fname,last_inode_number):								#Create a new file
	frag_size=20													#Initialise inode values for new file 
	size=0
	
	inode_no ="inode_no :"+str(last_inode_number)					#Calculate inode number
	size = "size :"+str(size)										#Store all inode values in the file
	fragment_size = "fragment_size :"+str(frag_size)
	fname = "fname :"+str(fname)
	sf.seek(0,2)
	sf.write(str(inode_no)+'\n')									#Write all values in file
	sf.write(str(size)+'\n')
	sf.write(str(fragment_size)+'\n')
	sf.write(str(fname)+'\n')
	sf.write("1234567890!@#$%^&*()\n")								#Write Start of data delimiter 
	sf.write(end_of_file+"\n")
	for x in xrange(0,frag_size):
		sf.write('\n')
	sf.write("1234567890!@#$%^&*()\n")								#Write end of file delimeter
	#update_last_inode(last_inode_number)
	
	return "File was created"										#Return status to print

def main():															#Main function
	last_inode_number=0												
	sf.readline()	
			
	nodes_count=int(sf.readline().split(':')[1])					#Read metadata of file and store into variables
	first_node_add=int(sf.readline().split(':')[1])
	node_size=int(sf.readline().split(':')[1])
	last_inode_number=int(sf.readline().split(':')[1])
	get_all_file_names(nodes_count,first_node_add,node_size)		#Store all file names in a list
				
	while True:
		
		command=raw_input('textfs>>> ')								#Making our own command line interpreter 
		if not command:												#Handling unidentified commands   
			continue											
		
		command=command.split()					
		if command[0]=="create":									#CREATE 
				if command[1] in file_names:						#Check for existence of file  
					print "Already exists"
					continue
				status = create(command[1],last_inode_number+1)		#Create a file with the name given by user
			 	print status										#Print output
				nodes_count+=1 										#Increment the count in metadata 	
				last_inode_number+=1
				update_metadata(nodes_count,last_inode_number)		#Update the metadata
				global file_names
				file_names=[]
				global file_loc
				file_loc=[]
				get_all_file_names(nodes_count,first_node_add,node_size)	#Update file names in the list 
				continue

		elif command[0]=="copy":									#COPY
	
				if command[1] in file_names:						#Check for existence of source file
					print "File should be external file"			
					continue
				if command[2] not in file_names :					#Check for existence of destination file
					print "File has not been created"
					continue
				else:
					source_file = open(command[1],'r');				#Open source file  
					status = copy(source_file.readlines(),command[2]);	#Copy contents of source file into destination 
					print status									#Print output
					source_file.close()
				continue

		elif command[0]=="echo":									#ECHO
						
				if command[1] not in file_names:					#Check for existence of file 
					print "File does not exists"					#Print error
					continue				
				else:
					echo_d(command[1])								#Call echo function if file exists
				continue
	
		elif command[0]=="ls":										#LS	
				for x in file_names:								#Print names of all files from the list
					print x
				continue

		elif command[0]=="delete":									#DELETE
				if command[1] not in file_names:					#Check for existence of file 
					print "File does not exist"					#Print error
					continue
				else:
					status=delete_file(command[1],node_size)		#Call delete command if file exists				
					print status									#Print output 
					file_names=[]									#Reset list	
					file_loc=[]
					get_all_file_names(nodes_count,first_node_add,node_size)	#Update names of files in the list
	
		elif command[0]=="q":										#Exit the application
				exit(0)
		else:
				print "Invalid command"								#Print invalid command		
 

if __name__== '__main__':
	main()





