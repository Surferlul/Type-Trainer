import curses
from curses import wrapper, initscr, endwin
from time import sleep, time
from art import text2art
import locale
from math import log
from json import load
from os.path import isfile
from _thread import start_new_thread as nt 
from copy import deepcopy


if not isfile(".chars"):
    print ("There is no character file! Creating .char (cause the program will be slow af otherwhise)...")
    with open(".chars", "w", encoding="utf8") as charf:
        univ_chars = {}
        charf.write("{")
        for i in range(128):
            charf.write(str(i) + ":\"\"\"" + text2art(chr(i), "universal").replace("\"", "\\\"") + "\"\"\",")
        charf.write("}")


if not isfile(".conf"):
    print ("There is no config! Creating config...")
    with open(".conf", "w", encoding="utf8") as cnf:
        cnf.write("0;0;0")

with open(".chars", "r", encoding="utf8") as charf:
    chars = eval(charf.read())

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
    av_speed = float(r[0])
    counter = int(r[1])
    score = float(r[2])

def save_conf(av_speed, counter, score):
    with open(".conf", "w") as s:
        s.write(str(av_speed) + ";" + str(counter) + ";" + str(score))

def save_save(sv, diff):
    for i in diff:
        for  j in diff[i]:
            sv[i][j] = diff[i][j]
    
    with open(".save", "w", encoding="utf8") as s:
        sv["out"] = []
        for i in range(len(sv["words"])):
            sv["out"].append(";".join([sv["words"][i],str(sv["amount"][i]),str(sv["average"][i]),str(sv["priority"][i])]))
        s.write("\n".join(sv["out"]))

def round2(num):
    return int(num * 100) /100

def my_t2a(text, size, do_round=True):
    if size == 0:
        res = [[""] for i in range(12)]
        for i in text:
            tmp = chars[ord(i)].split("\n")
            for j in range(len(tmp)):
                res[j] += tmp[j]
        
        return res
    elif size == 1:
        font = "bulbhead"
    
    if isinstance(text, int):
        text = str(text)
    elif isinstance(text, float):
        if do_round:
            text = str(round2(text))
        else:
            text = str(text)
    elif not isinstance(text, str):
        raise TypeError
    
    return text2art(text, font).split("\n")
    

def strt_scrn():
    stdscr = initscr()
    stdscr.keypad(True)
    return stdscr

def give_word():
    global counter
    while 0 not in [counter % i for i in sv["priority"]]:
        counter+=1
    return [counter % i for i in sv["priority"]].index(0)

def create_header(av_speed_ART, spl_prev_ART, av_speed_word_ART, score_ART, amount, counter, past_priority, current_priority):
    global stdscr
    counter = str(counter)
    amount = str(amount)
    current_priority = str(current_priority)
    past_priority = str(past_priority)
    stdscr.addstr("esc - menu", curses.A_BLINK)
    stdscr.addstr("\n\n")
    
    for i in range(len(spl_prev_ART)):
        stdscr.addstr("   ")
        stdscr.addstr(av_speed_ART[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(av_speed_ART[i])))
        stdscr.addstr(av_speed_word_ART[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(av_speed_word_ART[i])))
        stdscr.addstr(spl_prev_ART[i], curses.A_BLINK)
        stdscr.addstr(" " * (32 - len(spl_prev_ART[i])))
        stdscr.addstr(score_ART[i] + "\n", curses.A_BLINK)
    
    stdscr.addstr("\n   "+ "Total: ")
    stdscr.addstr(amount, curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(amount))+ "Pos: ")
    stdscr.addstr(counter, curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(counter))+ "Prv Pnts: ")
    stdscr.addstr(str(past_priority), curses.A_BLINK)
    stdscr.addstr(" " * (8 - len(past_priority))+ "Crr Pnts: ")
    stdscr.addstr(current_priority, curses.A_BLINK)
    stdscr.addstr("\n\n")

def create_text(Art, y):
    global stdscr
    for i in Art:
        stdscr.addstr("   ")
        for j in range(len(i)):
            if j<y:
                stdscr.addstr(i[j], curses.A_BLINK)
            else:
                stdscr.addstr(i[j])
        stdscr.addstr("\n")

