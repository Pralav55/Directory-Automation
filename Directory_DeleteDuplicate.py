#Importing required libraries
from sys import *
import os
import hashlib
import time

#Function which deletes duplicate files
def DeleteFiles(dict):
    results = list(filter(lambda x: len(x)>1 , dict.values()))

    icnt = 0

    if len(results) > 0:
        for result in results:
            for subresult in result:
                icnt+=1

                if icnt>=2:
                    os.remove(subresult)
            icnt = 0
        print("Duplicate files deleted successfully")
    else:
        print("No duplicate file found")

#Function which reads file and calculate size using md5 algorithm
def hashFile(path,blocksize=1024):
    fd = open(path,'rb')
    hasher = hashlib.md5()
    buf = fd.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = fd.read(blocksize)
    
    fd.close()

    return hasher.hexdigest()

#Function which finds Duplicate files present in the following path
def findDup(path):
    flag = os.path.isabs(path)

    if flag == False:
        path = os.path.abspath(path)
    
    exists = os.path.isdir(path)

    dups = {}

    if exists:
        for dirName, subDirs, fileList in os.walk(path):

            for fileN in fileList:
                path = os.path.join(dirName,fileN)
                file_hash = hashFile(path)

                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
    
    else:
        print("Invalid Path")

#Function which creates files if duplicates found and write all duplicate file path into the file created
def PrintDuplicates(dic,log_dir="DeletedDuplicates"):
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
        log_path = os.path.join(log_dir , "DeletedFiles%s.log" %(time.ctime()))
        
        #Opening the created file in write mode
        f = open(log_path,'w')

        #Writing content into the file
        f.write(seperator+"\n")
        f.write("List of Deleted Duplicate Files : "+time.ctime()+"\n")
        f.write(seperator+"\n")

        icnt = 0

        #Iterating over duplicates
        for res in results:
            for subres in res:
                icnt+=1

                if icnt>=2:
                    f.write("%s\n"%subres)

#Execution starts from main
def main():
    #Displays Header
    print("----------Python Automation to Delete Duplicate files------------")

    print("Application name : "+argv[0])

    #Handling Arguments while compilation
    if(len(argv) != 2):
        print("Error : Invalid number of argument")
        exit()
    
    if(argv[1]=="-h" or argv[1] =="-H"):
        print("This script is used to traverse specific directory and delete duplicate files")
        exit()
    
    if(argv[1] == "-u" or argv[1] == "-U"):
        print("Usage : Application_Name Absolute_Path_of_Directory Extension")
        exit()
    
    #Handling Exception using try except
    try:
        arr = {}
        
        startTime = time.time()
        
        #Calling Function which finds duplicates in the given folder
        arr = findDup(argv[1])

        #Prints all duplicate files on output window
        PrintDuplicates(arr)

        #Deletes all duplicates files permanently 
        DeleteFiles(arr)

        endTime = time.time()

        #Printing the execution time required for the program to delete files
        print('Took %s seconds to evaluate' %(endTime - startTime))
    
    #Handling Exception 
    except ValueError:
        print("Error : Invalid datatype of input")
    
    except Exception as E:
        print("Error : Invalid inputs",E)


#Application Starter
if __name__ == "__main__":
    main()