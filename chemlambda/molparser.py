
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  molparser.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 18:09:22 IST
#  ver    : 
#
# A python port of chemlambda-gui by chorasimilarity (Marius Buliga, http://chorasimilarity.wordpress.com/)
#

# Parse mol files based on rules from topology.py

def parse_mol_file(mol_file):
    """
    parse_mol_file(mol_file | list_of_line)
    if argument is a string it's treated as a file name and file is read
    if argument is a list, it's treated as a list of lines
    return [{ 'atom': 'L', 'ports': [a, b, c]}, ...]
    """
    mols = []

    if mol_file.__class__ == str:
        try:
            with open(mol_file, 'r') as f:
                mf = f.read().splitlines()    
        except FileNotFoundError:
            print("{} could not be read".format(mol_id))
            return None
    else:
        mf = mol_file
        
    all_names = [ i for j in mf for i in j.split() ]
    for i, line in enumerate(mf):
        try:
            l = line.split()
            counter = [ all_names.count(i) for i in l[1:] ]
            if max(counter) > 2:
                print("\033[91mError:\033[0m in mol file\nline \033[92m{}\033[0m:{}"
                        .format(i+1, line))
            else:
                mols.append({ "atom": l[0], "ports": l[1:], "lno":i+1})
        except IndexError:
            #ignore empty lines
            pass
        except ValueError:
            #ignore error raised by max() at empty lines
            pass
    return mols

