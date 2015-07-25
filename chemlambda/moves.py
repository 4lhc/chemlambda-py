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

# TODO: Needs move uid
# TODO: _move_update

from chemlambda import topology
from chemlambda import settings
from chemlambda import molparser as mp
from chemlambda import textcolor

tc = textcolor.TextColor()


class Moves:
    """
    find valid moves
    create required atoms
    """
    def __init__(self, atom1, counter):
        """
            args: Atom objects
            atom1, atom2 are atoms in Left Pattern (LP)
            a, b, c1 are ports of atom1
            d, e, c2 are ports of atom2
            c1 and c2 are ports with the common port_name, ie; c1 and c2 links
            the two atoms
        """
        self.atom1 = atom1
        self.valid_move = self._find_moves()
        self.uid = ''
        self.counter = counter  # counter object

    def _move_update(self):
        """
        fill move uid, move name, LP_RP etc
        """
        cc = self.counter.cycle_count
        mc = self.counter.move_count
        self.uid = str(cc) + '_' + str(mc)
        self.LP_RP = self._get_LP_to_RP()
        self.counter.move_count += 1
        return self

    def _bind_ports(self):
        """
        set a, b, c1
        or
        d, e, c2
        c will be the port connected to another non-FR port for a particular
        Left Pattern.
        """
        self.a, self.b = [p for p in self.atom1.targets if p.atom != self.c1.atom]
        self.a.port_name = 'a'
        self.b.port_name = 'b'
        try:
            # pruning/ comb moves don't have d and e
            self.d, self.e = [p for p in self.atom2.targets
                              if p.atom != self.c2.atom]
            self.d.port_name = 'd'
            self.e.port_name = 'e'
        except ValueError:
            pass

    @staticmethod
    def _update_old_port(p1, p2):
        p1.atom = p2.atom
        p2.parent_atom._remove_target(p2)
        p2.parent_atom._add_target(p1)
        p1.parent_atom = p2.parent_atom
        p1.port_name = p2.port_name


    def _create_atoms_and_ports(self):
        """
        """
        d_a, d_p = mp._read_mol_file(self.right_pattern,
                                     self.counter.atom_count)
        self.counter.atom_count += list(d_a.keys()).__len__()
        ports_to_del = []
        ports_to_add = []

        for k, p in d_p.items():
            # update p.atom ro-->mo etc
            # update self.b's parent & parent's target
            if p.port_name == 'a':
                Moves._update_old_port(self.a, p)
                ports_to_del.append(p.uid)
                ports_to_add.append(self.a)
            elif p.port_name == 'b':
                Moves._update_old_port(self.b, p)
                ports_to_del.append(p.uid)
                ports_to_add.append(self.b)
            elif p.port_name == 'd':
                Moves._update_old_port(self.d, p)
                ports_to_del.append(p.uid)
                ports_to_add.append(self.d)
            elif p.port_name == 'e':
                Moves._update_old_port(self.e, p)
                ports_to_del.append(p.uid)
                ports_to_add.append(self.e)
            else:
                pass
        # deleting newly created atoms (a,b,d,e equivalents)
        [d_p.__delitem__(k) for k in ports_to_del]
        # adding a,b,c,d to d_p
        [d_p.update({p.uid: p}) for p in ports_to_add]

        mp._find_matched(d_p)
        Moves._delete_attr(d_p, 'port_name')  # clear generic port_names
        Moves._delete_attr(d_a, 'lno')
        return (d_a, d_p)

    @staticmethod
    def _delete_attr(d, attr):
        """delete certain attributes from all atom/port objects"""
        [d[k].__setattr__(attr, '') for k in d]

    def _atoms_to_add(self):
        """Return Atom objects"""
        self._bind_ports()
        return self._create_atoms_and_ports()

    #def _atoms_to_delete(self):
        #"""Return dict of Atom objects"""
        #d = {}  # atoms_to_delete_dict
        #[d.update({a.uid: a}) for a in [self.atom1, self.atom2]]
        #return d

    def _atoms_to_delete(self):
        """Return dict of Atoms and Ports objects"""
        ports_to_del = [self.c1, self.c2]
        atoms_to_del = [self.atom1, self.atom2]
        d_p = [(a.uid, a) for a in ports_to_del]
        d_a = [(a.uid, a) for a in atoms_to_del]
        return (dict(d_a), dict(d_p))

    def _del_atoms_ports_from_dict(self, dict_atoms, dict_ports):
        """Delete all unwanted atoms from dict_atoms and dict_ports"""
        d_a, d_p = self._atoms_to_delete()
        [dict_atoms.__delitem__(k) for k in d_a]
        [dict_ports.__delitem__(k) for k in d_p]
        return self

    def _add_atoms_ports_to_dict(self, dict_atoms, dict_ports):
        """Adds atoms and ports to dict_atoms and dict_ports"""
        d_a, d_p = self._atoms_to_add()
        dict_atoms.update(d_a)
        dict_ports.update(d_p)
        return self

    def _find_moves(self):
        """ Sets some variables and returns boolean on match"""
        move_dict = topology.moves[self.atom1.atom]
        for port_type in move_dict.keys():
            self.c1, = self.atom1._get_port_by_type(port_type)
            self.c2, = self.c1.targets  # c1 is always 'out' and c2 'in' port
            self.atom2 = self.c2.parent_atom
            if self.atom2.atom in move_dict[port_type].keys():
                self.right_pattern = move_dict[port_type][self.atom2.atom]
                self.move_name = self.atom1.atom + "-" + self.atom2.atom
                return True
        return False

    def _get_LP_to_RP(self):
        """
        Return colour formatted string of LP --> RP for the move
        """
        def _atom_format(atom):
            """"""
            text = tc.ftext('[', fcol='mg')
            text += tc.ftext(atom.uid, **t_cols[atom.atom])
            text += '  '
            text += ','.join([tc.ftext(port.uid, **t_cols[port.atom])
                              for port in atom.targets])
            text += tc.ftext(']', fcol='mg')
            return text

        t_cols = settings.atom_term_color
        d_a = self._atoms_to_delete()[0]
        a_a = self._atoms_to_add()[0]

        lp_rp = ', '.join([_atom_format(a) for a in d_a.values()])
        lp_rp += tc.ftext(' --> ', fcol='wt')
        lp_rp += ', '.join([_atom_format(a) for a in a_a.values()])
        return lp_rp

    def _move_snapshot(self):
        """
        Deflate Moves object for snapshot.
        Returns deflated move object
        """
        return self


