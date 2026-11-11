import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
INK="#191A1E"; MUTED="#6E6B62"; NAVY="#183A6B"; BG="#FBFAF6"; RED="#9B3B2E"; GOLD="#B27C2E"
plt.rcParams.update({"font.family":"DejaVu Sans","figure.facecolor":BG,"savefig.dpi":200})
fig,ax=plt.subplots(figsize=(11,5.4)); ax.set_xlim(0,22); ax.set_ylim(0,11); ax.axis("off"); ax.set_aspect("equal")
def person(x,y,c):
    ax.add_patch(Circle((x,y+0.32),0.17,color=c)); ax.add_patch(FancyBboxPatch((x-0.24,y-0.32),0.48,0.5,boxstyle="round,pad=0,rounding_size=0.2",color=c))
# 100 flagged: 16 true, 84 false; grid 10x10
for i in range(100):
    r,c_=divmod(i,10); x=0.8+c_*0.95; y=9.0-r*0.95
    person(x,y, NAVY if i<16 else RED)
ax.text(0.4,10.35,"100 students flagged as \"written by AI\"",fontsize=13,color=INK,weight="bold")
tx=11.0
ax.text(tx,8.6,"16",fontsize=40,color=NAVY,weight="bold",va="center"); ax.text(tx+2.1,8.6,"actually used AI",fontsize=14,color=INK,va="center")
ax.text(tx,6.3,"84",fontsize=40,color=RED,weight="bold",va="center"); ax.text(tx+2.1,6.3,"did nothing wrong",fontsize=14,color=INK,va="center")
ax.text(tx,3.9,"The detector is \"90% accurate\":\n90% sensitivity, 90% specificity.\nOnly 2 in 100 essays are AI-written.",fontsize=11.5,color=MUTED,va="center",linespacing=1.5)
ax.text(tx,1.9,"A good test on a rare problem\nmostly accuses the innocent.",fontsize=12.5,color=INK,va="center",style="italic",linespacing=1.4)
fig.savefig("latent-people.png",bbox_inches="tight",facecolor=BG)
