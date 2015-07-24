# TODO: combined dict?? call _deflate _inflate -> snapshot list
class Counter:
    """
    Various (unnecessary) Counters
    """
    def __init__(self):
        self.cycle_count = 0  # intial visualisation = cycle 0
        self.total_move_count = 0
        self.atom_count = 0
        self.port_count = 0

    def update(self, ds):
        # per atom counter
        # per port counter
        self.total_move_count = ds.dict_moves.__len_()


class ChemlambdaDicts:
    """"""
    def __init__(self):
        self.mega_atoms_list = {}  # snapshot of atoms and ports for cycles
        self.moves_list = []
        self.dict_atoms = {}
        self.dict_ports = {}

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
