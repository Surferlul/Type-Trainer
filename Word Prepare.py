from random import randint

srt = input("first x sorted words (default:0,-1 for all):")
if srt:
    srt = int(srt)
else:
    srt=0
fl = input("file with words (default:./.words)")
if fl:
    pass
else:
    fl=".words"
otp = input("output save-file (default:./.save)")
if otp:
    pass
else:
    otp=".save"

sv = []

with open(fl, "r", encoding="utf8") as f:
    wrds = f.read().split("\n")
if srt < 0:
    srt = len(wrds)
x=0
for i in range (len(wrds)):
    if x > (srt-1) * 100:
        x=randint(srt*100, len(wrds)*100)
    else:
        x+=100
    sv.append([])
    sv[i].append(wrds[i])
    sv[i].append("0") #how often already
    sv[i].append("0") #how long on average
    sv[i].append(str(x)) #priority
with open(otp, "w", encoding="utf8") as o:
    for i in range(len(sv)):
        sv[i] = ";".join(sv[i])
    o.write("\n".join(sv))