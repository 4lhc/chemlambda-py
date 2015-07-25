# -*- coding: utf-8 -*-
#
#  topology.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 17:53:16 IST
#  ver    :
#

# 'Topology' (ie; rules to read mol files ) and allowed 'Moves' for each atom
# [http://chorasimilarity.github.io/chemlambda-gui/dynamic/moves.html]

# dict containg rules to identify ports for each atom
# mi = 'middle in', lo = 'left out' and so...
graph = {
        "L": ["mi", "lo", "ro"],
        "FO": ["mi", "lo", "ro"],
        "FOE": ["mi", "lo", "ro"],
        "A": ["li", "ri", "mo"],
        "FI": ["li", "ri", "mo"],
        "Arrow": ["mi", "mo"],
        "T": ["mi"],
        "FRIN": ["fo"],
        "FROUT": ["fi"]
        }


# Allowed moves for each atom
# structure { "Atom1":
#                    { 'port' :
#                           { 'Atom2': [ RP ],
#                             'Atom2x': [ RP],
#                               -
#                               -
#                               -
#                           }
#                    }
#           }

# Atom1, Atom2x forms the left pattern
# port is the port of Atom1 through which legal moves are possible
# 'ro' is the only valid port type for 'L' atoms
# RP is written in the same notation as in:
# [https://chorasimilarity.wordpress.com/2015/03/15/the-moves-of-chemlambda-v2-in-mol-format/]

# Hence reading the first move => L-A's RP = Arrow a e, Arrow d b

# TODO: Write COMB moves rule

moves = {
        "L":
        {
            'ro':
            {
                'A': ["Arrow a e", "Arrow d b"],
                'FO': ["FI  j i b", "L  k i d", "L  l j e", "FOE  a k l"],
                'FOE': ["FI  j i b", "L  k i d", "L  l j e", "FOE  a k l"],
                'T': ["T a", "FRIN  b"],

                }
            },
        "A":
        {
            'mo':
            {
                'FO': ["FOE  a i j", "A  i k d", "A  j l e", "FOE  b k l"],
                'FOE': ["FOE  a i j", "A  i k d", "A  j l e", "FOE  b k l"],
                'T': ["T  a", "T b"],

                }
            },
        "FI":
        {
            'mo':
            {
                'FOE': ["Arrow  a e", "Arrow  b d"],
                'FO': ["FO  a i j", "FI  i k d", "FI  j l e", "FO  b k l"],
                'T': ["T  a", "T b"],

                }
            },
        "FO":
        {
            'ro':
            {
                'FOE': ["FI  j i b", "FO  k i d", "FO  l j e", "FOE  a k l"],
                'T': ["Arrow a b"]

                },
            'lo':
            {
                'T': ["Arrow  a b"]

                }
            },
        "FOE":
        {
            'ro':
            {
                'T': ["Arrow  a b"]

                },
            'lo':
            {
                'T': ["Arrow  a b"]

                }

            }
        }
