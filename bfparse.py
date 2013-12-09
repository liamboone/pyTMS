import sys
import re

def left_inst(character, number):
    return "{},{},L".format(number + 1, character)

def right_inst(character, number):
    return "{},{},R".format(number + 1, character)

def plus_inst(character, number, allchars, count=1):
    chnum = allchars.index(character)
    chnum = (chnum + count) % len(allchars)
    return "{},{},N".format(number + 1, allchars[chnum])

def minus_inst(character, number, allchars, count=1):
    chnum = allchars.index(character)
    chnum = (chnum - count) % len(allchars)
    return "{},{},N".format(number + 1, allchars[chnum])

def lbrac_inst(character, number, matching, allchars):
    chnum = allchars.index(character)
    if chnum == 0:
        return "{},{},N".format(matching, character)
    else:
        return "{},{},N".format(number + 1, character)

def rbrac_inst(character, number, matching, allchars):
    chnum = allchars.index(character)
    if chnum == 0:
        return "{},{},N".format(number + 1, character)
    else:
        return "{},{},N".format(matching, character)

def halt_inst(character):
    return "0,{},H".format(character)

chars = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPTIMIZE = False
i = 0
stack = []
insts = []
program = []
ch = sys.stdin.read(1)
while ch != '':
    if ch in '[]+-<>':
        program.append(ch)
    ch = sys.stdin.read(1)

prstr = ''.join(program)

pluss = re.compile(r'\++')
minuss = re.compile(r'-+')

ispliter = re.compile(r'\+[0-9]+|-[0-9]+|<|>|\[|\]')

for it in reversed([x for x in re.finditer(pluss, prstr)]):
    s = it.start()
    e = it.end()
    prstr = prstr[:s] + '+' + str(e-s) + prstr[e:]

for it in reversed([x for x in re.finditer(minuss, prstr)]):
    s = it.start()
    e = it.end()
    prstr = prstr[:s] + '-' + str(e-s) + prstr[e:]

program = re.findall(ispliter, prstr)

for ch in program:
    if ch == '[':
        insts.append(None)
        stack.append(i)
        i += 1
    elif ch == ']':
        if len(stack) == 0:
            sys.stderr.write("ERROR: Extra ']'")
            exit()
        match = stack.pop()
        insts.append((rbrac_inst, i, match, chars))
        insts[match] = (lbrac_inst, match, i, chars)
        i += 1
    elif ch[0] == '-':
        if OPTIMIZE:
            insts.append((minus_inst, i, chars, int(ch[1:])))
            i += 1
        else:
            for x in xrange(int(ch[1:])):
                insts.append((minus_inst, i, chars, 1))
                i += 1
    elif ch[0] == '+':
        if OPTIMIZE:
            insts.append((plus_inst, i, chars, int(ch[1:])))
            i += 1
        else:
            for x in xrange(int(ch[1:])):
                insts.append((plus_inst, i, chars, 1))
                i += 1
    elif ch == '<':
        insts.append((left_inst, i))
        i += 1
    elif ch == '>':
        insts.append((right_inst, i))
        i += 1

if len(stack) != 0:
    sys.stderr.write("ERROR Missing ']'")
    exit()

print """#!./tumsim.py
[header]
states={}
display={}
instructions=""".format(len(insts)+1, chars),

for inst in insts:
    for c in chars:
        print inst[0](c,*inst[1:]),
    print "\n            |",
for c in chars:
    print halt_inst(c),

print """
[init]
state=0
pos=0
motion=N
memory=0
"""
