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
            'parent', vl, 'sources', vl, 'targets', vl)

    print(hl*head.__len__())
    print(head)
    print(hl*head.__len__())
    for k, i in dict_ports.items():
        d = i.__dict__
        uid = d['uid']
        atom = d['atom']
        parent = d['parent_atom'].uid
        port_name = d['port_name']
        sources = ', '.join([p.uid for p in d['sources']])
        targets = ', '.join([p.uid for p in d['targets']])
        print(" {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}"
              .format(k, vl, uid, vl, atom, vl,
                      parent, vl, sources, vl, targets, vl))

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
    Read mol file and generate initial configuration of atoms, ports and their
    links
    """
    dicts._reset()
    counter._reset()

    d_a, d_p = mp._read_mol_file(mol_file)

    dict_atoms.update(d_a)
    dict_ports.update(d_p)

    mp._find_matched(dict_ports)
    mp._add_frin_frout(dict_atoms, dict_ports)
    # clear original port_names
    moves.Moves._delete_attr(dict_ports, 'port_name')

    print_dict_ports(dict_ports, "Ports")

    counter.atom_count = list(dict_atoms.keys()).__len__()
    counter.port_count = list(dict_ports.keys()).__len__()
    dicts._take_snapshot(counter.cycle_count)


def generate_cycle(*args):
    """
    generate_cycle([start, [step]], max=50)
    Generate cycles up to max_cycles [default 50] or when all moves are
    exhausted
    """
    if len(args) == 3:
        start, step, max_c = args
    elif len(args) == 2:
        start, max_c = args
        step = 1
    elif len(args) == 1:
        max_c, = args
        start, step = [0, 1]
    elif len(args) == 0:
        start, step, max_c = [0, 1, 50]
    else:
        start, step, max_c = args[:3]

    # range_list = list(range(start, step, max_c))
    range_list = [i for i in range(start, max_c, step)]

    while counter.cycle_count < max_c:
        print("{:^70}".format(counter.cycle_count))
        counter.cycle_count += 1
        M = [moves.Moves(a, counter) for a in dict_atoms.values()
             if a.atom in topology.moves]
        M = [m._move_update() for m in M if m.valid_move]
        if len(M) == 0:
            break
        M = [m._del_atoms_ports_from_dict(dict_atoms, dict_ports) for m in M]
        M = [m._add_atoms_ports_to_dict(dict_atoms, dict_ports) for m in M]

        print_dict_ports(dict_ports, "Ports")

        if counter.cycle_count in range_list + [max_c]:
            M = [m._move_snapshot() for m in M]
            dicts._take_snapshot(counter.cycle_count)
            dicts.moves_list[counter.cycle_count] = M

        # end of one cycle


def main():
    intialise('mol_files/small.mol')
    generate_cycle(50)
    print(dicts.moves_list[1][0].LP_RP)
    return 0

if __name__ == '__main__':
    main()
