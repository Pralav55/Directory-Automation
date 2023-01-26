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

#Function which finds duplicate files in following path
def FindDuplicates(path):
    #Generating absoulte path of the directory 
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)
    
    exists = os.path.isdir(path)

    dups = {}

    #Travling through folders and files using os.walk() method
    if exists:
        for dirName , subdirs, fileName in os.walk(path):
            for fileN in fileName:
                path = os.path.join(dirName,fileN)
                file_Hash = hashfile(path)

                if file_Hash in dups:
                    dups[file_Hash].append(path)
                else:
                    dups[file_Hash] = [path]
        
        return dups
    
    else:
        print("Invalid Path")

#Function which creates files if duplicates found and write all duplicate file path into the file created
def PrintDuplicates(dic,log_dir="Duplicates"):
    results = list(filter(lambda x: len(x)>1 , dic.values()))

    if len(results) > 0:
        print("Duplicates Found")

        #creating folder on same file path
        if not os.path.exists(log_dir):
            try:
                os.mkdir(log_dir)
            except:
                pass
        
        seperator = "-" * 80

        #Creating a file with a particular name
        log_path = os.path.join(log_dir , "Duplicates%s.log" %(time.ctime()))
        
        #Opening the created file in write mode
        f = open(log_path,'w')

        #Writing content into the file
        f.write(seperator+"\n")
        f.write("List of Duplicates : "+time.ctime()+"\n")
        f.write(seperator+"\n")

        icnt = 0

        #Iterating over duplicates
        for res in results:
            for subres in res:
                icnt+=1

                if icnt>=2:
                    f.write("%s\n"%subres)
    else:
        print("No duplicate files found.")

#Execution starts from main
def main():
    #Displays header
    print("----------Python Automation Directory Check Sum-----------")

    print("Application name : "+argv[0])

    #Handling Arguments
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
        arr = {}

        #Calling Function which finds duplicates
        arr = FindDuplicates(argv[1])

        #Calling function which prints duplicates into a file
        PrintDuplicates(arr)
    
    except ValueError:
        print("Error : Invalid datatype of input ")
    
    except Exception:
        print("Error:")

#Application starter
if __name__ == "__main__":
    Start_time = time.time()
    main()
    EndTime = time.time()

    print("Time required to execute : %s "%(EndTime-Start_time))