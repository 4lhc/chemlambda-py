# -*- coding: utf-8 -*-

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

import textcolor
import topology
import sys

tc = textcolor.TextColor()


def _print_warn(text, desc="", *args):
    """
    Prints warning text and description of error is specified
    args is a list of tuples for tc.ftext( text, color)
    """
    text += '\n' + '{} '*len(args)
    f_text = [tc.ftext(i, fcol=k) for i, k in args]
    tc.warn(text.format(*f_text))
    print(desc)


def _read_mol_file(mol_file):
    """
    populate list mf
    exit on exception filenotfounderror
    """
    try:
        with open(mol_file, 'r') as f:
            mf = [i.strip() for i in f.read().splitlines()]
        return mf
    except FileNotFoundError:
        tc.error("file not found, {}".format(mol_file))
        sys.exit()


def _ignore_spaces_comments(mf):
    """
    removes lines with whitespaces and comments from the list mf
    """
    invalid_lines = []
    for line in mf:
        if line == '' or line.split()[0][0] == '#':
            invalid_lines.append(line)
    mf = [l for l in mf if l not in invalid_lines]
    return mf


def _is_valid_atom(mf, mol_file, err_okay):
    """
    check if the atom is a valid atom in topology.graph
    returns boolean
    """
    invalid_lines = []
    for line in mf:
        if line.split()[0] not in topology.graph:
            desc = 'Atom {}, is not a valid atom defined in topology.graph'.format(line.split()[0])
            _print_warn("Invalid Atom", desc,
                                        (mol_file, 'mg'),
                                        (str(i+1) + ': ->', 'gr'),
                                        (line, 'wt'))
            invalid_lines.append(line)
    mf = [l for l in mf if l not in invalid_lines]
    if not err_okay and not invalid_lines.__len__ == 0:
        tc.error("Mol file contains errors.\nquitting...")
        sys.exit()
    return mf


def _duplicate_lines(mf, mol_file, err_okay):
    """
    Removes duplicate lines from list mf
    Returns boolean
    """
    invalid_lines = []
    for line in mf:
        dup_lines_list = [(i+1, line)]
        dup_lines_list += [(i+j+2, line2) for j, line2 in enumerate(mf[i+1:])
                if line == line2 and line2 not in invalid_lines]
        if dup_lines_list.__len__() > 1:
            dup_line_num = ', '.join([str(j) for j, k in dup_lines_list])
            invalid_lines += [k for j, k in dup_lines_list[1:]]
            desc = "Duplicate lines will be ignored if ignore_errors set to True"
            _print_warn("Duplicate lines", desc,
                                           (mol_file,'mg'),
                                           (dup_line_num+': ->' ,'gr'),
                                           (line, 'wt'))
    mf = [l for l in mf if l not in invalid_lines]
    if not err_okay and not invalid_lines.__len__ == 0:
        tc.error("Mol file contains errors.\nquitting...")
        sys.exit()
    return mf


def _port_name_error(mf, mol_file, err_okay):
    """
    Check if an atom has two similar named ports
    Returns boolean
    """
    invalid_lines = []
    for line in mf:
        i_ports = line.split()[1:]
        if len(i_ports) != len(set(i_ports)):
            desc = "Similar named ports in single line"
            tc.warn("Port name error", desc,
                    (mol_file, 'mg'),
                    ( str(i+1)+': ->', 'gr'),
                    (line, 'wt'))
            invalid_lines.append(line)
    mf = [l for l in mf if l not in invalid_lines]
    if not err_okay and not invalid_lines.__len__ == 0:
        tc.error("Mol file contains errors.\nquitting...")
        sys.exit()
    return mf


def validate(mol_file, ignore_errors=True):
    """
    calls:
    _read_mol_file
    _ignore_spaces_comments()
    _is_valid_atom()
    _duplicate_lines()
    _port_name_error()

    Returns list of valid lines if ignore_errors=True, else quits on error
    """
    mf = _read_mol_file(mol_file)
    mf = _ignore_spaces_comments(mf)
    mf = _is_valid_atom(mf, mol_file, ignore_errors)
    mf = _duplicate_lines(mf, mol_file, ignore_errors)
    mf = _port_name_error(mf, mol_file, ignore_errors)
    print(mf)


validate('mol_files/1.mol')








#def validatea(mol_file):

    ## check multi ports and port mismatch
    #for i,line in enumerate(mf):
        #atom_i = line.split()[0]
        #graph_i = topology.graph[atom_i]
        #ports_i = line.split()[1:]
        #if len(graph_i) != len(ports_i):
            #tc.warn("Port name error\n{} {} {}\n".format(tc.ftext(mol_file,
                            #fcol='mg'), tc.ftext( str(i+2)+': ->', fcol='gr'), line))
            #print("Atom {} has ports {}, {} given".format(atom_i,
                        #' '.join(graph_i), ' '.join(ports_i)))

        #i_port_bind = {}
        #[i_port_bind.update(k=v) for k,v in zip(ports_i, graph_i)]

        #for p in ports_i:
            #multi_port_names = [(i, line)]
            #for j, line2 in enumerate(mf[i+1:]):
                #atom_j = line2.split()[0]
                #graph_j = topology.graph[atom_j]
                #ports_j = line.split()[1:]
                #if p in ports_j:
                    #multi_port_names.append((j, line2))
            #if len(multi_port_names) > 2:
                ## TODO : make funciton of long warning
                #line_num = ', '.join([str(j) for j, k in multi_port_names])
                #invalid_lines += k for j, k in multi_port_names [2:]]
                #tc.warn("Port name {} appears more than twice\n{} {}\n"
                            #.format(p, tc.ftext(mol_file,
                                        #fcol='mg'), tc.ftext( line_num,
                                        #fcol='gr')))


