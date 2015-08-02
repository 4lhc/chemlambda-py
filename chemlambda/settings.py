# -*- coding: utf-8 -*-
#
#  settings.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 17:25:35 IST
#  ver    :


# Atom specific settings for visualisation

# TODO: Class

verbose = True  # set verbosity

# The following takes effect only if verbose is True
# Print Atoms and Ports as tables; Useless in huge molecules
show_tables = False
show_atom_count = True

# Every moves per cycle
show_moves = False
show_move_count = True

# show attempts at moves and failures
show_move_tries = False

# set False for random moves
deterministic = True

# atom (node) colors
green_col = "#8CC152"
red_col = "#b80000"
in_col = "#f0a900"
out_col = "#91009a"
term_col = "#222222"
arrow_col = "#ffffff"
white_col = "#ffffff"

# atom sizes
port_size = 1
mid_port_size = 2
main_atom_size = 4


atom_color_size_dict = {
        "mi": [in_col,  mid_port_size],
        "li": [in_col,  port_size],
        "ri": [in_col,  port_size],
        "mo": [out_col,  mid_port_size],
        "lo": [out_col,  port_size],
        "ro": [out_col,  port_size],
        "fo": [out_col,  port_size],
        "fi": [in_col,  port_size],
        "L": [red_col,  main_atom_size],
        "A": [green_col,  main_atom_size],
        "FI": [red_col,  main_atom_size],
        "FO": [green_col,  main_atom_size],
        "FOE": [in_col,  main_atom_size],
        "Arrow": [arrow_col,  main_atom_size],
        "T": [term_col,  main_atom_size],
        "FROUT": [out_col,  main_atom_size],
        "FRIN": [in_col,  main_atom_size]
        }


term_in_col = dict(fcol='ye', fattr='none')
term_out_col = dict(fcol='cy', fattr='none')
term_red_col = dict(fcol='rd', fattr='bold')
term_green_col = dict(fcol='gr', fattr='bold')
term_arrow_col = dict(fcol='wt', fattr='bold')
term_term_col = dict(fcol='bl', fattr='bold')


atom_term_color = {
        "mi": term_in_col,
        "li": term_in_col,
        "ri": term_in_col,
        "mo": term_out_col,
        "lo": term_out_col,
        "ro": term_out_col,
        "fo": term_out_col,
        "fi": term_in_col,
        "L": term_red_col,
        "A": term_green_col,
        "FI": term_red_col,
        "FO": term_green_col,
        "FOE": term_in_col,
        "Arrow": term_arrow_col,
        "T": term_term_col,
        "FROUT": term_out_col,
        "FRIN": term_in_col
        }
