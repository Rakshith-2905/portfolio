import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"; RED="#9B3B2E"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,
 "figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":LINE,"savefig.dpi":200})
rng=np.random.default_rng(11); out={}
sig=lambda z:1/(1+np.exp(-z)); logit=lambda p:np.log(p/(1-p))
def ece(p,y,M=15):
    b=np.minimum((p*M).astype(int),M-1); e=0
    for m in range(M):
        k=b==m
        if k.any(): e+=k.mean()*abs(p[k].mean()-y[k].mean())
    return e
# ---- Fig 1: published numbers
fig,ax=plt.subplots(1,3,figsize=(13,4.3),gridspec_kw={"width_ratios":[1.6,0.8,1]})
a=ax[0]; names=["ResNet-110\nCIFAR-100","ResNet-110\nCIFAR-10","ResNet-152\nImageNet","DenseNet-161\nImageNet"]
pre=[16.53,4.6,5.48,6.28]; post=[1.26,0.83,1.86,1.99]; x=np.arange(4)
a.bar(x-0.2,pre,0.38,color=RED,label="as trained"); a.bar(x+0.2,post,0.38,color=NAVY,label="after temperature scaling (1 parameter)")
for i in range(4): a.text(x[i]-0.2,pre[i]+0.3,f"{pre[i]:g}",ha="center",fontsize=9); a.text(x[i]+0.2,post[i]+0.3,f"{post[i]:g}",ha="center",fontsize=9)
a.set_xticks(x); a.set_xticklabels(names,fontsize=9); a.set_ylabel("Expected calibration error (%)"); a.legend(frameon=False,fontsize=9); a.grid(axis="x",visible=False)
a.set_title("Accurate networks, overconfident scores\n(Guo et al. 2017)",loc="left",fontsize=10.5,color=INK)
a=ax[1]; a.bar([0,1],[0.007,0.074],color=[NAVY,RED],width=0.6)
for i,v in enumerate([0.007,0.074]): a.text(i,v+0.002,f"{v}",ha="center",fontsize=10)
a.set_xticks([0,1]); a.set_xticklabels(["pre-trained","after RLHF"]); a.set_ylabel("ECE on an MMLU subset"); a.grid(axis="x",visible=False)
a.set_title("GPT-4: post-training\nhurts calibration",loc="left",fontsize=10.5,color=INK)
a=ax[2]; a.plot([0,0],[54.3,93.4],color=GOLD,lw=10,solid_capstyle="butt"); a.scatter([0,0],[54.3,93.4],color=INK,zorder=5)
a.text(0.08,93.4,"93.4%: one ordering",va="center",fontsize=10); a.text(0.08,54.3,"54.3%: another ordering",va="center",fontsize=10)
a.axhline(50,color=MUTED,ls=":",lw=1); a.text(0.08,50.8,"chance",fontsize=9,color=MUTED)
a.set_xlim(-0.3,1.2); a.set_ylim(45,100); a.set_xticks([]); a.set_ylabel("SST-2 accuracy, GPT-3 2.7B, 4-shot")
a.set_title("Same examples, different order\n(Zhao et al. 2021)",loc="left",fontsize=10.5,color=INK)
fig.tight_layout(); fig.savefig("latent-evidence.png"); plt.close(fig)
# ---- Fig 2: base rate
fig,ax=plt.subplots(figsize=(8,4.4))
pi=np.logspace(-3,np.log10(0.5),300)
for s,c in [(0.9,RED),(0.95,GOLD),(0.99,NAVY)]:
    ppv=s*pi/(s*pi+(1-s)*(1-pi)); ax.plot(pi*100,ppv*100,color=c,lw=2.2,label=f"{int(s*100)}% sensitivity and specificity")
ax.set_xscale("log"); ax.set_xlabel("How common the class is in deployment (%)"); ax.set_ylabel("% of positive calls that are correct")
p2=0.9*0.02/(0.9*0.02+0.1*0.98); out["ppv2"]=p2
ax.scatter([2],[p2*100],color=RED,zorder=5); ax.annotate(f"at 2%: {p2*100:.0f}% of alarms are real",(2,p2*100),textcoords="offset points",xytext=(10,-4),fontsize=10)
ax.legend(frameon=False,fontsize=9.5,loc="upper left"); ax.set_xticks([0.1,1,10,50]); ax.set_xticklabels(["0.1","1","10","50"])
ax.set_title("A '90% accurate' classifier, deployed where the class is rare",loc="left",fontsize=11,color=INK)
fig.tight_layout(); fig.savefig("latent-baserate.png"); plt.close(fig)
# ---- Fig 3: how many labels does calibration need?
N=20000; T0=2.5
def sample(n):
    p=rng.beta(1.2,1.2,n); y=(rng.random(n)<p).astype(float); z=T0*logit(np.clip(p,1e-4,1-1e-4)); return z,y
zt,yt=sample(N)
def fitT(z,y):
    f=lambda T: -np.mean(y*np.log(sig(z/T)+1e-12)+(1-y)*np.log(1-sig(z/T)+1e-12))
    return minimize_scalar(f,bounds=(0.2,10),method="bounded").x
ns=[10,20,50,100,200,500,1000,5000]; med=[];lo=[];hi=[]
for n in ns:
    e=[]
    for r in range(200):
        z,y=sample(n); T=fitT(z,y); e.append(ece(sig(zt/T),yt))
    e=np.array(e)*100; med.append(np.median(e)); lo.append(np.percentile(e,10)); hi.append(np.percentile(e,90))
raw=ece(sig(zt),yt)*100; out["raw"]=raw; out["ns"]=dict(zip(ns,np.round(med,2))); out["hi"]=dict(zip(ns,np.round(hi,2)))
fig,(a,b)=plt.subplots(1,2,figsize=(12,4.4))
a.axhline(raw,color=RED,lw=2,label=f"no calibration: {raw:.1f}%"); a.fill_between(ns,lo,hi,color=NAVY,alpha=0.18,lw=0)
a.plot(ns,med,color=NAVY,lw=2.2,marker="o",label="temperature fit on n labels (median, 10–90%)")
a.set_xscale("log"); a.set_xlabel("Labelled examples used to calibrate"); a.set_ylabel("ECE on held-out data (%)"); a.legend(frameon=False,fontsize=9.5)
a.set_title("Calibration needs hundreds of labels, not thousands",loc="left",fontsize=11,color=INK)
z,y=sample(200); T=fitT(z,y); out["T200"]=T
bins=np.linspace(0,1,11); c=(bins[:-1]+bins[1:])/2
for pp,col,lab in [(sig(zt),RED,"raw scores"),(sig(zt/T),NAVY,f"after T = {T:.2f} fit on 200 labels")]:
    idx=np.digitize(pp,bins[1:-1]); acc=[yt[idx==i].mean() if (idx==i).any() else np.nan for i in range(10)]; conf=[pp[idx==i].mean() if (idx==i).any() else np.nan for i in range(10)]
    b.plot(conf,acc,marker="o",color=col,lw=2,label=lab)
b.plot([0,1],[0,1],color=MUTED,ls=":",lw=1); b.set_xlabel("Stated confidence"); b.set_ylabel("Observed frequency"); b.legend(frameon=False,fontsize=9.5)
b.set_title("Reliability diagram: overconfident, then fixed",loc="left",fontsize=11,color=INK)
fig.tight_layout(); fig.savefig("latent-calibration.png"); plt.close(fig)
print(out)
