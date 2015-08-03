# -*- coding: utf-8 -*-
#
#  moves.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sun 19 Jul 2015 13:26:52 IST
#  ver    :

# 'Moves' to be performed
# [https://chorasimilarity.wordpress.com/2015/03/15/the-moves-of-chemlambda-v2-in-mol-format/]

from chemlambda import topology
from chemlambda import settings
from chemlambda import molparser as mp
from chemlambda import textformat

tf = textformat.TextFormat()


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
        self.counter = counter  # counter object
        self.is_comb = False  # this is for Pruning and COMBs
        self.is_prune = False
        self.is_cycomb = False  # Arrow -Arrow chains
        self.is_FRINcomb = False  # FRIN-Arrow chain
        self.is_FrinPrune = False  # FRIN-T chain
        self.move_name = ''
        self.right_pattern = ''
        self.weight = -100  # priority for deterministic cases
        # valid_move is set to True if move is valid in topology
        self.valid_move = self._find_moves()  # keep this the last line in init

    def _find_moves(self):
        """ Sets some variables and returns None"""
        move_dict = topology.moves[self.atom1.atom]
        for port_type in move_dict.keys():
            # IMPPPP both lo and ro happens!!
            # sets c1 from outport set in topology.moves
            self.c1, = self.atom1._get_port_by_type(port_type)
            # this is important! c1 is always 'out' port and c2 'in'
            self.c2, = self.c1.targets
            self.atom2 = self.c2.parent_atom
            if self.atom2.atom in move_dict[port_type].keys():
                self.valid_move = True
                if self.atom2.atom == 'T':
                    self.move_name = 'PRUNE'
                elif self.atom2.atom == 'Arrow':
                    self.move_name = 'COMB'
                else:
                    self.move_name = self.atom1.atom + "-" + self.atom2.atom
                self.right_pattern = move_dict[port_type][self.atom2.atom]
                self.weight = topology.weight[self.move_name]
                return True
        return False

    def _bind_ports(self):
        """
        set a, b, c1 or d, e, c2
        c will be the port connected to another non-FR port for a particular
        Left Pattern.
        """
        try:
            # in case of Arrow chains and FRIN-Arrow
            self.a, self.b = [p for p in self.atom1.targets
                              if p.atom != self.c1.atom]
            self.a.port_name = 'a'
            self.b.port_name = 'b'
        except ValueError:
            if self.atom1.atom == 'FRIN' and self.atom2.atom == 'Arrow':
                self.d, = [p for p in self.atom2.targets
                           if p.atom != self.c2.atom]
                self.d.port_name = 'd'
                self.is_FRINcomb = True
            if self.atom1.atom == 'FRIN' and self.atom2.atom == 'T':
                self.is_FrinPrune = True
            if self.atom1.atom == 'Arrow' and self.atom2.atom == 'Arrow':
                self.a, = [p for p in self.atom1.targets
                           if p.atom != self.c1.atom]
                self.d, = [p for p in self.atom2.targets
                           if p.atom != self.c2.atom]
                self.a.port_name = 'a'
                self.d.port_name = 'd'
                self.is_cycomb = True

        self.c1.port_name = 'c'
        self.c2.port_name = 'c'


        try:
            # pruning/ comb moves don't have d and/or e
            self.d, self.e = [p for p in self.atom2.targets
                              if p.atom != self.c2.atom]
            self.d.port_name = 'd'
            self.e.port_name = 'e'
        except ValueError:
            if self.atom2.atom == 'T':
                self.is_prune = True
            if (self.atom2.atom == 'Arrow' and
                    not self.is_cycomb and
                    not self.is_FRINcomb):
                self.d, = [p for p in self.atom2.targets
                           if p.atom != self.c2.atom]
                self.d.port_name = 'd'
                self.is_comb = True
            pass

    def _is_valid(self, atoms_taken):
        """Return boolean"""
        if (self.valid_move and
                self.atom1 not in atoms_taken and
                self.atom2 not in atoms_taken):
            if settings.show_move_tries:
                print(tf.ftext("[y] MOVE of " + self.atom1.uid + " >" +
                               self.atom2.uid, fcol='gr'))
            self._bind_ports()
            self._move_update()
            atoms_taken += [self.atom1, self.atom2]
            return True
        if settings.show_move_tries:
            print(tf.ftext("[n] MOVE of " + self.atom1.uid + " >" +
                           self.atom2.uid, fcol='rd'))
        return False

    def _move_update(self):
        """ fill move uid, move name, LP_RP etc """
        cc = self.counter.cycle_count
        mc = self.counter.move_count
        self.uid = str(cc) + '_' + str(mc)
        self.counter.move_count += 1
        return self

    @staticmethod
    def _update_new_port(p, p2):
        p.targets = p2.targets
        p.sources = p2.sources
        if len(p2.sources) > 0:
            p2.sources[0].targets = [p]
        else:
            p2.targets[0].sources = [p]

    def _create_atoms_and_ports(self):
        """ """
        d_a, d_p = mp._read_mol_file(self.right_pattern,
                                     self.counter.atom_count)
        self.counter.atom_count += list(d_a.keys()).__len__()
        ports_to_add = []

        for k, p in d_p.items():
            # self.b's parent & parent's target --> p
            if p.port_name == 'a':
                Moves._update_new_port(p, self.a)
                ports_to_add.append(p)
            elif p.port_name == 'b':
                Moves._update_new_port(p, self.b)
                ports_to_add.append(p)
            elif p.port_name == 'd':
                Moves._update_new_port(p, self.d)
                ports_to_add.append(p)
            elif p.port_name == 'e':
                Moves._update_new_port(p, self.e)
                ports_to_add.append(p)
            else:
                pass
        [d_p.update({p.uid: p}) for p in ports_to_add]

        mp._find_matched(d_p)

        if settings.verbose:
            self.lp_rp = self._get_LP_to_RP(d_a)

        Moves._delete_attr(d_p, 'port_name')  # clear generic port_names
        Moves._delete_attr(d_a, 'lno')
        return (d_a, d_p)

    @staticmethod
    def _delete_attr(d, attr):
        """delete certain attributes from all atom/port objects"""
        [d[k].__setattr__(attr, '') for k in d]

    def _atoms_to_delete(self):
        """Return dict of Atoms and Ports objects"""
        if self.is_cycomb:
            ports_to_del = [self.a, self.d, self.c1, self.c2]
        elif self.is_FrinPrune:
            # keep this above is_prune:
            ports_to_del = [self.c1, self.c2]
        elif self.is_FRINcomb:
            ports_to_del = [self.d, self.c1, self.c2]
        elif self.is_comb:
            ports_to_del = [self.a, self.b, self.c1, self.c2, self.d]
        elif self.is_prune:
            ports_to_del = [self.a, self.b, self.c1, self.c2]
        else:
            ports_to_del = [self.a, self.b, self.d, self.e, self.c1, self.c2]
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

    def _atoms_to_add(self):
        """Return Atom objects"""
        self._bind_ports()
        return self._create_atoms_and_ports()

    def _add_atoms_ports_to_dict(self, dict_atoms, dict_ports):
        """Adds atoms and ports to dict_atoms and dict_ports"""
        d_a, d_p = self._atoms_to_add()
        dict_atoms.update(d_a)
        dict_ports.update(d_p)
        return self

    def _get_LP_to_RP(self, a_a):
        """
        Return colour formatted string of LP --> RP for the move
        """
        def _atom_format(atom):
            """"""
            text = tf.ftext('[', fcol='mg')
            text += tf.ftext(atom.uid, **t_cols[atom.atom])
            text += '  '
            text += ' '.join([tf.ftext(port.port_name, **t_cols[port.atom])
                              for port in atom.targets])
            text += tf.ftext(']', fcol='mg')
            return text

        t_cols = settings.atom_term_color
        d_a = [self.atom1, self.atom2]  # d_a is LP & a_a is RP

        lp_rp = ', '.join([_atom_format(a) for a in d_a])
        lp_rp += tf.ftext(' --> ', fcol='wt')
        lp_rp += ', '.join([_atom_format(a) for a in a_a.values()])
        return lp_rp

    def _move_snapshot(self):
        """
        Deflate Moves object for snapshot.
        Returns deflated move object
        """
        [self.__setattr__(k, v.uid) for k, v in self.__dict__.items()
         if hasattr(v, 'uid')]  # hope nothing else turn up with attr 'uid'
        return self