stdscr = strt_scrn()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.use_default_colors()

def main(stdscr):
    global av_speed
    diff = {}
    for i in sv:
        diff[i] = {}
    sv2 = deepcopy(sv)
    curses.start_color()
    curses.use_default_colors()
    active = set()
    for i in range(len(sv["average"])):
        if sv["average"][i] != 0:
            active.add(i)
    stdscr.clear()
    y=0
    x=""
    past_priority = 0
    spl_prev = "----"
    score = (1/(sum([sv["average"][i] for i in active])/len(active)))**3*len(sv["words"])**0.5 
    while True:
        for no_need in range(10):

            score = (1/(sum([sv["average"][i] / len(sv["words"][i]) for i in active])/len(active)))**3*len(sv["words"])**0.5 
            
            stdscr.clear()
            
            Art = []
            ind = give_word()
            active.add(ind)
            Word = sv["words"][ind]
            
            for i in Word:
                if i in "äöüÖÜÄß":
                    Art.append(sc[i].split("\n"))
                else:
                    Art.append(chars[ord(i)].split("\n"))
            Art2 = [[] for i in range (12)]
            
            for i in Art:
                for j in range(len(i)):
                    Art2[j].append(i[j])
            Art = Art2
            
            amount              = sum(sv["amount"])
            av_speed_word       = sv["average"][ind] / len(Word)
            current_priority    = sv["priority"][ind]
            
            av_speed_ART        = my_t2a(av_speed, 1)
            av_speed_word_ART   = my_t2a(av_speed_word, 1)
            spl_prev_ART        = my_t2a(spl_prev, 1)
            score_ART           = my_t2a(score, 1)
            
            create_header(av_speed_ART, spl_prev_ART, av_speed_word_ART, score_ART, amount, counter, past_priority, current_priority)
            
            create_text(Art, 0)
           
            while True:
                x=stdscr.getkey()
                if y >= len(Word):
                    y=0
                    break
                if x == chr(27):
                    break
                elif x == Word[y]:
                    if y==0:
                        start = time()
                    y+=1
                else:
                    continue
                stdscr.clear()
                av_speed_ART = my_t2a(av_speed, 1)
                if y > 1:
                    spl_prev_ART = my_t2a((end1-start)/(y-1), 1)
                else:
                    spl_prev_ART = my_t2a("----", 1)
                
                create_header(av_speed_ART, spl_prev_ART, av_speed_word_ART, score_ART, amount, counter, past_priority, current_priority)
                
                create_text(Art, y)
                
                end1 = time()
            if x == chr(27):
                break
            end = time()
            speed = end - start
            am = sv["amount"][ind]
            if am > 19:
                am = 19
            sv["average"][ind] = (sv["average"][ind] * am + speed) / (am + 1)
            diff["average"][ind] = sv["average"][ind]
            sv["amount"][ind] += 1
            diff["amount"][ind] = sv["amount"][ind]
            if sv["amount"][ind] < 10:
                sv["priority"][ind] += 101
                past_priority = 100
            else:
                add_p = (av_speed/((speed + sv["average"][ind]*9)/len(Word) + av_speed*90)*100)** (10 + log(sv["amount"][ind], 10)) 
                sv["priority"][ind] = int((1 + add_p / (1 + abs(add_p)))**30/100)
                past_priority = sv["priority"][ind]
            diff["priority"][ind] = sv["priority"][ind]
            diff["words"][ind] = sv["words"][ind]
            spl_prev = speed / len(Word)
            av_speed = (av_speed * (1000-len(Word)) + speed)/1000
        
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
                    

        nt(save_conf, (av_speed, counter, score))
        nt(save_save, (sv2, deepcopy(diff)))

main(stdscr)

with open(".conf", "w") as s:
    s.write(str(av_speed) + ";" + str(counter) + ";" + str(score))

with open(".save", "w", encoding="utf8") as s:
    sv["out"] = []
    for i in range(len(sv["words"])):
        sv["out"].append(";".join([sv["words"][i],str(sv["amount"][i]),str(sv["average"][i]),str(sv["priority"][i])]))
    s.write("\n".join(sv["out"]))

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()