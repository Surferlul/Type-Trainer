import curses
from curses import wrapper, initscr, endwin
import time
from time import sleep
from art import text2art
import locale
from math import log
from json import load
from os.path import isfile

if not isfile(".conf"):
    print ("There is no config! Creating config...")
    with open(".conf", "w") as cnf:
        cnf.write("0.5;0;0")

with open("special characters", "r", encoding="utf8") as s:
    sc = eval(s.read())
input("resize screen if needed")

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

with open(".save", "r", encoding="utf8") as s:
    sv2 = s.read().split("\n")
    sv = {
    "words": [],
    "amount": [],
    "average":[],
    "priority": []
    }
    for i in range(len(sv2)):
        sv2[i]=sv2[i].split(";")
        sv["words"].append(sv2[i][0])
        sv["amount"].append(int(sv2[i][1]))
        sv["average"].append(float(sv2[i][2]))
        sv["priority"].append(int(sv2[i][3]))

with open(".conf", "r") as f:
    r = f.read().split(";")
    spl = float(r[0])
    tr = int(r[1])
    score = float(r[2])

def strt_scrn():
    stdscr = initscr()
    stdscr.keypad(True)
    return stdscr

def give_word():
    global tr
    while 0 not in [tr % i for i in sv["priority"]]:
        tr+=1
    return [tr % i for i in sv["priority"]].index(0)

def create_header(Tm, Tm2, av, scr, amount, counter, pp, cp):
    global stdscr
    stdscr.addstr("esc - menu", curses.A_BLINK)
    stdscr.addstr("\n\n")
    
    for i in range(len(Tm2)):
        stdscr.addstr("   ")
        stdscr.addstr(Tm[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(Tm[i])))
        stdscr.addstr(av[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(av[i])))
        stdscr.addstr(Tm2[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(Tm2[i])))
        stdscr.addstr(scr[i] + "\n", curses.A_BLINK)
    
    stdscr.addstr("\n   "+ "Total: ")
    stdscr.addstr(amount, curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(amount))+ "Pos: ")
    stdscr.addstr(counter, curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(counter))+ "Prv Pnts: ")
    stdscr.addstr(str(pp), curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(str(pp)))+ "Crr Pnts: ")
    stdscr.addstr(str(cp), curses.A_BLINK)
    stdscr.addstr("\n\n")

stdscr = strt_scrn()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.use_default_colors()

def main(stdscr):
    global spl
    curses.start_color()
    curses.use_default_colors()
    # Clear screen
    stdscr.clear()
    y=0
    x=""
    pp = 0
    spl_prev = "----"
    active=sorted([sv["average"][i] / len(sv["words"][i]) for i in range(len(sv["average"])) if sv["average"][i] != 0])
    score = (1/(sum(active)/len(active)))**3*len(sv["words"])**0.5 
    while True:
        for no_need in range(10):
            active=sorted([sv["average"][i] / len(sv["words"][i]) for i in range(len(sv["average"])) if sv["average"][i] != 0])
            score = (1/(sum(active)/len(active)))**3*len(sv["words"])**0.5 
            stdscr.clear()
            Art = []
            ind = give_word()
            Word = sv["words"][ind]
            for i in Word:
                if i in "äöüÖÜÄß":
                    Art.append(sc[i].split("\n"))
                else:
                    Art.append(text2art(i, "universe").split("\n"))
            Art2 = [[],[],[],[],[],[],[],[],[],[],[],[]]
            for i in Art:
                for j in range(len(i)):
                    Art2[j].append(i[j])
            amount = str(sum(sv["amount"]))
            average = str(int(sv["average"][ind] / len(Word)*100)/100)
            counter = str(tr)
            cp = str(sv["priority"][ind])
            Tm = text2art(str(int(spl*100)/100), "bulbhead").split("\n")
            av = text2art(average, "bulbhead").split("\n")
            Tm2 = text2art(spl_prev, "bulbhead").split("\n")
            scr = text2art(str(int(score*100)/100), "bulbhead").split("\n")
            
            create_header(Tm, Tm2, av, scr, amount, counter, pp, cp)
            
            for i in Art2:
                stdscr.addstr("   ")
                for j in range(len(i)):
                    stdscr.addstr(i[j])
                stdscr.addstr("\n")
            stdscr.refresh()
            while True:
                x=stdscr.getkey()
                if y >= len(Word):
                    y=0
                    break
                if x == chr(27):
                    break
                if x == Word[y]:
                    if y==0:
                        start = time.time()
                    y+=1
                else:
                    continue
                stdscr.clear()
                Tm = text2art(str(int(spl*100)/100), "bulbhead").split("\n")
                if y > 1:
                    Tm2 = text2art(str(int((end1-start)/(y-1)*100)/100), "bulbhead").split("\n")
                else:
                    Tm2 = text2art("----", "bulbhead").split("\n")
                
                create_header(Tm, Tm2, av, scr, amount, counter, pp, cp)
                
                for i in Art2:
                    stdscr.addstr("   ")
                    for j in range(len(i)):
                        if j<y:
                            stdscr.addstr(i[j], curses.A_BLINK)
                        else:
                            stdscr.addstr(i[j])
                    stdscr.addstr("\n")
                end1 = time.time()
                stdscr.refresh()
            if x == chr(27):
                break
            end = time.time()
            speed = end - start
            am = sv["amount"][ind]
            if am > 19:
                am = 19
            sv["average"][ind] = (sv["average"][ind] * am + speed) / (am + 1)
            sv["amount"][ind] += 1
            if sv["amount"][ind] < 10:
                sv["priority"][ind] += 101
                pp = 100
            else:
                add_p = (spl/((speed + sv["average"][ind]*9)/len(Word) + spl*90)*100)** (10 + log(sv["amount"][ind], 10)) 
                sv["priority"][ind] = int((1 + add_p / (1 + abs(add_p)))**30/100)
                pp = sv["priority"][ind]
            spl_prev = str(int(speed / len(Word) * 100) / 100)
            spl = (spl * (1000-len(Word)) + speed)/1000
        
        if x == chr(27):
            stdscr.clear()
            stdscr.addstr("q - quit", curses.A_BLINK)
            stdscr.addstr("   ")
            stdscr.addstr("c - continue", curses.A_BLINK)
            stdscr.addstr("\n")
            while True:
                x=stdscr.getkey()
                if x in "cq":
                    break
                else:
                    stdscr.addstr("\ninvalid input", curses.A_BLINK)
            if x == "q":
                break
            if x == "c":
                y=0
                    
            
                    
                
        
        with open(".conf", "w") as s:
            s.write(str(spl) + ";" + str(tr) + ";" + str(score))

        with open(".save", "w", encoding="utf8") as s:
            sv["out"] = []
            for i in range(len(sv["words"])):
                sv["out"].append(";".join([sv["words"][i],str(sv["amount"][i]),str(sv["average"][i]),str(sv["priority"][i])]))
            s.write("\n".join(sv["out"]))
        
    stdscr.refresh()

main(stdscr)

with open(".conf", "w") as s:
    s.write(str(spl) + ";" + str(tr) + ";" + str(score))

with open(".save", "w", encoding="utf8") as s:
    sv["out"] = []
    for i in range(len(sv["words"])):
        sv["out"].append(";".join([sv["words"][i],str(sv["amount"][i]),str(sv["average"][i]),str(sv["priority"][i])]))
    s.write("\n".join(sv["out"]))

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()