#!/usr/bin/python

import argparse
import re
import pathlib
import os

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

class _TreeGenerator:
    def __init__(self, root_dir, dir_only, include, exclude):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._include = include
        self._exclude = exclude
        self._tree = []

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)
    
    def _tree_body(self, directory, prefix = ''):
        entries = self._prepare_entries(directory)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)
    
    def _prepare_entries(self,directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
        if self._exclude :
            entries = self._filter_entries(self._exclude, list(entries), True)
        if self._include :
            entries = self._filter_entries(self._include, list(entries), False)
        entries = sorted(entries, key = lambda entry: entry.is_file())
        return entries

    def _filter_entries(self, patterns: 'list [str]', entries, exclude: bool) :
        filter = []
        for pattern in patterns :
            filter = [entry for entry in entries if re.search(pattern, entry.name)] 
            print(filter)
        if exclude :
            entries = [entry for entry in entries if (entry not in filter)]
        else :
            entries = [entry for entry in entries if (entry in filter)]
        return entries
    
    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f'{prefix}{connector} {directory.name}{os.sep}')
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory, prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f'{prefix}{connector} {file.name}')

class DirectoryTree:
    def __init__(self, root_dir, dir_only, include = None, exclude = None):
        self._generator = _TreeGenerator(root_dir, dir_only, include, exclude)
        self.tree = []

    def generate(self):
        self.tree = self._generator.build_tree()

    def print(self, tofile = None):
        for entry in self.tree:
            print(entry, file = tofile)

def fList(path, include, exclude) : 
    files = list(path.glob('**/*'))
    filtered = files
    if exclude :
        print(exclude)
        for pattern in exclude :
            print(pattern, files[0].name)
            filter = [entry for entry in files if re.search(pattern, entry.name)] 
        filtered = [entry for entry in files if (entry not in filter)]
    if include :
        for pattern in include :
            filter = [entry for entry in files if re.search(pattern, entry.name)] 
        filtered = [entry for entry in files if (entry in filter)]
    return filtered
    
def fileOps():
    parser = argparse.ArgumentParser(prog = 'fileops', 
                                 description = 'Execute different operations on files and directories.',)
    parser.add_argument('operation', choices = ['dirtree', 'flist'])
    
    parser.add_argument('-p','--path', 
                        default = '.',
                        help = 'Execute the file operation with the specified path\n')
    
    parser.add_argument('-in','--include', 
                        default = None, nargs = '*',
                        help = 'Include the specified extension/directory path in the file opeartion\n')
    
    parser.add_argument('-exc','--exclude',
                        default = None, nargs = '*',
                        help = 'Exclude the specified extension/directory path from the file opeartion\n')
    
    parser.add_argument('-f','--file',
                        action = 'store_true',
                        help = '''Write the output to a file.\n 
                                If no file name is set, fileOps sets the file name to the directory\n''')
    
    parser.add_argument('-d', '--dir',
                        default = False, action = 'store_true',
                        help = 'Directory only output\n')
    
    args = parser.parse_args()
    
    args.path = pathlib.Path(args.path)
    if (args.operation == 'dirtree') : 
        tree = DirectoryTree(args.path, args.dir, args.include, args.exclude)
        tree.generate()
        
        if(args.file):
            filename = args.path.resolve().name + ".tree"
            with open(filename, 'w') as fhandle:
                tree.print(fhandle)
        else : tree.print()
            
    elif (args.operation == 'flist') : 
        files = fList(args.path, args.include, args.exclude)
        if(args.file):
            filename = args.path.resolve().name + ".flist"
            with open(filename, 'w') as fhandle:
                [print(file, file = fhandle) for file in files if file.is_file()]
        else : [print(file) for file in files if file.is_file()]

if __name__ == "__main__":
    fileOps()