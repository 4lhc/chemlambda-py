# TODO: combined dict?? call _deflate _inflate -> snapshot list
class Counter:
    """
    Various (unnecessary) Counters
    """
    def __init__(self):
        self.cycle_count = 0 #intial visualisation = cycle 0
        self.total_move_count = 0
        self.atom_count = 0
        self.port_count = 0

    def update(self, ds):
        #per atom counter
        #per port counter
        self.total_move_count = ds.dict_moves.__len_()


class ChemlambdaDicts:
    """"""
    def __init__(self):
        self.mega_atoms_list = []  # snapshot of atoms everycycle
        self.mega_ports_list = []
        self.moves_list = []
        self.dict_atoms = {}
        self.dict_ports = {}
