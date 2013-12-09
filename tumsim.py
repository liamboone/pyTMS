#!/usr/bin/python
import sys
import re
import ConfigParser
import time
import curses
import random

def cast(tup, chars):
    a,b,c = tup
    return (int(a), chars.index(b), c)

def initCurses():
    stdscr = curses.initscr()
    stdscr.scrollok(True)
    height, width = stdscr.getmaxyx()
    return (stdscr, height, width)

def drawTape(y, x, tape, chars):
    stdscr.addstr(y,0,chars[0]*w)
    for i,c in enumerate(tape):
        try:
            stdscr.addch(y, x + i, ord(chars[c]))
        except:
            pass

def randomMemory():
    return [0]+[random.randint(1,2) for i in xrange(80)]

if __name__ == '__main__':
    try:
        # Main Body
        # Read tm spec from arg[1]
        # spec includes states, characters, transitions, halting
        # configurations, initial state, initial head position and
        # direction, and initial memory configuration.
        play = False

        config = ConfigParser.SafeConfigParser({'memory':False})
        with open(sys.argv[1]) as fin:
            config.readfp(fin)

        states = config.getint('header', 'states')
        #characters = config.getint('header', 'characters')
        instructions = re.split(r'\s*\|\s*', config.get('header', 'instructions'))
        displaychars = config.get('header','display')
        instructions = map(lambda x: re.split(r'\s+', x), instructions)
        instructions = map(lambda y: map(lambda x: cast(re.split(r',', x),
                                                        displaychars), y), instructions)


        state = config.getint('init', 'state')
        pos = config.getint('init', 'pos')
        motion = config.get('init', 'motion')
        if config.get('init', 'memory'):
            memory = map(lambda x: displaychars.index(x), config.get('init', 'memory'))
        else:
            memory = randomMemory()

        (stdscr, h, w) = initCurses()

        cx = 2# int(w/2)
        cy = h-4 #int(h/2)

        sy = int(3*h/4)

        drawTape(cy,cx,memory,displaychars)
        while motion != 'H':
            #stdscr.clear()
            stdscr.move(0,0)
            stdscr.clrtoeol()
            stdscr.move(1,0)
            stdscr.clrtoeol()
            stdscr.move(h-3,0)
            stdscr.clrtoeol()
            stdscr.move(h-2,0)
            stdscr.clrtoeol()
            stdscr.move(h-1,0)
            stdscr.clrtoeol()
            if state == 0 and pos == 1:
                stdscr.scroll(1)
            drawTape(cy,cx,memory,displaychars)
            stdscr.addstr(0,0,'STATE:%d\nMOTION:%c' % (state, motion))
            state, char, motion = instructions[state][memory[pos]]
            memory[pos] = char
            oldpos = pos
            if motion == 'R':
                pos += 1
            elif motion == 'L':
                pos -= 1
            while pos < 0:
                memory.insert(0,0)
                pos += 1
            while pos >= len(memory):
                memory.append(0)

            if motion != 'H':
                stdscr.addstr(h-3,0,'NEXT_STATE:%d\nNEXT_MOTION:%c\nNEXT_CHARACTER:%c'
                              % (state, motion, displaychars[char]))
            else:
                stdscr.addstr(h-3,0,'NEXT_STATE:HALT\nNEXT_MOTION:HALT\nNEXT_CHARACTER:%c'
                              % (displaychars[char]))
            stdscr.move(cy,cx+oldpos)
            time.sleep(0.016)
            stdscr.refresh()
            if not play:
                play = (ord(' ') == stdscr.getch())

        stdscr.clear()
        stdscr.addstr(0,0,'STATE:HALT\nMOTION:HALT')
        drawTape(cy,cx,memory,displaychars)
        stdscr.move(cy,cx)
        stdscr.getch()
    except Exception as e:
        print e
        raise
    finally:
        try:
            curses.endwin()
        except:
            raise
