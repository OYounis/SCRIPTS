#!/usr/bin/python

#import argparse
import os

def getFileList(dir = '.'):
    # get the list of directories
    dirs = os.listdir(dir)
    
    # make a list to save file paths
    file_names = list()
    
    # print all directory names
    for dir_name in dirs:
        if (dir_name.startswith(".")): continue    #skip directories like .git, .gitignore, etc.
        
        abs_path = os.path.join(dir, dir_name)
        #print(abs_path)
        if os.path.isdir(abs_path):
            #getFileList(abs_path)
            file_names = file_names + getFileList(abs_path)
        else: 
            file_names.append(abs_path)
    return file_names

#def getFlist():
                #for level1_item in level1:
            #    if os.path.isdir(level1_item) == False:
            #        item_path = dir_name + "/" + level1_item +"\n"
            #        if "pkg" in item_path: file_names.insert(0, item_path)
            #        else: file_names.append(item_path)
                
            #with open(dir_name + ".f", "w") as f_handle:
            #    f_handle.writelines(file_names)
            #    file_names = []


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #args = parser.parse_args()
    files = getFileList()
    for file in files:
        print(file)