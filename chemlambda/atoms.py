# -*- coding: utf-8 -*-
#
#  atoms.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sun 19 Jul 2015 18:55:29 IST
#  ver    :

# Atom class

from chemlambda import settings
from chemlambda import topology
from chemlambda import textformat
import copy

tf = textformat.TextFormat()


class Atom:
    """ """
    def __init__(self, uid='', atom='', targets=[], lno=''):
        self.uid = uid
        self.atom = atom
        self.targets = targets
        self.lno = lno

    def _add_target(self, target):
        index = self._insert_into(target)
        self.targets.insert(index, target)

    def _remove_target(self, target):
        self.targets.remove(target)

    def _get_color_and_size(self):
        """_get_color_and_size()
            Return type: list
            [ color, size ]
        """
        return settings.atom_color_size_dict[self.atom]

    def _get_port_by_type(self, port_kind):
        """ Return the port of the Atom from port atom kind """
        return [port for port in self.targets if port.atom == port_kind]

    def _insert_into(self, p):
        """Returns which index a p(ort) should go for the current atom1"""
        return topology.graph[self.atom].index(p.atom)

    def _deflate(self):
        """
        Converts all Atom obj targets to uid strings
        Returns a copy of Atom
        """
        atom_copy = copy.copy(self)
        for key, value in atom_copy.__dict__.items():
            if key == 'targets':
                atom_copy.targets = [p.uid for p in value]
            if key == 'sources':
                atom_copy.sources = [p.uid for p in value]
            if key == 'parent_atom':
                atom_copy.parent_atom = value.uid
        return atom_copy

    def _inflate(self, atom_dict):
        """
        Convert puid targets back to atom objects (use?)
        """
        atom_copy = copy.copy(self)
        for key, value in atom_copy.__dict__.items():
            if key == 'targets':
                atom_copy.targets = [atom_dict[uid] for uid in value]
            if key == 'sources':
                atom_copy.sources = [atom_dict[uid] for uid in value]
            if key == 'parent_atom':
                atom_copy.parent_atom = atom_dict[value]
        return atom_copy


class Port(Atom):
    """ """
    def __init__(self, uid='', atom='', port_name='',  parent_atom='', free=1,
                 sources=[]):
        Atom.__init__(self, uid=uid, atom=atom, targets=[])
        self.port_name = port_name
        self.parent_atom = parent_atom
        self.lno = self.parent_atom.lno
        self.free = free
        self.sources = sources

    def _add_target(self, target):
        self.targets = [target]

    def _add_source(self, source):
        self.sources = [source]

    @staticmethod
    def _set_matched_port(p1, p2):
        """
        Check if matching ports, ie; in port & out port (mo ->li or ro->ri etc)
        Set targets p1 --> p2
        """
        if p1.atom[-1] == p2.atom[-1]:
            # TODO: untested
            ln = tf.ftext(p1.parent_atom.lno, fcol='gr')
            tf.error("Port mismatch in mol file\n line {}".format(ln))
            #print("\033[91mError:\033[0m Port mismatch in mol file\nline \033[92m{}\033[0m"
                  #.format(p1.parent_atom.lno))
            return None
        p1.free = p2.free = 0  # ready for Freenodes
        if p1.atom[-1] == 'o':
            p1.targets = [p2]
            p2.sources = [p1]
        else:
            p2.targets = [p1]
            p1.sources = [p2]

    def _is_out_port(self):
        """ returns boolean """
        return self.atom[-1] is 'o'
