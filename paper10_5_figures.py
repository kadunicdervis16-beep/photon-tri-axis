from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(exist_ok=True)

BLUE = '#2B507A'
GOLD = '#D99000'
GREEN = '#55A06A'
LIGHT_BLUE = '#EAF0F6'
LIGHT_GOLD = '#F8F0DF'
LIGHT_GREEN = '#E8F3EA'
GRAY = '#444444'
GRID = '#D9DDE3'
RED = '#C84B4B'

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10})


def frame(ax, title, subtitle=None):
    ax.set_facecolor('white')
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.965, title, ha='center', va='top', fontsize=18, fontweight='bold', color=BLUE, transform=ax.transAxes)
    if subtitle:
        ax.text(0.5, 0.905, subtitle, ha='center', va='top', fontsize=11.5, color=GOLD, transform=ax.transAxes)
    ax.add_patch(Rectangle((0.025,0.025),0.95,0.95, fill=False, lw=1.0, ec=GOLD, transform=ax.transAxes))


def save(fig, name):
    fig.savefig(OUT/name, dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig1():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 1 — THE COMPANION PAPER AS A CLAIM CHAIN','From exact enumeration to an empirical statement')
    xs=[0.11,0.30,0.49,0.68,0.87]; labels=['COUNT','ALLOCATE','BLOCK','TRANSITION','OBSERVE']; fills=[LIGHT_BLUE,LIGHT_GOLD,LIGHT_BLUE,LIGHT_GREEN,'#F4EAF5']; colors=[BLUE,GOLD,BLUE,GREEN,'#7A4A85']
    for x,l,fc,ec in zip(xs,labels,fills,colors):
        ax.add_patch(FancyBboxPatch((x-0.075,0.42),0.15,0.16,boxstyle='round,pad=0.012',fc=fc,ec=ec,lw=2,transform=ax.transAxes))
        ax.text(x,0.50,l,ha='center',va='center',fontweight='bold',color=ec,transform=ax.transAxes)
    for a,b in zip(xs[:-1],xs[1:]):
        ax.add_patch(FancyArrowPatch((a+0.075,0.50),(b-0.075,0.50),arrowstyle='-|>',mutation_scale=15,lw=1.8,color=GOLD,transform=ax.transAxes))
    ax.text(0.205,0.33,'shell-count theorem',ha='center',color=GRAY,fontsize=9,transform=ax.transAxes)
    ax.text(0.395,0.33,'workload rule',ha='center',color=GRAY,fontsize=9,transform=ax.transAxes)
    ax.text(0.585,0.33,'capacity threshold',ha='center',color=GRAY,fontsize=9,transform=ax.transAxes)
    ax.text(0.775,0.33,'reconstruction bridge',ha='center',color=GRAY,fontsize=9,transform=ax.transAxes)
    ax.text(0.5,0.15,'The bridge ledger audits the arrows, not only the boxes.',ha='center',fontsize=12,color=BLUE,transform=ax.transAxes)
    save(fig,'figure_1_claim_chain.png')


def fig2():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 2 — EXACT SHELL COUNT AND INVERSE-SQUARE SHADOW','The finite +2 is part of the exact native object')
    d=np.arange(1,13); exact=1/(4*d*d+2); shadow=1/(4*d*d)
    ax.set_position([0.10,0.20,0.84,0.62]);
    ax.plot(d,exact,'o-',lw=2,ms=5,color=BLUE,label=r'Exact $1/(4d^2+2)$')
    ax.plot(d,shadow,'--',lw=2,color=GOLD,label=r'Shadow $1/(4d^2)$')
    ax.set_xlabel('taxicab relay distance d',color=GRAY); ax.set_ylabel('per-site allocation (normalized)',color=GRAY)
    ax.grid(True,alpha=.3,color=GRID); ax.legend(frameon=False,loc='upper right')
    ax.text(0.5,0.10,r'$N(d)=4d^2+2$',ha='center',fontsize=14,color=BLUE,transform=fig.transFigure)
    save(fig,'figure_2_shell_count.png')


def fig3():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 3 — SIX-PORT CAPACITY EXHAUSTION','Blocking creates a finite directional response set')
    ax.set_position([0.09,0.22,0.85,0.60]); b=np.arange(7); o=6-b; factors=[1,6/5,3/2,2,3,6,np.nan]
    ax.bar(b[:6],factors[:6],width=.62,color=BLUE,alpha=.92)
    for x,y in zip(b[:6],factors[:6]): ax.text(x,y+0.12,f'{y:g}',ha='center',color=BLUE,fontweight='bold')
    ax.scatter([6],[0.18],s=100,color=RED,zorder=5); ax.text(6,0.48,'isolated',ha='center',color=RED,fontweight='bold')
    ax.set_xticks(b); ax.set_xticklabels([f'{i}\nblocked' for i in b]); ax.set_ylabel('factor on open ports'); ax.grid(axis='y',alpha=.25,color=GRID)
    ax.text(0.5,0.11,'factor = 6/(6−b) for b < 6; b = 6 requires a separate transition rule',ha='center',fontsize=11,color=GRAY,transform=fig.transFigure)
    save(fig,'figure_3_port_exhaustion.png')


def fig4():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 4 — WHY β = 1/3 IS NOT A FREE COEFFICIENT','Three axes + conservation + equivalent treatment')
    centers=[(0.25,0.50),(0.50,0.50),(0.75,0.50)]; labs=['X-axis','Y-axis','Z-axis']
    for (x,y),lab in zip(centers,labs):
        ax.add_patch(Circle((x,y),0.09,fc=LIGHT_BLUE,ec=BLUE,lw=2,transform=ax.transAxes)); ax.text(x,y,lab,ha='center',va='center',fontweight='bold',color=BLUE,transform=ax.transAxes)
        ax.text(x,0.32,r'$\beta$',ha='center',fontsize=14,color=GOLD,transform=ax.transAxes)
    ax.add_patch(FancyArrowPatch((0.28,0.62),(0.46,0.62),arrowstyle='-|>',mutation_scale=13,color=GOLD,transform=ax.transAxes))
    ax.add_patch(FancyArrowPatch((0.53,0.62),(0.71,0.62),arrowstyle='-|>',mutation_scale=13,color=GOLD,transform=ax.transAxes))
    ax.text(0.5,0.16,r'$\beta+\beta+\beta=1\quad\Rightarrow\quad\beta=1/3$',ha='center',fontsize=17,color=BLUE,transform=ax.transAxes)
    ax.text(0.5,0.78,'S₃ treats the axes equivalently; the Circa partition supplies normalization.',ha='center',fontsize=11.5,color=GRAY,transform=ax.transAxes)
    save(fig,'figure_4_beta.png')


def fig5():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 5 — TWO MANDATORY OPERATIONS','The factor of two belongs to the execution sequence before physical reconstruction')
    boxes=[(0.17,'IDENTITY\nVERIFICATION',LIGHT_GOLD,GOLD),(0.50,'TEMPORAL\nPROPAGATION',LIGHT_BLUE,BLUE),(0.83,'PHYSICAL\nRECONSTRUCTION',LIGHT_GREEN,GREEN)]
    for x,t,fc,ec in boxes:
        ax.add_patch(FancyBboxPatch((x-.115,.40),.23,.20,boxstyle='round,pad=.015',fc=fc,ec=ec,lw=2,transform=ax.transAxes)); ax.text(x,.50,t,ha='center',va='center',fontweight='bold',color=ec,transform=ax.transAxes)
    ax.add_patch(FancyArrowPatch((.285,.50),(.385,.50),arrowstyle='-|>',mutation_scale=15,color=GOLD,lw=2,transform=ax.transAxes))
    ax.add_patch(FancyArrowPatch((.615,.50),(.715,.50),arrowstyle='-|>',mutation_scale=15,color=GOLD,lw=2,transform=ax.transAxes))
    ax.text(.335,.64,'operation 1',ha='center',color=GOLD,fontsize=9,transform=ax.transAxes); ax.text(.665,.64,'operation 2',ha='center',color=GOLD,fontsize=9,transform=ax.transAxes)
    ax.text(.50,.20,r'$N_{transitions}=2$',ha='center',fontsize=19,color=BLUE,transform=ax.transAxes)
    save(fig,'figure_5_two_transitions.png')


def fig6():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 6 — THE SINGLE-REGIME TEST','Separate local-rule change from finite-boundary effects')
    ax.set_position([0.10,0.21,0.84,0.60]); N=np.array([1e3,1e4,1e5,1e6,1e9]); ideal=np.zeros_like(N); planted=0.15*np.log10(N)
    ax.plot(N,ideal,'o-',color=GREEN,lw=2,label='declared single-regime: Δ=0')
    ax.plot(N,planted,'o--',color=RED,lw=2,label='planted scale-dependent failure')
    ax.set_xscale('log'); ax.set_xlabel('aggregate inventory size $N_{agg}$'); ax.set_ylabel(r'$\Delta(\rho,N_{agg})$ at fixed $\rho$')
    ax.grid(True,alpha=.3,color=GRID); ax.legend(frameon=False,loc='upper left')
    ax.text(.5,.10,'A clean harness must be able to reject the planted failure.',ha='center',fontsize=11,color=GRAY,transform=fig.transFigure)
    save(fig,'figure_6_single_regime.png')


def fig7():
    fig, ax = plt.subplots(figsize=(10,5.8)); frame(ax,'FIGURE 7 — THE BRIDGE LEDGER','Claim strength cannot increase across a weaker necessary bridge')
    levels=[('LEVEL A','native exact',BLUE,LIGHT_BLUE),('LEVEL B','reconstruction',GOLD,LIGHT_GOLD),('LEVEL C','observation / calibration','#7A4A85','#F1EAF5')]
    y=.63
    for i,(lab,desc,ec,fc) in enumerate(levels):
        x=.18+i*.32
        ax.add_patch(FancyBboxPatch((x-.12,y-.07),.24,.14,boxstyle='round,pad=.012',fc=fc,ec=ec,lw=2,transform=ax.transAxes)); ax.text(x,y+.015,lab,ha='center',fontweight='bold',color=ec,transform=ax.transAxes); ax.text(x,y-.045,desc,ha='center',fontsize=8.5,color=GRAY,transform=ax.transAxes)
        if i<2: ax.add_patch(FancyArrowPatch((x+.12,y),(x+.20,y),arrowstyle='-|>',mutation_scale=14,color=GOLD,lw=1.8,transform=ax.transAxes))
    ax.text(.5,.34,r'$L_{claim}\leq\min(L_1,L_2,\ldots,L_n)$',ha='center',fontsize=20,color=BLUE,transform=ax.transAxes)
    ax.text(.5,.20,'Exact upstream arithmetic does not upgrade a downstream reconstruction or observation.',ha='center',fontsize=11,color=GRAY,transform=ax.transAxes)
    save(fig,'figure_7_bridge_ledger.png')


if __name__ == '__main__':
    for f in (fig1,fig2,fig3,fig4,fig5,fig6,fig7): f()
    print(f'Generated {len(list(OUT.glob("figure_*.png")))} figures in {OUT}')
