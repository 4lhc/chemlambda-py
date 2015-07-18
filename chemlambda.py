
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  chemlambda.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 12:34:38 IST
#  ver    : 

from chemlambda import topology
from chemlambda import molparser as mp


rules = topology.graph
mol_file = 'mol_files/test.mol'

try:
    with open(mol_file, 'r') as f:
        st = f.read().splitlines()
    print(mp.molParser(st, rules))
except FileNotFoundError:
        print("File not found")
