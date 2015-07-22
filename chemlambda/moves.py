
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  moves.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sun 19 Jul 2015 13:26:52 IST
#  ver    : 

#'Moves' to be performed
# [https://chorasimilarity.wordpress.com/2015/03/15/the-moves-of-chemlambda-v2-in-mol-format/]


from chemlambda import topology
from chemlambda import atoms
from chemlambda import molparser as mp

class Moves:
    """
    find valid moves
    create required atoms
    """
    def __init__(self, atom1):
        """
            args: Atom objects
            atom1, atom2 are atoms in Left Pattern (LP)
            a, b, c1 are ports of atom1
            d, e, c2 are ports of atom2
            c1 and c2 are ports with the common port_name, ie; c1 and c2 links
            the two atoms
        """
        self.atom1 = atom1
        self.validate_move = self._find_moves()
        self.uid = ''


    def _bind_ports(self):
        """
        set a, b, c1
        or
        d, e, c2
        c will be the port connected to another non-FR port for a particular
        Left Pattern.
        """
        self.a, self.b = [ p for p in self.atom1.targets if p.atom != self.c1.atom ]
        self.d, self.e = [ p for p in self.atom2.targets if p.atom != self.c2.atom ]

    
    def _create_atoms_and_ports(self):
        """"""
        print(self.right_pattern)


            


    def _atoms_to_add(self):
        """Return Atom objects"""
        self._create_atoms_and_ports()
        

        
    def _atoms_to_delete(self):
        """Return list of Atom objects"""
        d = {} #atoms_to_delete_dict
        [ d.update({a.uid: a}) for a in [ self.atom1, self.atom2, self.c1, self.c2 ]]
        return d


    def _find_moves(self):
        """ Sets some variables and returns boolean on match"""
        move_dict = topology.moves[self.atom1.atom] #dict of moves for current atom
        for port_type in move_dict.keys():
            self.c1, = self.atom1._get_port_by_type(port_type)
            self.c2, = self.c1.targets #c1 is always 'out' port and c2 'in' port
            self.atom2 = self.c2.parent_atom
            if self.atom2.atom in move_dict[port_type].keys():
                self.right_pattern = mp._parse_mol_file(move_dict[port_type][self.atom2.atom])
                self.move_name = self.atom1.atom + "-" + self.atom2.atom
                return True
        return False


        
    


def atom_weightage( a1, a2):
    """
    atomWeightage( a1 = Atom object, a2 = Atom object)
    returns atom according to weightage, ie; L < A <FI....< T
    """
    weightage = [ "L", "A", "FI", "FO", "FOE", "Arrow", "T"]
    if _weightage.index(a1.atom) < _weightage.index(a2.atom):
        return [a1.atom, a2.atom]
    else:
        return [a2.atom, a1.atom]




def beta_move( d, L, A, cl, ca, mid):
    """ betaMove( mol_dict, L_mol_id, A_mol_id, c_port_of_L, c_port_A)
        return dict
        { mol_id: { 'target': [], 'type': str, 'name': str }
        ....}

        L-A (Beta) move
        ---------------
        L a b c, A c d e -> Arrow a e, Arrow d b
    """
    port_names_of_L = d[L]['target'].copy()
    port_names_of_L.remove(cl)
    a, b = port_names_of_L

    port_names_of_A = d[A]['target'].copy()
    port_names_of_A.remove(ca)
    d,e = port_names_of_A
    
    nodes_to_add = { str(mid): { 'target': [a, e], 'type': 'Arrow'},
            str(mid+1): { 'target': [b, d], 'type': 'Arrow'} }
    nodes_to_remove = { L : {}, A: {}, cl: {}, ca:{} }
    
    links_to_remove = { }


