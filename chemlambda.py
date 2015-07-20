
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


parse_data = mp.parseMolfile(mol_file)

for i, mol in enumerate(parse_data):
    uid = mol['atom'] + "_" + str(i)
    
    atom_list = topology.graph[mol['atom']]
    port_list = mol['ports']
    
    dict_atoms[uid] = atoms.Atom(uid=uid, atom=mol['atom'])
    dict_atoms[uid].targets = [] ###???

    for j, (atom, port_name) in enumerate(zip(atom_list, port_list)):
        puid = uid + "_" + str(j)
        dict_ports[puid] = atoms.Port( uid=puid, atom=atom, port_name=port_name)
        dict_atoms[uid].targets.append(puid)
    

print(dict_atoms['L_1'].__dict__)
print(dict_ports['L_1_0'].__dict__)
