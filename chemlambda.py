
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

def freeInOut():
    """
    Create FROUT, FRIN and thier ports
    """

def findMatched():
    """
    find LP from matched ports
    """
    l = list(dict_ports.values())
    matched_ports = [ (p1.setMatchedport(p2)) 
            for (i, p1) in enumerate(l) 
            for p2 in l[i+1:] 
            if p1.port_name == p2.port_name]


def readMolfile(mol_file):
    """
        readMolfile( str or list of lines)
        Reads the mol file, parses it and populates dict_atoms and dict_ports
    """
    parse_data = mp.parseMolfile(mol_file)

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

    
    
readMolfile(mol_file)
print(dict_atoms['L_0'].__dict__)
print(dict_ports['L_0_0'].__dict__)
#print(dict_atoms)
