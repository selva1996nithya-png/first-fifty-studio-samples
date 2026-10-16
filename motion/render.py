"""Original deterministic motion graphics; no generative video or stock footage."""
from pathlib import Path
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H, FPS, SECONDS = 1080, 1350, 24, 26
BG, PANEL, INK = '#102C36', '#183B46', '#F4F0E5'
TEAL, GOLD, MUTED = '#4FD2C4', '#F6C478', '#AAC4C7'
REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n, bold=False): return ImageFont.truetype(BOLD if bold else REG, n)
F = {n: font(n) for n in [23, 26, 28, 30, 32, 36, 40]}
FB = {n: font(n, True) for n in [28, 34, 38, 48, 62, 66, 70]}
def ease(v):
    v=max(0,min(1,v)); return v*v*(3-2*v)
def lines(d, pos, value, face, fill=INK, gap=12):
    x,y=pos
    for line in value.split('\n'):
        assert d.textbbox((0,0),line,font=face)[2] <= W-x-60, line
        d.text((x,y),line,font=face,fill=fill)
        y += face.size+gap
def frame(t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((65,50),'FIRST FIFTY STUDIO  /  COASTAL EXPLAINER',font=F[26],fill=MUTED)
    d.line((65,105,1015,105),fill='#41606A',width=2)
    scene=0 if t<5 else 1 if t<12 else 2 if t<19 else 3
    labels=['THE SETUP','WHY','THE COMBINATION','HOW LONG']
    d.text((65,145),labels[scene],font=FB[28],fill=GOLD)
    if scene==0:
        lines(d,(60,202),'THE TIDE\nSTARTS HIGHER.',FB[70],gap=4)
        lines(d,(65,397),'Why El Niño can amplify\nWest Coast coastal flooding.',F[36],gap=10)
    elif scene==1:
        lines(d,(60,202),'A HIGHER\nSTARTING POINT.',FB[66],gap=6)
        lines(d,(65,397),'Kelvin waves can temporarily\nraise coastal sea level. [1]',F[36])
    elif scene==2:
        lines(d,(60,202),'THEN COMES\nTHE HIGH TIDE.',FB[66],gap=6)
        lines(d,(65,397),'Elevated water + high tides + storms\ncan increase flooding and erosion. [1]',F[32])
    else:
        lines(d,(60,202),'THIS WINTER\nIS THE WATCHPOINT.',FB[62],gap=6)
        lines(d,(65,387),'Strong-to-very strong El Niño likely\nthrough Jan–Mar 2027. [2]',F[32],gap=10)
    d.rounded_rectangle((60,545,1020,1020),radius=32,fill=PANEL)
    # Diagram is explicitly schematic; the moving line does not predict a tide height.
    d.text((90,570),'SCHEMATIC · NOT TO SCALE',font=F[23],fill=MUTED)
    quay=795
    rise=60*ease((t-5)/4)
    tide=80*ease((t-12)/5)
    level=885-rise-tide
    if scene==0: level=885-20*ease(t/5)
    d.polygon([(745,quay),(990,quay),(990,985),(745,985)],fill='#52646A')
    d.rectangle((765,quay-50,820,quay),fill='#C6D3CE')
    d.rectangle((846,quay-88,914,quay),fill='#C6D3CE')
    d.rectangle((935,quay-43,975,quay),fill='#C6D3CE')
    d.line((745,quay,992,quay),fill=GOLD,width=5)
    # Animated shallow pulse arriving from the left.
    wave=[]
    for x in range(90,746,4):
        y=level+7*math.sin(x/60-t*1.6)+4*math.sin(x/31+t)
        wave.append((x,y))
    d.polygon(wave+[(745,985),(90,985)],fill='#146B79')
    d.line(wave,fill=TEAL,width=5)
    warm=[(x,y+23+5*math.sin(x/100-t)) for x,y in wave]
    d.line(warm,fill='#F3B866',width=7)
    if level<quay:
        d.rectangle((745,int(level),990,quay+5),fill='#258C99')
        d.line((745,int(level),990,int(level)),fill=TEAL,width=5)
    d.line((90,885,733,885),fill=MUTED,width=2)
    d.text((100,908),'reference water level',font=F[23],fill=MUTED)
    if scene in [0,1]:
        d.text((100,650),'SAN FRANCISCO',font=FB[28],fill=INK)
        d.text((100,692),'~6 in',font=FB[62],fill=GOLD)
        d.text((310,717),'above normal [1]',font=F[28],fill=INK)
        d.text((100,774),'Reported 5 Oct 2026',font=F[26],fill=MUTED)
    elif scene==2:
        d.text((100,650),'SMALL LIFT.',font=FB[38],fill=GOLD)
        d.text((100,700),'LESS ROOM AT HIGH TIDE.',font=FB[28],fill=INK)
    else:
        d.text((100,650),'KING TIDES PEAK [1]',font=FB[28],fill=GOLD)
        for i,m in enumerate(['NOV','DEC','JAN','FEB']):
            x=100+i*145
            d.rounded_rectangle((x,705,x+125,765),radius=12,fill='#2D6570')
            d.text((x+22,719),m,font=FB[28],fill=INK)
        d.text((100,794),'Risk rises when the drivers overlap.',font=F[28],fill=INK)
    if scene==3:
        lines(d,(65,1050),'HIGHER BASELINE. HIGHER TIDE.\nA SMALLER MARGIN.',FB[34],gap=5)
    else:
        d.text((65,1055),'A Kelvin wave is not a tsunami. [1]',font=F[32],fill=INK)
    d.text((65,1168),'[1] SFist · 5 Oct 2026 · SF tides & Kelvin waves',font=F[26],fill=MUTED)
    d.text((65,1212),'[2] NOAA CPC · 8 Oct 2026 · ENSO discussion',font=F[26],fill=MUTED)
    d.text((65,1262),'Source snapshot: 16 Oct 2026 · Links in sources.md',font=F[23],fill=MUTED)
    d.rectangle((0,1338,int(W*t/SECONDS),1349),fill=GOLD)
    return im

def main():
    OUT.mkdir(exist_ok=True)
    target=OUT/'higher-baseline.mp4'
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    cmd=[ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL) as process:
        for i in range(SECONDS*FPS):process.stdin.write(frame(i/FPS).tobytes())
        process.stdin.close(); assert process.wait()==0
    times=[2,9,16,23]
    sheet=Image.new('RGB',(W*2,H*2),BG)
    for i,t in enumerate(times):
        f=frame(t);f.save(OUT/f'frame-{t:02d}.png');sheet.paste(f,((i%2)*W,(i//2)*H))
    sheet.thumbnail((1080,1350));sheet.save(OUT/'contact-sheet.png')
    print(target)

if __name__=='__main__':main()
