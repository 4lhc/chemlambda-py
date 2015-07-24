# -*- coding: utf-8 -*-
#
#  chemlambda.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Thu 23 Jul 2015 15:15:57 IST
#  ver    :

# Define wrapper functions

# TODO: generate_output(start, [[step] end])
# TODO: create_mol_file(45)

#from chemlambda import validator
from chemlambda import molparser as mp
from chemlambda import data
from chemlambda import moves
from chemlambda import topology
from chemlambda import settings


counter = data.Counter()
dicts = data.ChemlambdaDicts()

dict_atoms = dicts.dict_atoms
dict_ports = dicts.dict_ports
moves_list = dicts.moves_list


################################################################################
# testing #
hl = '-'
vl = '│'


def print_dict_atoms(dict_atoms, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
    head = " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>30} {}".format(
            'key', vl, 'uid', vl, 'atom', vl, 'lno', vl, 'targets', vl)
    print(hl*head.__len__())
    print(head)
    print(hl*head.__len__())
    for k, i in dict_atoms.items():
        d = i.__dict__
        uid = d['uid']
        lno = d['lno']
        if not lno:
            lno = '---'
        atom = d['atom']
        targets = ', '.join([p.uid for p in d['targets']])
        print(" {:<10} {} {:<10} {} {:<10} {} {:^10} {} {:>30} {}".format(
            k, vl, uid, vl, atom, vl, lno, vl, targets, vl))

    print(hl*head.__len__())


def print_dict_ports(dict_ports, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
    head = " {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format(
            'key', vl, 'uid', vl, 'atom', vl,
            'parent', vl, 'port_name', vl, 'targets', vl)

    print(hl*head.__len__())
    print(head)
    print(hl*head.__len__())
    for k, i in dict_ports.items():
        d = i.__dict__
        uid = d['uid']
        atom = d['atom']
        parent = d['parent_atom'].uid
        port_name = d['port_name']
        targets = ', '.join([p.uid for p in d['targets']])
        print(" {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}"
              .format(k, vl, uid, vl, atom, vl,
                      parent, vl, port_name, vl, targets, vl))

    print(hl*head.__len__())
################################################################################


def validate_mol_file(mol_file, ignore_errors=True):
    """
    print errors present in the mol file.
    exits if ignore_errors=false, else return a list of valid lines
    """
    print('test')


def intialise(mol_file):
    """
    Read mol file and generate initial configuration of atoms ports and their
    links
    """
    d_a, d_p = mp._read_mol_file(mol_file)

    dict_atoms.update(d_a)
    dict_ports.update(d_p)

    mp._find_matched(dict_ports)
    mp._add_frin_frout(dict_atoms, dict_ports)
    # clear generic port_names
    moves.Moves._delete_attr(dict_ports, 'port_name')

    counter.atom_count = list(dict_atoms.keys()).__len__()
    counter.port_count = list(dict_ports.keys()).__len__()

    print_dict_atoms(dict_atoms, "Atoms")
    print_dict_ports(dict_ports, "Ports")


def generate_cycle(max_cycles=50):
    """
    Generate cycles up to max_cycles [default 50] or when all moves are
    exhausted
    """
    while counter.cycle_count < max_cycles:
        counter.cycle_count += 1
        M = [moves.Moves(a, counter) for a in dict_atoms.values()
             if a.atom in topology.moves]
        M = [m for m in M if m.valid_move]
        if len(M) == 0:
            break
        for m in M:
            d_a, d_p = m._atoms_to_add()  # creates new atoms on this call
            [dict_atoms.__delitem__(k) for k in m._atoms_to_delete()]
            dict_atoms.update(d_a)
            [dict_ports.__delitem__(k) for k in m._ports_to_delete()]
            dict_ports.update(d_p)

        print(counter.cycle_count)
        dicts._take_snapshot(counter.cycle_count)

        print_dict_atoms(dict_atoms, "Atoms")
        print_dict_ports(dict_ports, "Ports")
        # end of one cycle


def main():
    intialise('mol_files/9_quine.mol')
    generate_cycle(50)
    return 0

if __name__ == '__main__':
    main()
