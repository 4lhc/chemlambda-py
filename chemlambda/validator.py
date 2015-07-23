# -*- coding: utf-8 -*-
#
#  validator.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Thu 23 Jul 2015 01:53:02 IST
#  ver    :

# validate mol files

# TODO identify >2 portnames
# TODO Duplicate lines
# TODO ignore invalid atoms and comments

from chemlambda import textcolor
from chemlambda import topology
import sys

tc = textcolor.TextColor()


def validate(mol_file):
    try:
        with open(mol_file, 'r') as f:
            mf = [i.strip() for i in f.read().splitlines()]
    except FileNotFoundError:
        tc.error("File not found, {}".format(mol_file))
        sys.exit()

    invalid_lines = []
    multi_port_names = []  # [[(i1, l1), (i2, l2), (i3, l3)],... ]
    all_port_names = [i for j in mf for i in j.split()]

    for i, line in enumerate(mf):
        # ignore whitespaces
        if line == '':
            invalid_lines.append(line)
            continue

        # ignore comments
        if line.split()[0][0] == '#':
            invalid_lines.append(line)
            continue

        # Check valid atom
        if line.split()[0] not in topology.graph:
            tc.warn("Invalid Atom \n{} {} {} \n".format(tc.ftext(mol_file,
                fcol='mg'), tc.ftext(str(i+1) + ': ->' , fcol='gr'), line))
            invalid_lines.append(line)
            continue

        #Duplicate
        dup_lines_list = [(i+1, line)]
        dup_lines_list += [(i+j+2, line2) for j, line2 in enumerate(mf[i+1:])
                if line == line2 and line2 not in invalid_lines]
        if dup_lines_list.__len__() > 1:
            dup_line_num = ', '.join([str(j) for j, k in dup_lines_list])
            invalid_lines += [ k for j, k in dup_lines_list[1:]]
            tc.warn("Duplicate lines \n{} {} {} \n".format(tc.ftext(mol_file,
                fcol='mg'), tc.ftext(dup_line_num+': ->' , fcol='gr'), line))
            continue

        # Portnaming error eg: L a1 a1 c
        i_ports = line.split()[1:]
        if len(i_ports) != len(set(i_ports)):
            tc.warn("Port name error\n{} {} {}\n".format(tc.ftext(mol_file,
                fcol='mg'), tc.ftext( str(i+1)+': ->', fcol='gr'), line))
            invalid_lines.append(line)



    mf = [l for l in mf if l not in invalid_lines]

    # check multi ports and port mismatch
    for i,line in enumerate(mf):
        atom_i = line.split()[0]
        graph_i = topology.graph[atom_i]
        ports_i = line.split()[1:]
        if len(graph_i) != len(ports_i):
            tc.warn("Port name error\n{} {} {}\n".format(tc.ftext(mol_file,
                            fcol='mg'), tc.ftext( str(i+2)+': ->', fcol='gr'), line))
            print("Atom {} has ports {}, {} given".format(atom_i,
                        ' '.join(graph_i), ' '.join(ports_i)))

        i_port_bind = {}
        [i_port_bind.update(k=v) for k,v in zip(ports_i, graph_i)]

        for p in ports_i:
            multi_port_names = [(i, line)]
            for j, line2 in enumerate(mf[i+1:]):
                atom_j = line2.split()[0]
                graph_j = topology.graph[atom_j]
                ports_j = line.split()[1:]
                if p in ports_j:
                    multi_port_names.append((j, line2))
            if len(multi_port_names) > 2:
                # TODO : make funciton of long warning
                line_num = ', '.join([str(j) for j, k in multi_port_names])
                invalid_lines += [ k for j, k in multi_port_names [2:]]
                tc.warn("Port name {} appears more than twice\n{} {}\n"
                            .format(p, tc.ftext(mol_file,
                                        fcol='mg'), tc.ftext( line_num,
                                        fcol='gr')))


validate('mol_files/1.mol')
