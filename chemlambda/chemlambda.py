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
from chemlambda import textcolor

tc = textcolor.TextColor()


counter = data.Counter()
dicts = data.ChemlambdaDicts()



################################################################################
# testing #
hl = '-'
vl = '│'
vl = '|'


def print_dict_atoms(dict_atoms, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
    head = "{:<10} {} {:<10} {} {:<10} {} {:>30} {}".format(
             'uid', vl, 'atom', vl, 'lno', vl, 'targets', vl)
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
        print("{:<10} {} {:<10} {} {:^10} {} {:>30} {}".format(
            uid, vl, atom, vl, lno, vl, targets, vl))

    print(hl*head.__len__())


def print_dict_ports(dict_ports, title=''):
    print("\033[92;1m{:^70}\033[0m".format(title))
    head = "{:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}".format(
            'uid', vl, 'atom', vl,
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
        print("{:<10} {} {:<10} {} {:<10} {} {:<10} {} {:>20} {}"
              .format(uid, vl, atom, vl,
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

    dicts.dict_atoms.update(d_a)
    dicts.dict_ports.update(d_p)

    mp._find_matched(dicts.dict_ports)
    mp._add_frin_frout(dicts.dict_atoms, dicts.dict_ports)
    # clear original port_names
    moves.Moves._delete_attr(dicts.dict_ports, 'port_name')

    # test output##############################
    hr = tc.ftext('\n' + "-"*80 + '\n', fcol='rd')
    cc = tc.ftext("\nIntial Config: " + str(counter.cycle_count), fcol='rd')
    print(hr + "{:^80}".format(cc) + hr)
    print_dict_atoms(dicts.dict_atoms, "Atoms")
    print_dict_ports(dicts.dict_ports, "Ports")

    counter.atom_count = list(dicts.dict_atoms.keys()).__len__()
    counter.port_count = list(dicts.dict_ports.keys()).__len__()
    dicts._take_snapshot(counter.cycle_count)


def generate_cycle(deterministic=True, *args):
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
        counter.cycle_count += 1
        atoms_taken = []  # list to keep track of used atoms. Reset every cycle

        M = [moves.Moves(a, counter)
             for a in dicts.dict_atoms.values()
             if a.atom in topology.moves]

        if deterministic:
            # If deterministic, sort according to weight
            M = sorted(M, key=lambda m: m.weight, reverse=True)
            M = [m for m in M if m.move_name != '']
            print([(m.weight, m.move_name) for m in M])
            # perfect! was looking for an apt usage of lambda :)

        M = [m for m in M if m._is_valid(atoms_taken)]

        if len(M) == 0:  # no moves
            break

        M = [m._add_atoms_ports_to_dict(dicts.dict_atoms, dicts.dict_ports)
             for m in M]
        M = [m._del_atoms_ports_from_dict(dicts.dict_atoms, dicts.dict_ports)
             for m in M]

        # test output##############################
        [print(m.lp_rp) for m in M]
        hr = tc.ftext('\n' + "-"*80 + '\n', fcol='rd')
        cc = tc.ftext("Cycle: " + str(counter.cycle_count), fcol='rd')
        print(hr + "{:^80}".format(cc) + hr)
        print_dict_atoms(dicts.dict_atoms, "Atoms")
        print_dict_ports(dicts.dict_ports, "Ports")
        # ##############################

        if counter.cycle_count in range_list + [max_c]:
            M = [m._move_snapshot() for m in M]
            dicts._take_snapshot(counter.cycle_count)
            dicts.moves_list[counter.cycle_count] = M
        # end of one cycle


def main():
    intialise('mol_files/small.mol')
    generate_cycle(5)
    return 0

if __name__ == '__main__':
    main()
