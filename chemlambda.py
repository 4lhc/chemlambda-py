
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  chemlambda.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 12:34:38 IST
#  ver    : 
#
# A python port of chemlambda-gui by chorasimilarity (Marius Buliga, http://chorasimilarity.wordpress.com/)
#


from chemlambda import topology
from chemlambda import molparser as mp
from chemlambda import atoms 

mol_file = 'mol_files/1.mol'
mol_file = 'mol_files/test.mol'

dict_atoms = {}  #dict of Atom objects { uid: Atom obj }
dict_ports = {}

matched_ports = []


def add_frin_frout():
    """
    Create FROUT, FRIN and their ports
    """
    L = list(dict_ports.values())
    i = list(dict_atoms.keys()).__len__()

    d = { 'i': [ "FRIN", "fo" ], 'o': [ "FROUT", "fi"] }

    for p in L:
        at = d[p.atom[-1]]
        if p.free == 1:
            #free port exist
            uid = at[0] +"_" + str(i)
            puid = uid + "_0"
            dict_atoms[uid] = atoms.Atom( uid=uid, atom=at[0], targets = [])
            dict_ports[puid] = atoms.Port( uid=puid, atom=at[1],
                     parent_atom=dict_atoms[uid], free=0)
            dict_atoms[uid].targets.append(dict_ports[puid]) #adding targets
            p.add_target(dict_ports[puid])
            p.free = 0
            i += 1


def find_matched():
    """
    find LP from matched ports
    """
    L = list(dict_ports.values())
    matched_ports.extend((p1.set_matched_port(p2) 
            for (i, p1) in enumerate(L) 
            for p2 in L[i+1:] 
            if p1.port_name == p2.port_name))


def read_mol_file(mol_file):
    """
        read_mol_file( str or list of lines)
        Reads the mol file, parses it and populates dict_atoms and dict_ports
    """
    parse_data = mp.parse_mol_file(mol_file)

    for i, mol in enumerate(parse_data):
        uid = mol['atom'] + "_" + str(i)
        
        atom_list = topology.graph[mol['atom']]
        port_list = mol['ports']
        
        dict_atoms[uid] = atoms.Atom(uid=uid, atom=mol['atom'], lno=mol['lno'])
        dict_atoms[uid].targets = [] ###???

        for j, (atom, port_name) in enumerate(zip(atom_list, port_list)):
            puid = uid + "_" + str(j)
            dict_ports[puid] = atoms.Port( uid=puid, atom=atom,
                    port_name=port_name, parent_atom=dict_atoms[uid])
            dict_atoms[uid].targets.append(dict_ports[puid])


read_mol_file(mol_file)
find_matched()
add_frin_frout()


hl = '-'
vl = '│'
print(hl*71)
print( " {:<10} {} {:<10} {} {:<10} {} {:>30} {}".format('uid', vl, 'atom', vl, 'lno', vl, 'targets', vl))
print(hl*71)
for i in list(dict_atoms.values()):
    d = i.__dict__
    uid = d['uid']
    lno = d['lno']
    if not lno: lno = '---'
    atom = d['atom']
    targets = ', '.join([ p.uid for p in d['targets'] ])
    print( " {:<10} {} {:<10} {} {:^10} {} {:>30} {}".format(uid, vl, atom,
        vl, lno, vl, targets, vl))

print(hl*71,'\n')

print(hl*74)
print( " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format('uid', vl, 'atom', vl,
    'parent', vl, 'port_name', vl, 'targets', vl))
print(hl*74)
for i in list(dict_ports.values()):
    d = i.__dict__
    uid = d['uid']
    atom = d['atom']
    parent = d['parent_atom'].uid
    port_name = d['port_name']
    targets = ', '.join([ p.uid for p in d['targets'] ])
    print( " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format(uid, vl, atom, vl,
    parent, vl, port_name, vl, targets, vl))

print(hl*74)

matched_ports = set(matched_ports)
try:
    matched_ports.remove(None)
except KeyError:
    pass
print([ (a.uid, b.uid) for (a, b) in matched_ports])
