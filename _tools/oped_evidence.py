import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; BG="#FBFAF6"; GREY="#A9A397"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False,"axes.spines.left":False,"axes.grid":False,"savefig.dpi":200})
fig,(a,b)=plt.subplots(1,2,figsize=(9,3.6))
def pair(ax,vals,labels,title,fmt,ymax,note):
    bars=ax.bar(labels,vals,color=[GREY,NAVY],width=0.55)
    for bb,v in zip(bars,vals): ax.text(bb.get_x()+bb.get_width()/2,v+ymax*0.03,fmt(v),ha="center",color=INK,fontsize=13,fontweight="bold")
    ax.set_ylim(0,ymax); ax.set_yticks([]); ax.set_title(title,loc="left",fontsize=11.5,color=INK,pad=10)
    ax.set_xlabel(note,fontsize=8.5,color=MUTED,labelpad=8)
pair(a,[3,2],["People","LLMs"],"Distinct ways to solve a coding problem",lambda v:f"~{v:.0f}",3.7,"Introductory problems, EMNLP Findings 2025")
pair(b,[0.48,0.54],["Writing alone","With GPT-4o\nautocomplete"],"How alike Indian and US essays are",lambda v:f"{v:.2f}",0.68,"Cosine similarity, Agarwal et al. 2025 (N = 118)")
fig.tight_layout(w_pad=3); fig.savefig("assets/img/posts/oped/oped-evidence.png",bbox_inches="tight",pad_inches=0.2); plt.close(fig)
