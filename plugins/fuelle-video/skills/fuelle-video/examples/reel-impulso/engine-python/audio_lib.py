import numpy as np, math
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=48000; DUR=35.0; N=int(SR*DUR)
rng=np.random.default_rng(3)
mus=np.zeros(N); sfx=np.zeros(N)
def add(buf,t,x,g=1.0):
    i=int(t*SR); j=min(N,i+len(x))
    if i<N: buf[i:j]+=x[:j-i]*g
def env(n,a=0.002,d=0.2):
    t=np.arange(n)/SR; e=np.exp(-t/d); na=int(a*SR)
    if na>0: e[:na]*=np.linspace(0,1,na)
    return e
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'band',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def lp(x,f): return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def noise(d): return rng.standard_normal(int(d*SR))
def tone(f0,f1,d,decay,shape='sine'):
    n=int(d*SR); t=np.arange(n)/SR
    f=f0*(f1/f0)**(t/d); ph=2*np.pi*np.cumsum(f)/SR
    w=np.sin(ph) if shape=='sine' else (2*((ph/(2*np.pi))%1)-1)
    return w*env(n,0.002,decay)
# ---------- instrumentos ----------
def kick():
    x=tone(140,42,0.35,0.12); c=hp(noise(0.01),3000)*env(480,0.0,0.002)*0.3; x[:480]+=c; return x
def hat(): return hp(noise(0.06),7000)*env(int(0.06*SR),0.0005,0.012)*0.35
def clap():
    x=bp(noise(0.18),900,3000)*env(int(0.18*SR),0.001,0.05)
    return x*0.6
def bass(f,d=0.22): return lp(tone(f,f,d,0.09,'saw'),400)*0.55
def pluck(f,d=0.3): return (tone(f,f,d,0.08)+0.4*tone(2*f,2*f,d,0.05))*0.25
