
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

class Moves:
    """
    """
    def __init__(self, atom1, atom2, a, b, c1, d, e, c2):
        """
            args: Atom objects
            atom1, atom2 are atoms in Left Pattern (LP)
            a, b, c1 are ports of atom1
            d, e, c2 are ports of atom2
            c1 and c2 are ports with the common port_name, ie; c1 and c2 links
            the two atoms
        """
        self.identifyMove()
        moves = { "BETA" : { 'ddd': 'ddd'

                    }


        }

        
    def identifyMove(self):
        """
        """
        identifymove = { 
            "COMB": ["L-Arrow","A-Arrow","FI-Arrow","FO-Arrow","FOE-Arrow"],
            "BETA": [ "L-A" ], 
            "FAN-IN": ["FI-FOE"],
            "DIST-L": [ "L-FO", "L-FOE" ],
            "DIST-A": ["A-FO", "A-FOE"], 
            "DIST-FI": ["FI-FO"],
             "DIST-FO": ["FO-FOE"], 
             "PRUNE1": [ "A-T", "FI-T"],
             "PRUNE2": [ "L-T"],
             "PRUNE3": ["FO-T", "FOE-T"]
                   #getattr 
            }
        
        self.atom1.atom


def atomWeightage( a1, a2):
    """
    atomWeightage( a1 = Atom object, a2 = Atom object)
    returns atom according to weightage, ie; L < A <FI....< T
    """
    _weightage = [ "L", "A", "FI", "FO", "FOE", "Arrow", "T"]
    if _weightage.index(a1.atom) < _weightage.index(a2.atom):
        return [a1.atom, a2.atom]
    else:
        return [a2.atom, a1.atom]




def betaMove( d, L, A, cl, ca, mid):
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



