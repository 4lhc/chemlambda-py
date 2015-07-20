
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
    def __init__(self, uid='', atom='', targets = [], sources = []):
        self.uid = uid
        self.atom = atom
        self.targets = targets
        self.sources = sources
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
        If c will be the port connected to another non-FR port for a particular
        Left Pattern.
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
    def __init__(self, uid='', atom='', port_name=''):
        Atom.__init__(self, uid=uid, atom=atom, targets = [], sources = [])
        self.port_name = port_name

    def setPortnames(self):
        print('port_name already set: {}'.format(self.port_name))

    def getPortnames(self):
        return [self.port_name]

    def getParentatom(self):
        """
        Return uid parent atom of the port atom
        port uid = L_0_2, parent uid = L_0
        """
        return '_'.join(self.uid.split('_')[:-1])




