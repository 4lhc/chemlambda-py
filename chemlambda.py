
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


from chemlambda import molparser as mp
from chemlambda import data
from chemlambda import moves


################################################################################
# 
hl = '-'
vl = '│'
def print_dict_atoms():
    head = " {:<10} {} {:<10} {} {:<10} {} {:>30} {}".format('uid', vl, 'atom', vl, 
            'lno', vl, 'targets', vl)
    print(hl*head.__len__())
    print(head)
    print(hl*head.__len__())
    for i in list(dict_atoms.values()):
        d = i.__dict__
        uid = d['uid']
        lno = d['lno']
        if not lno: lno = '---'
        atom = d['atom']
        targets = ', '.join([ p.uid for p in d['targets'] ])
        print( " {:<10} {} {:<10} {} {:^10} {} {:>30} {}".format(uid, vl, atom,
            vl, lno, vl, targets, vl))

    print(hl*head.__len__())



def print_dict_ports():
    head = " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format('uid', vl, 'atom', vl,
            'parent', vl, 'port_name', vl, 'targets', vl)

    print(hl*head.__len__())
    print(head)
    print(hl*head.__len__())
    for i in list(dict_ports.values()):
        d = i.__dict__
        uid = d['uid']
        atom = d['atom']
        parent = d['parent_atom'].uid
        port_name = d['port_name']
        targets = ', '.join([ p.uid for p in d['targets'] ])
        print( " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format(uid, vl, atom, vl,
        parent, vl, port_name, vl, targets, vl))

    print(hl*head.__len__())
################################################################################


counter = data.Counter()
dicts = data.ChemlambdaDicts()

mol_file = 'mol_files/1.mol'
mol_file = 'mol_files/test.mol'

dict_atoms = dicts.dict_atoms  #dict of Atom objects { uid: Atom obj }
dict_ports = dicts.dict_ports
dict_moves = dicts.dict_moves


c = list(dict_atoms.keys()).__len__()

d_a, d_p = mp._read_mol_file(mol_file, c)

dict_atoms.update(d_a)
dict_ports.update(d_p)

mp._find_matched(dict_ports)
mp._add_frin_frout(dict_atoms, dict_ports)

print_dict_atoms()
print_dict_ports()
