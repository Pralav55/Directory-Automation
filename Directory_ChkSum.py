#Importing required Libraries
from sys import *
import os
import hashlib
import time

#Function which reads file and calculate size using md5 algorithm
def hashfile(path,blocksize = 1024):
    afile = open(path,'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()

    return hasher.hexdigest()

#Function which displays check sum of all files present 
def DisplayCheckSum(path,log_dir="CheckSum"):
    #Generating absoulte path of the directory 
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)
    
    exists = os.path.isdir(path)

    #creating folder on same file path
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    
    seperator = "-" * 80

    #Creating a file with a particular name
    log_path = os.path.join(log_dir , "CheckSum%s.log" %(time.ctime()))
    
    #Opening the created file in write mode
    f = open(log_path,'w')

    #Writing content into the file
    f.write(seperator+"\n")
    f.write("Check Sum of All Files : "+time.ctime()+"\n")
    f.write(seperator+"\n")

    #Travling through folders and files using os.walk() method
    if exists:
        for dirName, subDir, filelist in os.walk(path):
            for fileN in filelist:
                path = os.path.join(dirName,fileN)
                file_hash = hashfile(path)
                
                #Displaying every path and check sum of file
                f.write("%s\n"%path)
                f.write("%s\n"%file_hash)
                f.write("\n")

    else:
        print("Invalid Path")

#Execution starts from main
def main():
    #Displays Header
    print("----------Python Automation Directory Check Sum-----------")

    print("Application name : "+argv[0])

    #Handling arguments
    if(len(argv) != 2):
        print("Error : Invalid number of arguments")
        exit()
    
    if(argv[1] == "-h" or argv[1] == "-H"):
        print("This script is used to traverse specific directory and display checksum of files")
        exit()

    if(argv[1] == "-u" or argv[1] == "-U"):
        print("Usage : ApplicationName AbsolutePath_of_directory Extension")
    
    #Handling Exception 
    try:
        #Calling Function which displays check sum
        DisplayCheckSum(argv[1])
    
    except:
        print("Error : ")

#Application Starter
if __name__ == "__main__":
    Start_time = time.time()
    main()
    EndTime = time.time()

    print("Time required to execute : %s "%(EndTime-Start_time))