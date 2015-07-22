
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

from chemlambda import topology
from chemlambda import atoms 

def _parse_mol_file(mol_file):
    """
    _parse_mol_file(mol_file | list_of_line)
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
        
    all_names = [i for j in mf for i in j.split()]
    for i, line in enumerate(mf):
        try:
            l = line.split()
            counter = [all_names.count(i) for i in l[1:]]
            if max(counter) > 2 or l[0] not in topology.graph:
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

def _read_mol_file(mol_file, atom_count=0):  
    """
        read_mol_file( str or list of lines, count)
        Reads the mol file, parses it and populates dict_atoms and dict_ports
    """
    parse_data = _parse_mol_file(mol_file)

    ac = atom_count

    dict_ports = {}
    dict_atoms = {}

    for i, mol in enumerate(parse_data):
        uid = mol['atom'] + "_" + str(ac + i)
        
        atom_list = topology.graph[mol['atom']]
        port_list = mol['ports']
        
        dict_atoms[uid] = atoms.Atom(uid=uid, atom=mol['atom'], lno=mol['lno'])
        dict_atoms[uid].targets = [] ###???

        for j, (atom, port_name) in enumerate(zip(atom_list, port_list)):
            puid = uid + "_" + str(j)
            dict_ports[puid] = atoms.Port( uid=puid, atom=atom,
                    port_name=port_name, parent_atom=dict_atoms[uid])
            index = dict_atoms[uid]._insert_into(dict_ports[puid])
            dict_atoms[uid].targets.insert(index, dict_ports[puid])
    return ( dict_atoms, dict_ports)


def _find_matched(dict_ports):
    """
    """
    L = list(dict_ports.values())
    [atoms.Port._set_matched_port(p1, p2) 
            for (i, p1) in enumerate(L) 
            for p2 in L[i+1:] 
            if p1.port_name == p2.port_name]


def _add_frin_frout(dict_atoms, dict_ports):
    """
    Create FROUT, FRIN and their ports
    """
    L = list(dict_ports.values())
    i = list(dict_atoms.keys()).__len__()

    for p in L:
        at = (["FRIN", "fo"], ["FROUT", "fi"])[p._is_out_port()] #tuple[0] or tuple[1]
        if p.free == 1:
            #free port exist
            uid = at[0] +"_" + str(i)
            puid = uid + "_0"
            dict_atoms[uid] = atoms.Atom( uid=uid, atom=at[0], targets = [])
            dict_ports[puid] = atoms.Port( uid=puid, atom=at[1],
                     parent_atom=dict_atoms[uid], free=0)
            dict_atoms[uid].targets.append(dict_ports[puid]) #adding targets
            
            if p._is_out_port():
                p._add_target(dict_ports[puid])
            else:
                dict_ports[puid]._add_target(p)
            p.free = 0
            i += 1
