import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"; RED="#9B3B2E"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10.5,"figure.facecolor":BG,"savefig.dpi":200})
fig,ax=plt.subplots(figsize=(13,4.6)); ax.set_xlim(0,13); ax.set_ylim(0.4,4.9); ax.axis("off")
def box(x,y,w,h,t,c,fc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.04,rounding_size=0.12",ec=c,fc=fc or BG,lw=1.6))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=9.6,color=INK,linespacing=1.35)
def arr(x1,x2,y,c=MUTED): ax.annotate("",(x2,y),(x1,y),arrowprops=dict(arrowstyle="-|>",color=c,lw=1.4))
# Row A
yA=3.2; h=1.25
ax.text(0.05,4.62,"A.  \"Just ask the model\": LLM + structured output",fontsize=12,color=RED,weight="bold")
xs=[(0.05,1.45,"ticket text\n+ prompt\n+ schema"),(1.85,1.75,"decoder-only\ntransformer\n(MoE blocks,\nlong context)"),
    (3.95,1.75,"softmax over\n~200k tokens\n(web text, then\nrater preferences)"),
    (6.05,1.75,"grammar mask:\nzero all but allowed\ntokens, renormalize"),
    (8.15,1.55,"sample one\npath, maybe\nafter hidden\nreasoning"),
    (10.05,2.9,'{"label": "billing",\n "confidence": 0.95}\n\nlabel = one draw\nconfidence = generated text')]
for i,(x,w,t) in enumerate(xs):
    box(x,yA,w,h,t,RED,"#F6ECE8" if i==5 else None)
    if i: arr(xs[i-1][0]+xs[i-1][1]+0.04,x-0.04,yA+h/2,RED)
# Row B
yB=0.55
ax.text(0.05,1.97,"B.  A classifier for this task: same model as a feature extractor, plus a trained head",fontsize=12,color=NAVY,weight="bold")
xs=[(0.05,1.45,"ticket text"),(1.85,1.75,"encoder or frozen\nLLM\n(embeddings)"),
    (3.95,1.75,"linear head\nK × d, softmax\nover K classes"),
    (6.05,1.75,"trained with\ncross-entropy on\nyour labels\n(a proper score)"),
    (8.15,1.55,"temperature /\nPlatt fit on\nheld-out labels,\nprior adjusted"),
    (10.05,2.9,"p(billing) = 0.71\np(technical) = 0.22\np(other) = 0.07\n\nthreshold for a target precision")]
for i,(x,w,t) in enumerate(xs):
    box(x,yB,w,h,t,NAVY,"#E8EDF4" if i==5 else None)
    if i: arr(xs[i-1][0]+xs[i-1][1]+0.04,x-0.04,yB+h/2,NAVY)
fig.savefig("latent-schematic.png",bbox_inches="tight",facecolor=BG)
