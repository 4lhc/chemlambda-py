# TODO _write_to_mol_file()
from chemlambda import topology
from collections import Counter
import random
import string

class ChemCounter:
    """
    Various (unnecessary) Counters
    """
    def __init__(self):
        self._reset()

    def update(self, ds):
        # per atom counter
        # per port counter
        self.total_move_count = ds.dict_moves.__len_()

    def _reset(self):
        self.cycle_count = 0  # intial visualisation = cycle 0
        self.total_move_count = 0
        self.atom_count = 0
        self.port_count = 0
        self.move_count = 0

        # move counts
        self.total_moves_count = Counter({})


class ChemlambdaDicts:
    """"""
    def __init__(self):
        self._reset()

    def _take_snapshot(self, curr_cycle):
        """
        Combines, compress and saves the dicitonary of atoms and ports as a
        snapshot of the current cycle.
        Returns None
        """
        d = self.mega_atoms_list[curr_cycle] = {}
        d.update(self.dict_atoms)
        d.update(self.dict_ports)
        for k, atom in d.items():
            d[k] = atom._deflate()

    def _get_snapshot(self, cycle):
        """
        Retrives combined dict snapshot for cycle
        and inflate it.
        Returns Atom_dict
        """
        d = self.mega_atoms_list[cycle]
        d_new = {}
        for k, atom in d.items():
            d_new[k] = atom._inflate(d)
        return d_new

    def _reset(self):
        """Empties every variables"""
        self.mega_atoms_list = {}  # snapshot of atoms and ports for cycles
        self.moves_list = {}
        self.dict_atoms = {}
        self.dict_ports = {}
        self.atoms_taken = []

    def _write_to_mol_file(self, cycle, file_name):
        """Fetches a cycle snapshot from mega_atoms_list and writes it"""
        used_port_name = set(['abc'])
        def create_pn(used_port_name):
            port_name = 'abc'
            pn_len = 3
            i = 0
            if port_name in used_port_name:
                while port_name not in used_port_name:
                    if i > 10:
                        pn_len += 1
                    port_name = ''.join([random.choice(string.ascii_lowercase)
                                         for i in range(pn_len)])
                    i += 1
            used_port_name.add(port_name)
            return port_name

        pn_dict = {}

        def write_pn(p):
            """write port_name for port p and it's target"""
            return p

# priority low
        lines = []
        d_c = self._get_snapshot(cycle)
        d_p = {k:v for k, v in d_c.item()
                if v.atom in ['mo', 'mi', 'ro', 'ri', 'lo', 'li', 'fo', 'fi'] }
        #for k, v in d_p.items():

        used_port_name.add(port_name)


def _write_to_file(fname, text, mode='at'):
    with open(fname, mode) as f:
        f.write(text)

