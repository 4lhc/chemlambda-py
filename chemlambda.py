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
# A python port of chemlambda-gui by chorasimilarity (Marius Buliga,
# http://chorasimilarity.wordpress.com/)
#


from chemlambda import molparser as mp
from chemlambda import data
from chemlambda import moves
from chemlambda import topology
from chemlambda import settings


# testing ##
hl = '-'
vl = '│'


def print_dict_atoms(dict_atoms, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
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
        targets = ', '.join([p.uid for p in d['targets']])
        print(" {:<10} {} {:<10} {} {:^10} {} {:>30} {}".format(uid, vl, atom,
            vl, lno, vl, targets, vl))

    print(hl*head.__len__())



def print_dict_ports(dict_ports, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
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
        targets = ', '.join([p.uid for p in d['targets']])
        print( " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format(uid, vl, atom, vl,
        parent, vl, port_name, vl, targets, vl))

    print(hl*head.__len__())


counter = data.Counter()
dicts = data.ChemlambdaDicts()

mol_file = 'mol_files/1.mol'
#mol_file = 'mol_files/test.mol'

dict_atoms = dicts.dict_atoms  #dict of Atom objects { uid: Atom obj }
dict_ports = dicts.dict_ports
dict_moves = dicts.dict_moves


d_a, d_p = mp._read_mol_file(mol_file)

dict_atoms.update(d_a)
dict_ports.update(d_p)

mp._find_matched(dict_ports)
mp._add_frin_frout(dict_atoms, dict_ports)

print_dict_atoms(dict_atoms, "Atoms")
print_dict_ports(dict_ports, "Ports")

dicts.mega_atoms_dict.append(dict_atoms)
dicts.mega_ports_dict.append(dict_ports)

counter.atom_count = list(dict_atoms.keys()).__len__()
counter.port_count = list(dict_ports.keys()).__len__()

st = '\033[91;1m{:^70}\n{:^70}\n{:^70}\033[0m'
#Start cycle
while counter.cycle_count < settings.MAX_CYCLES:
    print(st.format('-'*50, 'Cycle: ' + str(counter.cycle_count), '-'*50))
    M = [moves.Moves(a, counter) for a in dict_atoms.values() if a.atom in topology.moves]
    M = [m for m in M if m.valid_move]
    if len(M) == 0: break
    for m in M:
        d_a, d_p = m._atoms_to_add() #Moves class creates new nodes on this method call
        print_dict_atoms(d_a, "Move: " + m.move_name)
        print_dict_ports(d_p)
        [dict_atoms.__delitem__(k) for k in m._atoms_to_delete()]
        dict_atoms.update(d_a)
        [dict_ports.__delitem__(k) for k in m._ports_to_delete()]
        dict_ports.update(d_p)

    dicts.mega_atoms_dict.append(dict_atoms)
    dicts.mega_ports_dict.append(dict_ports)
    counter.cycle_count += 1 #end of one cycle

print(st.format('-'*11, 'END', '-'*11))
print_dict_atoms(dict_atoms, "Atoms")
print_dict_ports(dict_ports, "Ports")
