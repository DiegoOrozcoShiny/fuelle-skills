import numpy as np, math, random
from scipy.io import wavfile
exec(open('/home/claude/audio_lib.py').read())
from fuelle6 import to_new as TN
# ---------- música: urgencia · ansiedad · misterio ----------
SIL=(12.30,12.90)
def saw(f,d):
    n=int(d*SR); t=np.arange(n)/SR; return 2*((f*t)%1)-1
def drone(t0,t1,freqs,cut0,cut1,g):
    d=t1-t0; n=int(d*SR); x=np.zeros(n); tt=np.arange(n)/SR
    for f in freqs:
        for det in (-0.6,0.6): x+=saw(f+det,d)[:n]
    # filtro que se abre: bloques con distinto corte
    out=np.zeros(n); blk=int(0.25*SR)
    for i in range(0,n,blk):
        u=i/n; fc=cut0+(cut1-cut0)*u
        seg=x[max(0,i-4000):i+blk]; out[i:i+blk]=lp(seg,fc)[-len(out[i:i+blk]):]
    lfo=0.75+0.25*np.sin(2*np.pi*0.5*tt)
    fade=np.minimum(1,np.minimum(tt/0.3,(d-tt)/0.3))
    add(mus,t0,out*lfo*fade/len(freqs)*g)
def pad(t0,t1,freqs,g):
    d=t1-t0; n=int(d*SR); tt=np.arange(n)/SR; x=np.zeros(n)
    for f in freqs: x+=np.sin(2*np.pi*f*tt)*(0.6+0.4*np.sin(2*np.pi*5.5*tt+f))
    fade=np.minimum(1,np.minimum(tt/1.0,(d-tt)/0.5))
    add(mus,t0,x*fade/len(freqs)*g)
def tick_clock(t,hi): add(mus,t,bp(noise(0.03),2800 if hi else 1900,5200 if hi else 3400)*env(int(0.03*SR),0.0005,0.006),0.55)
def heart(t,g=1.0):
    add(mus,t,tone(70,40,0.25,0.07),0.95*g); add(mus,t+0.16,tone(62,38,0.22,0.06),0.6*g)
def stab(t,f,g=1.0,d=0.11): add(mus,t,lp(saw(f,d)*env(int(d*SR),0.002,0.035),1800),0.32*g)
def swell(t1,d,g=0.5):  # ruido en reversa que crece hacia un corte
    n=int(d*SR); x=hp(noise(d),600)*np.linspace(0,1,n)**3; add(mus,t1-d,x,g)
