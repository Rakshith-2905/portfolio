import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
INK="#191A1E"; MUTED="#6E6B62"; LINE="#E1DDD2"; NAVY="#183A6B"; GOLD="#B27C2E"; BG="#FBFAF6"; RED="#9B3B2E"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,
 "figure.facecolor":BG,"axes.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":LINE,"savefig.dpi":200})
h7=0.28; ho=(1-h7)/9
def p7(k): a=h7**k; b=9*ho**k; return a/(a+b)
def kfor(p): return np.log(p/(1-p)*9)/np.log(h7/ho)
def eff(p): o=(1-p)/9; return np.exp(-(p*np.log(p)+9*o*np.log(o)))
fig,(a,b)=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={"width_ratios":[1.15,1]})
ks=np.linspace(1,5,200); a.plot(ks,[p7(k)*100 for k in ks],color=NAVY,lw=2.4)
pts=[("People (Kubovy & Psotka 1976)",0.28,NAVY),("GPT-4o-mini, Gemini 2.0, Phi-4\n(Coronado-Blázquez 2025)",0.80,GOLD),("Claude: 90 of 100 asks",0.90,RED),("GPT: 92 of 100 asks",0.92,RED)]
off={0:(10,-4),1:(12,-30),2:(10,-14),3:(-150,4),4:(-125,-14)}
for i,(lab,p,c) in enumerate(pts):
    k=kfor(min(p,0.999)); a.scatter([k],[p*100],color=c,s=55,zorder=5)
    a.annotate(lab+(f"  (k ≈ {k:.1f})" if i else ""),(k,p*100),textcoords="offset points",xytext=off[i],fontsize=9,color=INK)
a.set_xlabel("Sharpening exponent k  (people's preferences raised to the power k)"); a.set_ylabel("% of answers that are 7")
a.set_ylim(0,105); a.set_title("Chatbots pick 7 the way people do, cubed",loc="left",fontsize=11.5,color=INK)
jokes=[("Why did the scarecrow win an award?",140),("Why did the tomato turn red?",122),("Why was the math book sad?",121),("Why don't scientists trust atoms?",119),("Why did the cookie go to the doctor?",79)]
y=np.arange(5)[::-1]; b.barh(y,[j[1] for j in jokes],color=NAVY,height=0.6)
for yi,j in zip(y,jokes): b.text(j[1]+3,yi,f"{j[1]}",va="center",fontsize=10,color=INK)
b.set_yticks(y); b.set_yticklabels([j[0] for j in jokes],fontsize=9.5); b.grid(axis="y",visible=False); b.set_xlim(0,165)
b.set_xlabel("Times told, out of 1,008 requests for a joke")
b.set_title("Jokes: 25 of them are 90% of all 1,008",loc="left",fontsize=11.5,color=INK)
fig.tight_layout(); fig.savefig("oped-seven.png")
for lab,p,c in pts: print(lab.replace("\n"," "),p,round(kfor(min(p,.999)),2),round(1/kfor(min(p,.999)),2),round(eff(min(p,.999)),2))
print("human eff",eff(0.28))
