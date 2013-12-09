#!/usr/bin/python

import sys

def tr(bch):
    return {'0':'.', '1':'@'}[bch]

decimal = int(sys.argv[1]) % 256
binary = "{0:08b}".format(decimal)

program = """#!./tumsim.py
# Simulate rule {0} 1D Cellular Automata
# 000 -> {8}
# 001 -> {7}
# 010 -> {6}
# 011 -> {5}
# 100 -> {4}
# 101 -> {3}
# 110 -> {2}
# 111 -> {1}
[header]
states=4

#0 - pass1a carry0 from left
#1 - pass1b carry1 from left
#2 - pass2a carry0 from right
#3 - pass2b carry1 from right

#Blanks are not counted and are represented as _
characters=6
display=_.@ABCD
#                      .     @     A     B     C     D
#              blank   0     1    00    01    10    11
instructions = 2,_,L 0,A,R 1,B,R 0,A,R 1,B,R 0,A,R 1,B,R
             | 2,_,L 0,C,R 1,D,R 0,C,R 1,D,R 0,C,R 1,D,R
             | 0,_,R 2,{8},L 3,{6},L 2,{8},L 3,{6},L 2,{4},L 3,{2},L
             | 0,_,R 2,{7},L 3,{5},L 2,{7},L 3,{5},L 2,{3},L 3,{1},L

[init]
state=0
pos=1
motion=R
""".format(decimal, *map(tr, binary))

print program
