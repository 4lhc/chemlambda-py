
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  atoms.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sun 19 Jul 2015 18:55:29 IST
#  ver    : 

# Create Atom objects

from chemlambda import settings
from chemlambda import topology

class Atom:
    """ """
    def __init__(self, uid='', atom='', targets = [], lno='', sources = []):
        self.uid = uid
        self.atom = atom
        self.targets = targets
        self.sources = sources
        self.lno = lno
        #print("Atom {} of kind '{}' created..".format(self.uid, self.atom))

    def _add_target(self, target):
        self.targets.append(target)

    def _remove_target(self, target):
        self.targets.remove(target)

    def _add_source(self, source):
        self.sources.append(source)

    def _remove_source(self, source):
        self.sources.remove(source)

    def _get_color_and_size(self):
        """_get_color_and_size()
            Return type: list 
            [ color, size ]
        """
        return settings.atom_color_size_dict[self.atom]



    def _get_port_by_type(self, port_kind):
        """ Return the port of the Atom from port atom kind """
        return [ port for port in self.targets if port.atom == port_kind ]




class Port(Atom):
    """ """
    def __init__(self, uid='', atom='', port_name='',  parent_atom='', free = 1):
        Atom.__init__(self, uid=uid, atom=atom, targets = [], sources = [])
        self.port_name = port_name
        self.parent_atom = parent_atom
        self.lno = self.parent_atom.lno
        self.free = free


    @staticmethod
    def _set_matched_port(p1, p2):
        """
        Check if matching ports, ie; in port & out port (mo ->li or ro->ri etc)
        Set targets p1 --> p2
        Return parent atoms of both port atom
        """
        if p1.atom[-1] == p2.atom[-1]:
            print("\033[91mError:\033[0m Port mismatch in mol file\nline \033[92m{}\033[0m"
                    .format(self.parent_atom.lno))
            return None
        p1.free = p2.free = 0 #ready for Freenodes
        if p1.atom[-1] == 'o':
            p1.targets.append(p2) #targets only on port of kind out todo
        else:
            p2.targets.append(p1)
        return (p1.parent_atom, p2.parent_atom) 

    def _is_out_port(self):
        """ returns boolean """
        return self.atom[-1] is 'o'





