
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
    """
    """
    def __init__(self, uid='', atom='', targets = [], lno='', sources = []):
        self.uid = uid
        self.atom = atom
        self.targets = targets
        self.sources = sources
        self.lno = lno
        print("Atom {} of kind '{}' created..".format(self.uid, self.atom))

    def addTarget(self, target):
        self.targets.append(target)

    def removeTarget(self, target):
        self.targets.remove(target)

    def addSource(self, source):
        self.sources.append(source)

    def removeSource(self, source):
        self.sources.remove(source)

    def getColorAndSize(self):
        """getColorAndSize()
            Return type: list 
            [ color, size ]
        """
        return settings.atom_color_size_dict[self.atom]

    def setPortnames(self, a, b, c):
        """
        set a, b, c
        or
        d, e, c
        c will be the port connected to another non-FR port for a particular
        Left Pattern.
        The ports are set before every LP move
        """
        self.a = a
        self.b = b
        self.c = c

    def getPortnames(self, dict_ports):
        """
        getPortnames(dict_ports)
        return port names of current atom
        """
        return [dict_ports[port].port_name for port in self.targets]

    def getTopology(self):
        """
        Return the order in which ports are written in mol files based on rules set
        in topology.py
        """
        return topology.graph[self.atom]




class Port(Atom):
    """
    """
    def __init__(self, uid='', atom='', port_name='',  parent_atom='', free = 1):
        Atom.__init__(self, uid=uid, atom=atom, targets = [], sources = [])
        self.port_name = port_name
        self.parent_atom = parent_atom
        self.lno = self.parent_atom.lno
        self.free = free

    def setPortnames(self):
        print('port_name already set: {}'.format(self.port_name))

    def getPortnames(self):
        return [self.port_name]

    def setMatchedport(self, p2):
        """
        Check if matching ports, ie; in port & out port (mo ->li or ro->ri etc)
        Set targets p1 --> p2
        Return parent atoms of both port atom
        """
        if self.atom[-1] == p2.atom[-1]:
            print("\033[91mError:\033[0m Port mismatch in mol file\nline \033[92m{}\033[0m"
                    .format(self.parent_atom.lno))
            return None
        self.free = p2.free = 0 #ready for Freenodes
        self.targets.append(p2)
        return (self.parent_atom, p2.parent_atom) 




