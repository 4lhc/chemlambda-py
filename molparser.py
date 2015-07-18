
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  molparser.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 18:09:22 IST
#  ver    : 

# Parse mol files based on rules from topology.py

import topology

def addTargets(d, mid):
    """ addTargets(mol_dict, last_mol_id)
        add targets for ports
        Create FRIN, FROUT and their ports
    """
    #create a list of ports
    mol_ids = [ mol for mol in list(d.keys()) if 'name' in d[mol]]
    #ports that will find mathces
    matched_ports = [] 
    for i, mol in enumerate(mol_ids):
        for t_mol in mol_ids[i+1:]:
            if d[mol]['name'] == d[t_mol]['name']:
                d[mol]['target'].append(t_mol)
                matched_ports.append(mol)
                matched_ports.append(t_mol)

    #update mol_ids, remove matched_ports
    mol_ids = [ mol for mol in mol_ids if mol not in matched_ports ]
    #FRIN, FROUT and ports + targets
    for mol in mol_ids:
        port_id = str(mid) + "_0"
        FR_id = str(mid)
        if d[mol]['type'][-1] == 'i':
            d[FR_id] = { 'type': "FRIN" , 'target': []}
            d[port_id] = { 'type': 'fo', 'target': [ FR_id, mol] }
        else:
            d[FR_id] = { 'type': "FROUT" , 'target': []}
            d[port_id] = { 'type': 'fi', 'target': [ FR_id, mol] }
        mid += 1

    return d






def molParser(mol_file):
    """ molParser(mol_file)
        Parses mol files line by line based on rules from topology.py
    """
    rules = topology.graph
    mols = {}
    mol_id = 0
    try:
        with open(mol_file, 'r') as f:
            for line in f:
                try:
                    l = line.split()
                    #l[0] -- main mol type
                    #rules[l[0]] -- (list) graph specific rules from topology
                    mols[str(mol_id)] = { 'type': l[0], 'target': [] }
                    for i, val in enumerate(rules[l[0]]):
                        mols[str(mol_id)]['target'].append(str(mol_id) + "_" + str(i))
                        port_id = str(mol_id) + "_" + str(i)
                        mols[port_id] = { 'type': val,
                                'name': l[i+1],
                                'target': []}

                    mol_id += 1
                except IndexError:
                    print("....................IndexError")
                    pass
    except FileNotFoundError:
        print("File not found")
    #return mols
    return  addTargets(mols, mol_id)





