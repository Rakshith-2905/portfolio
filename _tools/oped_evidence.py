import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":LINE,"grid.linewidth":0.8,"savefig.dpi":200})
fig,(a,b)=plt.subplots(2,1,figsize=(9,8.2))
rows=[("Story similarity gain, one AI idea (% of human spread)\nDoshi & Hauser 2024, N = 293",10.7),("India–US essay similarity, 0.48 → 0.54\nAgarwal et al. 2025, N = 118",(0.54/0.48-1)*100),("Unique key points lost, InstructGPT vs. alone\nPadmakumar & He 2024",(1-0.877/0.941)*100),("Unique 4-word phrases lost, InstructGPT vs. alone\nPadmakumar & He 2024",(1-0.953/0.973)*100)]
y=np.arange(len(rows))[::-1]
a.barh(y,[r[1] for r in rows],color=NAVY,height=0.55)
for yi,r in zip(y,rows): a.text(r[1]+0.25,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
a.set_yticks(y); a.set_yticklabels([r[0] for r in rows],fontsize=9.5)
a.set_xlabel("Convergence vs. writing alone, % (each study's own measure)"); a.set_xlim(0,15); a.grid(axis="y",visible=False)
a.set_title("Writing with an LLM makes people's work more alike",loc="left",fontsize=12,color=INK,pad=10)
rows2=[("Computer science arXiv abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",17.5),("PubMed abstracts, 2024 (lower bound)\nKobak et al. 2024 (% of abstracts)",13.5),("Nature-portfolio abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",6.3),("Mathematics arXiv abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",4.9)]
y2=np.arange(len(rows2))[::-1]
b.barh(y2,[r[1] for r in rows2],color=GOLD,height=0.55)
for yi,r in zip(y2,rows2): b.text(r[1]+0.3,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
b.set_yticks(y2); b.set_yticklabels([r[0] for r in rows2],fontsize=9.5); b.set_xlim(0,22); b.grid(axis="y",visible=False)
b.set_xlabel("Estimated share that is substantially LLM-modified (%)")
b.set_title("A growing share of published writing is already LLM-modified",loc="left",fontsize=12,color=INK,pad=10)
fig.tight_layout(h_pad=2.5); fig.savefig("assets/img/posts/oped/oped-evidence.png"); plt.close(fig)
