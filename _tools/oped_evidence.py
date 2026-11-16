import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"; GREY="#A9A397"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":LINE,"grid.linewidth":0.8,"savefig.dpi":200})
fig=plt.figure(figsize=(9,11.2))
gs=fig.add_gridspec(3,2,height_ratios=[1.05,0.8,1.05],hspace=0.62,wspace=0.35)
a=fig.add_subplot(gs[0,:]); c1=fig.add_subplot(gs[1,0]); c2=fig.add_subplot(gs[1,1]); b=fig.add_subplot(gs[2,:])
rows=[("Story similarity with one AI idea\n(vs. spread of human-only stories)\nDoshi & Hauser 2024, N = 293",10.7),("India–US essay similarity, 0.48 → 0.54\nAgarwal et al. 2025, N = 118",(0.54/0.48-1)*100),("Unique key points lost, InstructGPT vs. alone\nPadmakumar & He 2024",(1-0.877/0.941)*100)]
y=np.arange(len(rows))[::-1]
a.barh(y,[r[1] for r in rows],color=NAVY,height=0.55)
for yi,r in zip(y,rows): a.text(r[1]+0.25,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
a.set_yticks(y); a.set_yticklabels([r[0] for r in rows],fontsize=9.5); a.set_xlim(0,15); a.grid(axis="y",visible=False)
a.set_xlabel("% more similar, or % less diverse, than writing alone")
a.set_title("Writing: people's work becomes more alike",loc="left",fontsize=12,color=INK,pad=10)
def pair(ax,vals,labels,title,fmt,ymax,note):
    bars=ax.bar(labels,vals,color=[GREY,NAVY],width=0.55)
    for bb,v in zip(bars,vals): ax.text(bb.get_x()+bb.get_width()/2,v+ymax*0.03,fmt(v),ha="center",color=INK,fontsize=11)
    ax.set_ylim(0,ymax); ax.grid(axis="x",visible=False); ax.set_title(title,loc="left",fontsize=10.5,color=INK,pad=8)
    ax.set_xlabel(note,fontsize=8.5,color=MUTED)
pair(c1,[3,2],["Human\nprogrammers","LLM"],"Code: distinct algorithms per problem",lambda v:f"~{v:.0f}",3.8,"Introductory problems, EMNLP Findings 2025")
pair(c2,[1.0,2.3],["Human\nprojects","AI agents"],"Code: verbosity",lambda v:f"{v:.1f}×",2.9,"473 open-source Python repos, SlopCodeBench 2026")
rows2=[("Computer science arXiv abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",17.5),("PubMed abstracts, 2024 (lower bound)\nKobak et al. 2024 (% of abstracts)",13.5),("Nature-portfolio abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",6.3),("Mathematics arXiv abstracts, Feb 2024\nLiang et al. 2024 (% of sentences)",4.9)]
y2=np.arange(len(rows2))[::-1]
b.barh(y2,[r[1] for r in rows2],color=GOLD,height=0.55)
for yi,r in zip(y2,rows2): b.text(r[1]+0.3,yi,f"{r[1]:.1f}%",va="center",color=INK,fontsize=10.5)
b.set_yticks(y2); b.set_yticklabels([r[0] for r in rows2],fontsize=9.5); b.set_xlim(0,22); b.grid(axis="y",visible=False)
b.set_xlabel("Estimated share that is substantially LLM-modified (%)")
b.set_title("Already everywhere: published writing that is LLM-modified",loc="left",fontsize=12,color=INK,pad=10)
fig.savefig("assets/img/posts/oped/oped-evidence.png",bbox_inches="tight",pad_inches=0.25); plt.close(fig)
