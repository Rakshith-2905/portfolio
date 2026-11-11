import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"; RED="#9B3B2E"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,
 "xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,
 "axes.spines.right":False,"axes.grid":True,"grid.color":LINE,"grid.linewidth":0.8,"savefig.dpi":200})
rng=np.random.default_rng(7)
out={}

# ---------- Fig 1: evidence ----------
fig,(a,b)=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={"width_ratios":[1.25,1]})
rows=[("Story similarity, writers given one AI idea\nDoshi & Hauser 2024, N=300",10.7),
      ("India–US essay similarity, 0.48 → 0.54\nAgarwal et al. 2025, N=118",(0.54/0.48-1)*100),
      ("Loss of unique key points (threshold 0.6)\nPadmakumar & He 2024, InstructGPT vs solo",(1-0.877/0.941)*100),
      ("Loss of unique 4-grams\nPadmakumar & He 2024, InstructGPT vs solo",(1-0.953/0.973)*100)]
y=np.arange(len(rows))[::-1]
a.barh(y,[r[1] for r in rows],color=NAVY,height=0.55)
for yi,r in zip(y,rows): a.text(r[1]+0.3,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
a.set_yticks(y); a.set_yticklabels([r[0] for r in rows],fontsize=9.5)
a.set_xlabel("Convergence: % more similar, or % less diverse"); a.set_xlim(0,15); a.grid(axis="y",visible=False)
a.set_title("Measured convergence when people write with an LLM",loc="left",fontsize=11.5,color=INK)
rows2=[("CS arXiv abstracts, Feb 2024\nLiang et al. 2024",17.5),("Biomedical abstracts, 2024 (lower bound)\nKobak et al. 2024",13.5),
       ("Nature-portfolio abstracts, Feb 2024\nLiang et al. 2024",6.3),("Math arXiv abstracts, Feb 2024\nLiang et al. 2024",4.9)]
y2=np.arange(len(rows2))[::-1]
b.barh(y2,[r[1] for r in rows2],color=GOLD,height=0.55)
for yi,r in zip(y2,rows2): b.text(r[1]+0.3,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
b.set_yticks(y2); b.set_yticklabels([r[0] for r in rows2],fontsize=9.5); b.set_xlim(0,22); b.grid(axis="y",visible=False)
b.set_xlabel("Estimated % of abstracts")
b.set_title("Share of published text already LLM-modified",loc="left",fontsize=11.5,color=INK)
fig.tight_layout(); fig.savefig("oped-evidence.png"); plt.close(fig)

# ---------- Fig 2: temperature sharpening ----------
V=10000; s=1.1; r=np.arange(1,V+1); q=r**-s; q/=q.sum()
def sharpen(p,T):
    l=np.log(p)/T; l-=l.max(); e=np.exp(l); return e/e.sum()
def H(p): p=p[p>0]; return -(p*np.log(p)).sum()
Ts=np.linspace(0.3,1.5,121)
eff=[np.exp(H(sharpen(q,T))) for T in Ts]; top10=[sharpen(q,T)[:10].sum() for T in Ts]
tail=[sharpen(q,T)[100:].sum() for T in Ts]
for T in [1.0,0.8,0.7,0.5]:
    p=sharpen(q,T); out[f"T{T}"]=(np.exp(H(p)),p[:10].sum(),p[100:].sum())
fig,(a,b)=plt.subplots(1,2,figsize=(12,4.3))
a.plot(Ts,eff,color=NAVY,lw=2.2); a.set_yscale("log")
for T in [1.0,0.7]:
    v=np.exp(H(sharpen(q,T))); a.scatter([T],[v],color=GOLD,zorder=5); a.annotate(f"T={T}: {v:,.0f}",(T,v),textcoords="offset points",xytext=(8,-14),color=INK,fontsize=10)
a.set_xlabel("Sampling temperature T"); a.set_ylabel("Effective number of phrasings, exp(H)")
a.set_title("Lower temperature collapses the space of phrasings",loc="left",fontsize=11.5,color=INK)
b.plot(Ts,np.array(top10)*100,color=NAVY,lw=2.2,label="share of 10 most common phrasings")
b.plot(Ts,np.array(tail)*100,color=RED,lw=2.2,label="share beyond the top 100 (the tail)")
b.axvline(1,color=MUTED,ls=":",lw=1); b.set_xlabel("Sampling temperature T"); b.set_ylabel("% of probability mass")
b.legend(frameon=False,fontsize=9.5); b.set_title("Mass moves from the tail to the head",loc="left",fontsize=11.5,color=INK)
fig.tight_layout(); fig.savefig("oped-temperature.png"); plt.close(fig)

# ---------- Fig 3: recursive Gaussian fitting ----------
G=2000; R=400
fig,a=plt.subplots(figsize=(8.5,4.4))
cols={20:RED,100:GOLD,1000:NAVY}
for n,c in cols.items():
    sig=np.ones(R); mu=np.zeros(R); traj=[np.ones(R)]
    for t in range(G):
        x=rng.normal(mu[:,None],sig[:,None],size=(R,n))
        mu=x.mean(1); sig=x.std(1)   # MLE
        traj.append(sig.copy())
    traj=np.array(traj)**2
    med=np.median(traj,1); lo,hi=np.percentile(traj,[10,90],axis=1)
    g=np.arange(G+1)
    a.fill_between(g,lo,hi,color=c,alpha=0.15,lw=0); a.plot(g,med,color=c,lw=2,label=f"n = {n:,} samples per generation")
    out[f"n{n}"]=(med[100],med[1000],med[2000],(traj[2000]<0.5).mean())
    a.plot(g,np.exp(-2*g/n),color=c,ls="--",lw=1)
a.set_yscale("log"); a.set_ylim(1e-6,2); a.set_xlabel("Generation (each model trained only on the previous model's output)")
a.set_ylabel("Variance relative to the original, σ²ₜ / σ²₀")
a.set_title("Training on your own output: the tails go first",loc="left",fontsize=11.5,color=INK)
a.legend(frameon=False,fontsize=9.5,loc="lower left"); a.text(G*0.62,1.2,"dashed: e^(−2t/n), the median predicted by theory",color=MUTED,fontsize=9)
fig.tight_layout(); fig.savefig("oped-collapse.png"); plt.close(fig)

# ---------- Fig 4: feedback loop with fresh human data ----------
N=50000; T=0.9; Gen=60
alphas=[0.0,0.25,0.5,0.75,0.9,1.0]
fig,(a,b)=plt.subplots(1,2,figsize=(12,4.3))
cmap=plt.get_cmap("cividis")
fin={}
for i,al in enumerate(alphas):
    corpus=q.copy(); E=[np.exp(H(corpus))]; TL=[corpus[100:].sum()]
    for t in range(Gen):
        counts=rng.multinomial(N,corpus); p=counts/N               # train on a finite corpus
        model=np.zeros(V); nz=p>0; model[nz]=sharpen(p[nz],T)      # decode with T<1; unseen ideas get zero mass
        corpus=(1-al)*q+al*model                                   # next corpus: fresh human + model text
        E.append(np.exp(H(corpus))); TL.append(corpus[100:].sum())
    c=cmap(i/(len(alphas)-1)*0.9); lab=f"{int(al*100)}% synthetic"
    a.plot(E,color=c,lw=2,label=lab); b.plot(np.array(TL)*100,color=c,lw=2,label=lab)
    fin[al]=(E[-1],TL[-1],E[0],TL[0])
out["loop"]=fin
a.set_yscale("log"); a.set_xlabel("Generation"); a.set_ylabel("Effective number of ideas, exp(H)")
a.set_title("Fresh human writing sets the floor",loc="left",fontsize=11.5,color=INK); 
b.set_xlabel("Generation"); b.set_ylabel("% of corpus beyond the 100 most common ideas")
b.set_title("The tail survives only as long as people keep writing it",loc="left",fontsize=11.5,color=INK)
h,l=a.get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=6,frameon=False,fontsize=10); fig.tight_layout(rect=(0,0.08,1,1)); fig.savefig("oped-feedback.png"); plt.close(fig)
for k,v in out.items(): print(k,v)
