import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"
plt.rcParams.update({"font.family":"DejaVu Sans","figure.facecolor":BG,"savefig.dpi":200})
stats=[("Writing","10.7%","rise in story similarity with one\nAI idea (share of human spread)","Doshi & Hauser 2024, N = 293",NAVY),
       ("Code","2 vs 3","distinct algorithms per problem:\nmodels vs people","EMNLP Findings 2025",NAVY),
       ("Already everywhere","17.5%","of sentences in CS abstracts\nLLM-modified by early 2024","Liang et al. 2024",GOLD)]
fig=plt.figure(figsize=(10,2.7))
for i,(lab,num,desc,src,col) in enumerate(stats):
    x=i/3
    ax=fig.add_axes([x+0.015,0.04,1/3-0.03,0.92]); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.plot([0,1],[0.96,0.96],color=col,lw=3)
    ax.text(0,0.86,lab.upper(),fontsize=10,color=MUTED,va="top",fontweight="bold")
    ax.text(0,0.74,num,fontsize=34,color=col,va="top",fontweight="bold")
    ax.text(0,0.40,desc,fontsize=11.5,color=INK,va="top",linespacing=1.35)
    ax.text(0,0.0,src,fontsize=9,color=MUTED,va="bottom")
fig.savefig("assets/img/posts/oped/oped-evidence.png",bbox_inches="tight",pad_inches=0.25)
