
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  settings.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 17:25:35 IST
#  ver    : 

# Atom specific settings

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

atom_color_size_dict = { "mi": { "color": in_col, "size": mid_port_size},
                         "li": { "color": in_col, "size": port_size},
                         "ri": { "color": in_col, "size": port_size},
                         "mo": { "color": out_col, "size": mid_port_size}, 
                         "lo": { "color": out_col, "size": port_size},
                         "ro": { "color": out_col, "size": port_size},
                         "L": { "color": red_col, "size": main_atom_size},
                         "A": { "color": green_col, "size": main_atom_size},
                         "FI": { "color": red_col, "size": main_atom_size},
                         "FO": { "color": green_col, "size": main_atom_size},
                         "FOE": { "color": in_col, "size": main_atom_size},
                         "Arrow": { "color": arrow_col, "size": main_atom_size},
                         "T": { "color": term_col, "size": main_atom_size},
                         "FROUT": { "color": out_col, "size": main_atom_size},
                         "FRIN": { "color": in_col, "size": main_atom_size}
                       }


