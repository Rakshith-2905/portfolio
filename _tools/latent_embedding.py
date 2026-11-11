import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
INK="#191A1E"; MUTED="#6E6B62"; NAVY="#183A6B"; BG="#FBFAF6"; RED="#9B3B2E"; GOLD="#B27C2E"; GRN="#3F6B4E"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"figure.facecolor":BG,"axes.facecolor":BG,"savefig.dpi":200})
rng=np.random.default_rng(3)
C=np.array([[-2.0,1.2],[2.0,1.4],[0.0,-1.8]]); names=["billing","technical","other"]; cols=[NAVY,GOLD,GRN]
X=np.vstack([rng.normal(c,1.0,(60,2)) for c in C]); y=np.repeat([0,1,2],60)
# multinomial logistic regression by gradient descent
W=np.zeros((3,2)); b=np.zeros(3)
for _ in range(4000):
    z=X@W.T+b; z-=z.max(1,keepdims=True); P=np.exp(z); P/=P.sum(1,keepdims=True)
    G=P.copy(); G[np.arange(len(y)),y]-=1; W-=0.1*((G.T@X)/len(y)+0.05*W); b-=0.1*G.mean(0)
def prob(pts):
    z=pts@W.T+b; z-=z.max(1,keepdims=True); P=np.exp(z); return P/P.sum(1,keepdims=True)
xx,yy=np.meshgrid(np.linspace(-6,10,400),np.linspace(-5,7,300)); G=np.c_[xx.ravel(),yy.ravel()]
P=prob(G); lab=P.argmax(1).reshape(xx.shape); conf=P.max(1).reshape(xx.shape)
fig,ax=plt.subplots(figsize=(11,6.2))
ax.contourf(xx,yy,lab,levels=[-.5,.5,1.5,2.5],colors=["#E3E8F0","#F3E9D8","#E2ECE4"])
cs=ax.contour(xx,yy,conf,levels=[0.9,0.99],colors=[MUTED],linewidths=0.8,linestyles=[":","--"])
ax.clabel(cs,fmt={0.9:"90% sure",0.99:"99% sure"},fontsize=9)
for k in range(3):
    ax.scatter(*X[y==k].T,s=14,color=cols[k],alpha=0.8,label=f"training examples: {names[k]}")
qa=np.array([[-1.6,1.0]]); qb=np.array([[9.0,3.6]])
pa=prob(qa)[0]; pb=prob(qb)[0]
ax.scatter(*qa.T,s=160,marker="*",color=INK,zorder=5); ax.scatter(*qb.T,s=160,marker="*",color=RED,zorder=5)
ax.annotate(f"A ticket like the training data:\n\"{names[pa.argmax()]}\", {pa.max():.1%}\n(interpolation)",qa[0],(-5.7,5.4),fontsize=10,color=INK,arrowprops=dict(arrowstyle="->",color=INK))
ax.annotate(f"A ticket unlike anything seen:\nstill \"{names[pb.argmax()]}\", over 99.99%\n(extrapolation)",qb[0],(4.6,5.6),fontsize=10,color=RED,arrowprops=dict(arrowstyle="->",color=RED))
ax.set_xlim(-6,10); ax.set_ylim(-5,7); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("embedding dimension 1 (of thousands)",color=MUTED); ax.set_ylabel("embedding dimension 2",color=MUTED)
for s_ in ax.spines.values(): s_.set_color("#E1DDD2")
ax.legend(frameon=True,facecolor=BG,edgecolor=BG,framealpha=1,fontsize=9,loc="lower left")
fig.savefig("latent-embedding.png",bbox_inches="tight",facecolor=BG)
print(pa.round(3),pb.round(4))
