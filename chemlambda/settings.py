
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  settings.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 17:25:35 IST
#  ver    : 

#
# A python port of chemlambda-gui by chorasimilarity (Marius Buliga, http://chorasimilarity.wordpress.com/)
#

# Atom specific settings for visualisation



#atom (node) colors
green_col = "#8CC152"
red_col = "#b80000"
in_col = "#f0a900"
out_col = "#91009a"
term_col = "#222222"
arrow_col = "#ffffff"
white_col = "#ffffff"

#atom sizes
port_size = 1
mid_port_size = 2
main_atom_size = 4


atom_color_size_dict = { "mi": [  in_col,  mid_port_size],
                         "li": [  in_col,  port_size],
                         "ri": [  in_col,  port_size],
                         "mo": [  out_col,  mid_port_size], 
                         "lo": [  out_col,  port_size],
                         "ro": [  out_col,  port_size],
                         "fo": [  out_col,  port_size],
                         "fi": [  in_col,  port_size],
                         "L": [  red_col,  main_atom_size],
                         "A": [  green_col,  main_atom_size],
                         "FI": [  red_col,  main_atom_size],
                         "FO": [  green_col,  main_atom_size],
                         "FOE": [  in_col,  main_atom_size],
                         "Arrow": [  arrow_col,  main_atom_size],
                         "T": [  term_col,  main_atom_size],
                         "FROUT": [  out_col,  main_atom_size],
                         "FRIN": [  in_col,  main_atom_size]
                       }


