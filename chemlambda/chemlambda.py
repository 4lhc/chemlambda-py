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

    #tmp_dict = { k:deepcopy(v) for k,v in dict_atoms.items() }
    #dicts.mega_atoms_list.append(tmp_dict)
    #tmp_dict = { k:deepcopy(v) for k,v in dict_ports.items() }
    #dicts.mega_ports_list.append(tmp_dict)

    counter.atom_count = list(dict_atoms.keys()).__len__()
    counter.port_count = list(dict_ports.keys()).__len__()


def generate_cycle(max_cycles=50):
    """
    Generate cycles up to max_cycles [default 50] or when all moves are
    exhausted
    """
    while counter.cycle_count < max_cycles:
        M = [moves.Moves(a, counter) for a in dict_atoms.values() if a.atom in topology.moves]
        M = [m for m in M if m.valid_move]
        if len(M) == 0: break
        for m in M:
            d_a, d_p = m._atoms_to_add() #Moves class creates new nodes on this method call
            [dict_atoms.__delitem__(k) for k in m._atoms_to_delete()]
            dict_atoms.update(d_a)
            [dict_ports.__delitem__(k) for k in m._ports_to_delete()]
            dict_ports.update(d_p)

        #tmp_dict = { k:deepcopy(v) for k,v in dict_atoms.items() }
        #dicts.mega_atoms_list.append(tmp_dict)
        #tmp_dict = { k:deepcopy(v) for k,v in dict_ports.items() }
        #print(tmp_dict.__len__())
        #dicts.mega_ports_list.append(tmp_dict)
        #dicts.moves_list.append(deepcopy(M))

        counter.cycle_count += 1 #end of one cycle


def main():
    return 0

if __name__ == '__main__':
    main()