def snare(t,g): add(mus,t,bp(noise(0.12),1200,5000)*env(int(0.12*SR),0.001,0.04),0.5*g)
D,Eb,F,G,A,Bb,C=73.42,77.78,87.31,98.0,110.0,116.54,65.41
# drones por sección
drone(0.0,10.6,[36.71,55.0,38.89],180,700,0.55)          # D-A-Eb: disonancia de segunda menor
drone(10.6,12.3,[36.71,38.89],150,250,0.45)
drone(12.9,16.6,[36.71,55.0,38.89],300,1100,0.6)
drone(16.6,28.4,[36.71,55.0,73.42],250,900,0.5)          # se resuelve a D-A (sin Eb), sigue tenso
drone(28.4,31.9,[36.71,55.0,38.89,51.91],300,1600,0.65)   # tritono para el clímax
drone(31.9,35.0,[36.71,55.0,73.42],900,200,0.6)
pad(0.0,12.3,[587.3,622.3],0.10); pad(12.9,16.6,[587.3,622.3,830.6],0.12); pad(28.4,31.9,[587.3,622.3,415.3],0.12)
pad(16.6,28.4,[587.3,880.0],0.07); pad(31.9,35.0,[587.3,880.0,440.0],0.10)
S16=0.125
probl=[D,D,Eb,D,F,D,Eb,C]; sol=[D,F,A,D*2,A,F,G,A]; clim=[D,Eb,D,Eb,F,Eb,G,F]
k=0; t=0.0
while t<34.6:
    inSil = SIL[0]-0.05<=t<SIL[1]
    if not inSil:
        if 10.6<=t<SIL[0]:
            if k%4==0: tick_clock(t, (k//4)%2==0)
        else:
            if k%2==0: tick_clock(t,(k//2)%2==0)
            if k%4==0 and t<31.9: heart(t, 0.8 if t<16.6 else 0.6)
            if t>=3.0 and t<31.9:
                pat = probl if (t<16.6) else (sol if t<28.4 else clim)
                gain = 0.6+0.4*min(1,(t-3.0)/7) if t<16.6 else (0.75 if t<28.4 else 1.0)
                stab(t, pat[k%8]*2, gain)
                if t>=12.9 and t<16.6 and k%2==1: stab(t, pat[(k+3)%8]*4, 0.35, 0.06)
    t=round(t+S16,4); k+=1
# redoble que acelera hacia el logo (28.4 -> 31.9)
tt=28.4
while tt<31.85:
    u=(tt-28.4)/3.5; snare(tt,0.25+0.75*u); tt+= 0.25*(1-u)+0.04
# reloj final que se detiene antes del CTA
for i,t in enumerate(np.arange(31.95,34.6,0.5)): tick_clock(float(t), i%2==0)
for t1 in (7.3,16.6,20.1,28.4,31.9): swell(t1,0.9,0.45)
add(mus,31.9,tone(55,30,2.5,0.9),1.0)   # golpe grave del logo
mus[int(34.2*SR):]*=np.linspace(1,0,N-int(34.2*SR))**2
mus[int(SIL[0]*SR):int(SIL[1]*SR)]=0
# ---------- SFX (tiempos del storyboard convertidos a la línea nueva) ----------
def hit(t,g=1.0):
    add(sfx,t,tone(90,38,0.5,0.18),0.9*g); add(sfx,t,lp(noise(0.12),2500)*env(int(0.12*SR),0.0,0.03),0.5*g)
def tick(t,f=2400,g=0.35): add(sfx,t,tone(f,f*0.8,0.03,0.008),g)
def whoosh(t,d,up=True,g=0.6):
    n=int(d*SR); x=noise(d); out=np.zeros(n); seg=int(SR*0.01)
    for i in range(0,n,seg):
        u=i/n; fc=(300+5000*u) if up else (5000-4700*u)
        out[i:i+seg]=bp(x[max(0,i-2000):i+seg],fc*0.7,fc*1.3)[-len(out[i:i+seg]):]
    add(sfx,t,out*np.sin(np.linspace(0,np.pi,n))**1.5,g)
def golf_tock(t,g=1.0):
    add(sfx,t,bp(noise(0.05),1800,4500)*env(int(0.05*SR),0.0,0.006),1.2*g); add(sfx,t,tone(1150,950,0.08,0.02),0.45*g)
def thump(t,g=1.0): add(sfx,t,tone(110,55,0.3,0.08),0.9*g); add(sfx,t,lp(noise(0.05),1200)*env(int(0.05*SR),0,0.01),0.4*g)
def ding(t,g=1.0):
    n=int(1.8*SR); tt=np.arange(n)/SR; x=np.zeros(n)
    for fr,a,d in [(1318.5,1,0.9),(2637,0.35,0.5),(3950,0.15,0.3),(1975.5,0.2,0.6)]: x+=a*np.sin(2*np.pi*fr*tt)*np.exp(-tt/d)
    add(sfx,t,x*0.35*g)
def riser(t,d,f0,f1,g=0.25): add(sfx,t,lp(tone(f0,f1,d,10,'saw'),3000)*np.linspace(0.2,1,int(d*SR)),g)
O=TN
for ta in (0.35,1.15,1.95):
    riser(ta,0.2,220,660,0.2); add(sfx,ta+0.34,tone(500,80,0.25,0.08),0.5); thump(ta+0.46,0.6)
for to in (3.0,7.0,15.0,19.0,24.2,27.4): hit(O(to),0.8)
for ta in (3.10,3.85,4.75,5.85):
    whoosh(O(ta),0.22,False,0.25); golf_tock(O(ta+0.22)); golf_tock(O(ta+0.38),0.45); golf_tock(O(ta+0.46),0.15)
riser(O(7.15),O(8.55)-O(7.15),180,1100,0.2)
whoosh(O(9.45),O(10.0)-O(9.45),True,0.8); hit(O(10.0),0.6)
add(sfx,O(10.55),tone(700,350,0.12,0.04),0.35)   # giro de la mano
hit(O(11.5),1.2)
r=random.Random(7)
for k in range(24): tick(O(11.6+2.2*((k+1)/24)**(1/0.8)),r.choice([1600,2000,2400,2800]),0.22)
whoosh(O(16.0),0.25,False,0.5); thump(O(16.2),0.8)
for k in range(6): thump(O(16.6+0.33*k),0.55); tick(O(16.6+0.33*k),2600,0.2)
for i in range(4): tick(O(19.5+i*0.5),1200,0.25)
for i,ta in enumerate((22.05,22.65,23.25,23.75)):
    thump(O(ta),1.0); add(sfx,O(ta+0.17),tone(1400+i*200,1900+i*200,0.09,0.03),0.3)
y0,y1=560,1330
g=lambda u: y1-110-(y1-y0-240)*(1-u)**1.6; v=lambda u: y1-130-(y1-y0-240)*u**1.4
uc=min([i/400 for i in range(401)],key=lambda u:abs(g(u)-v(u))); tc=O(24.25+uc)
riser(O(24.25),tc-O(24.25),300,900,0.15); ding(tc,1.0)
hit(O(26.0),1.0)
for ta in (26.05,26.25,26.45,26.65,26.85): whoosh(O(ta),0.3,False,0.2)
thump(O(27.0),0.9); add(sfx,O(27.0),hp(noise(0.15),2000)*env(int(0.15*SR),0.001,0.04),0.35)
for s_ in range(4): thump(O(27.45+s_*0.33),0.5)
for s_ in range(6): add(sfx,O(27.5+s_*0.1),tone(400*1.19**s_,400*1.19**s_,0.06,0.02),0.3)
hit(O(28.9),1.3); add(sfx,O(28.9),hp(noise(1.2),5000)*env(int(1.2*SR),0.01,0.35),0.12)
add(sfx,O(30.2),tone(880,1320,0.08,0.03),0.35); thump(O(30.2),0.5)
# ---------- voz + ducking ----------
sr,vo=wavfile.read('/home/claude/voice.wav'); vo=vo.astype(np.float32)/32768
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]
voice=voice/np.max(np.abs(voice))*0.9
e=np.abs(voice); 
from scipy.ndimage import maximum_filter1d, uniform_filter1d
e=uniform_filter1d(maximum_filter1d(e,int(0.08*SR)),int(0.25*SR)); e=np.clip(e/np.percentile(e,95),0,1)
duck=1-0.6*e
musn=mus/np.max(np.abs(mus)); sfxn=sfx/np.max(np.abs(sfx))
mix=voice*1.0 + musn*0.34*duck + sfxn*0.42*(1-0.35*e)
mix=np.tanh(mix*1.1)/np.tanh(1.1); mix=mix/np.max(np.abs(mix))*0.93
st=np.stack([mix,mix],1)
wavfile.write('/home/claude/mix7.wav',SR,(st*32767).astype(np.int16))
nv=musn*0.30+sfxn*0.42; nv=nv/np.max(np.abs(nv))*0.9
wavfile.write('/home/claude/musica_sfx7.wav',SR,(np.stack([nv,nv],1)*32767).astype(np.int16))
print('ok tc',round(tc,3))
