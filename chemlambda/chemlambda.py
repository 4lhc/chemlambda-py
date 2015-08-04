# -*- coding: utf-8 -*-
#
#  chemlambda.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Thu 23 Jul 2015 15:15:57 IST
#  ver    :

# This file is a hardlink of chemlambda/chemlambda.py, this exists at it's
# current location for testing purpose.

# Define wrapper functions

# TODO: generate_output(start, [[step] end])
# TODO: create_mol_file(45)


# from chemlambda import validator
from chemlambda import molparser as mp
from chemlambda import data
from chemlambda import moves
from chemlambda import topology
from chemlambda import settings
from chemlambda import textformat
from collections import Counter

tc = textformat.TextFormat()
tf = textformat.TextOutput()


counter = data.ChemCounter()
dicts = data.ChemlambdaDicts()


def validate_mol_file(mol_file, ignore_errors=True):
    """
    print errors present in the mol file.
    exits if ignore_errors=false, else return a list of valid lines
    """
    print('test')


def intialise(mol_file, create_d3=False, html_out_file='out.html'):
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
    if settings.verbose:
        hr = tc.ftext("-"*79, fcol='mg')
        cc = tc.ftext("Intial Config: " + str(counter.cycle_count), fcol='cy')
        print(hr)
        print("{:^80}".format(cc))
        print(hr)
        out_file = ''  # print output to file if ut_file non empty
        # Tip: pipe output to '|egrep --color "FROUT|$"' to highlight all FROUTs
        if settings.show_tables:
            tf._output_tables(dicts.dict_atoms, file_name=out_file)
            tf._output_tables(dicts.dict_ports, title="Ports", kind='port',
                              file_name=out_file)

    if create_d3:
        dicts._take_snapshot(counter.cycle_count)
        data._d3_output(dicts.mega_atoms_list[counter.cycle_count],
                        html_out_file)

    counter.atom_count = list(dicts.dict_atoms.keys()).__len__()
    counter.port_count = list(dicts.dict_ports.keys()).__len__()
    dicts._take_snapshot(counter.cycle_count)


def generate_cycle(start=0, step=1, max_c=50, jsonAt=50, out_file='',
                   html_out_file='out.html'):
    """
    generate_cycle([start, [step]], max=50)
    Generate cycles up to max_cycles [default 50] or when all moves are
    exhausted
    """

    # range_list = list(range(start, step, max_c))
    range_list = [i for i in range(start, max_c, step)]

    while counter.cycle_count < max_c:
        counter.cycle_count += 1
        atoms_taken = []  # list to keep track of used atoms. Reset every cycle

        M = [moves.Moves(a, counter)
             for a in dicts.dict_atoms.values()
             if a.atom in topology.moves]

        if settings.deterministic:
            # If deterministic, sort according to weight
            M = sorted(M, key=lambda m: m.weight, reverse=True)
            # perfect! was looking for an apt usage of lambda :)
            M = [m for m in M if m.move_name != '']

        M = [m for m in M if m._is_valid(atoms_taken)]
        M = [m._add_atoms_ports_to_dict(dicts.dict_atoms, dicts.dict_ports)
             for m in M]
        M = [m._del_atoms_ports_from_dict(dicts.dict_atoms, dicts.dict_ports)
             for m in M]


        if len(M) == 0:  # no moves
            break

        if settings.verbose:
            hr = tc.ftext("-"*79, fcol='mg')
            cc = tc.ftext(" Cycle: " + str(counter.cycle_count), fcol='cy')
            aa = tc.ftext(" Atoms: " + str(len(dicts.dict_atoms)), fcol='cy')
            pp = tc.ftext(" Ports: " + str(len(dicts.dict_ports)), fcol='cy')
            mm = tc.ftext(" Moves: " + str(len(M)), fcol='cy')

            print(hr)
            print("\t{:^20}\t{:^20}\t{:^20}\t{:^20}".format(cc, aa, pp, mm))
            print(hr)

            if settings.show_atom_count:
                c_dict = Counter([v.atom for k, v in dicts.dict_atoms.items()])
                c_atoms = ' '.join(['{}:{}'.format(k, v)
                                    for k, v in c_dict.items()])
                print('Atoms Count:  {:<80}'.format(c_atoms))
            if settings.show_move_count:
                m_list = [m.move_name for m in M]
                m_dict = Counter(m_list)
                counter.total_moves_count += m_dict
                m_count = '  '.join(['{}:{}'.format(k, v)
                                    for k, v in m_dict.items()])
                print('Moves Count:  {:<80}'.format(m_count))
            if settings.show_moves:
                [print(m.lp_rp) for m in M]
            if settings.show_tables:
                tf._output_tables(dicts.dict_atoms, file_name=out_file)
                tf._output_tables(dicts.dict_ports, title="Ports", kind='port',
                                  file_name=out_file)

        if counter.cycle_count in range_list + [max_c] + [jsonAt]:
            M = [m._move_snapshot() for m in M]
            dicts._take_snapshot(counter.cycle_count)
            dicts.moves_list[counter.cycle_count] = M
            print(counter.cycle_count)
            if counter.cycle_count == jsonAt:
                data._d3_output(dicts.mega_atoms_list[counter.cycle_count],
                                html_out_file)
        # end of cycle

    if settings.verbose:
        # print total move count
        tm = tc.ftext("Total Moves: ", fcol='cy')
        print(hr)
        print('{:^80}'.format(tm))
        print(hr)
        m_count = '  '.join(['{}:{}'.format(k, v)
                            for k, v in counter.total_moves_count.items()])
        print(m_count)


def main():
    # The current version of chemlambda-py doesn't work like the original
    # chemlambda, it can produce a per-cycle output right now, but there's no
    # rewrites as in the original version.

    # mol files from mol_files/
    # mol_file = 'mol_files/lisfact_2_mod.mol'
    mol_file = 'mol_files/fibo.mol'
    html_out_file = mol_file.replace('.mol', '.html')

    # set create_d3 parameter to True to create d3 visualisation of the intial
    # molecule, that is cycle zero. The output html will be created inside the
    # mol_files directory. The verbosity of stdout output can be set in
    # settings.py
    intialise(mol_file, create_d3=False, html_out_file=html_out_file)

    # set jsonAt parameter to the cycle, which's output as d3 graph is
    # required.
    generate_cycle(start=50, step=1, max_c=70, jsonAt=56, out_file='',
                   html_out_file=html_out_file)
    return 0

if __name__ == '__main__':
    main()
