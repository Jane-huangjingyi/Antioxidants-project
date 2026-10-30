"""Generate the four active class-balanced antioxidant figures from the two master CSVs."""
from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import networkx as nx

# ================================ CONFIG ====================================
CONFIG = {
    "dpi": 300,
    "font_family": "DejaVu Sans",
    "figure_width": 13,
    "bar_height": 7,
    "heatmap_width": 16,
    "heatmap_height": 11,
    "network_width": 16,
    "network_height": 12,
    "point_size": 70,
    "line_width": 1.5,
    "label_rotation": 55,
    "exposure_window_fold": 100,
    "panel_status_order": ["core_panel", "exceptional_representative", "extended_special_case"],
    "class_order": ["Polyphenol", "Phenolic acid", "Phenolic conjugate", "Vitamin", "Carotenoid", "Organosulfur", "Other food phenolic"],
    "class_colors": {
        "Polyphenol": "#4C78A8", "Phenolic acid": "#72B7B2", "Phenolic conjugate": "#54A24B",
        "Vitamin": "#F58518", "Carotenoid": "#ECA82C", "Organosulfur": "#B279A2",
        "Other food phenolic": "#FF9DA6", "Mineral micronutrient": "#79706E"
    },
    "evidence_code": {"Strong": 3.0, "Moderate": 2.0, "Limited": 1.0, "Predictive": 0.5},
    "mechanism_order": ["direct radical scavenging", "reducing power", "metal chelation", "lipid peroxidation", "NRF2", "GSH/GPX", "SOD/CAT", "NOX/mitochondrial ROS", "ferroptosis/lipid", "redox-inflammatory", "mineral cofactor"],
    "axis_limits": {"exposure": (-1.2, 3.7)},
    "legend_location": "best",
}
# ============================================================================

ROOT = Path(__file__).resolve().parents[1]
PANEL_CSV = ROOT / "Antioxidant_Panel_Master.csv"
EVID_CSV = ROOT / "Antioxidant_Mechanism_Evidence_Master.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": CONFIG["font_family"], "axes.spines.top": False, "axes.spines.right": False})

panel = pd.read_csv(PANEL_CSV)
ev = pd.read_csv(EVID_CSV)
organic = panel[panel.panel_status != "micronutrient_context"].copy()

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=CONFIG["dpi"], bbox_inches="tight", facecolor="white")
    plt.close(fig)

# Figure 1: class balance
counts = organic.groupby("chemical_class").size().reindex(CONFIG["class_order"]).dropna()
fig, ax = plt.subplots(figsize=(CONFIG["figure_width"], CONFIG["bar_height"]))
bars = ax.bar(counts.index, counts.values, color=[CONFIG["class_colors"].get(x, "#888888") for x in counts.index])
ax.bar_label(bars, padding=3, fontsize=10)
ax.set_ylabel("Number of organic panel candidates")
ax.set_title("Class-balanced dietary antioxidant functional-factor panel (v1.0)", weight="bold")
ax.tick_params(axis="x", rotation=CONFIG["label_rotation"])
ax.text(0.99, 0.97, "Minerals (n=5) are a separate micronutrient context layer", transform=ax.transAxes, ha="right", va="top", fontsize=9)
save(fig, "Class_Balanced_Antioxidant_Panel.png")

# Figure 2: exposure, with core 100-fold window
e = organic.dropna(subset=["log10_exposure"]).sort_values("log10_exposure")
fig, ax = plt.subplots(figsize=(CONFIG["figure_width"], 8))
colors=[CONFIG["class_colors"].get(x,"#888") for x in e.chemical_class]
markers=["o" if s=="core_panel" else ("D" if s=="exceptional_representative" else "s") for s in e.panel_status]
for i,(_,r) in enumerate(e.iterrows()):
    ax.scatter(i,r.log10_exposure,s=CONFIG["point_size"],c=CONFIG["class_colors"].get(r.chemical_class,"#888"),marker=markers[i],edgecolor="black",linewidth=.5,zorder=3)
core=e[e.panel_status=="core_panel"]
if len(core):
    lo=core.log10_exposure.min(); hi=lo+math.log10(CONFIG["exposure_window_fold"])
    ax.axhspan(lo,hi,color="#4C78A8",alpha=.09,label="100-fold window anchored to lowest core exposure")
ax.set_xticks(range(len(e))); ax.set_xticklabels(e.compound,rotation=CONFIG["label_rotation"],ha="right")
ax.set_ylabel("log10 habitual intake (µmol/day)")
ax.set_ylim(*CONFIG["axis_limits"]["exposure"])
ax.set_title("Dietary exposure range: intake estimates, not systemic exposure",weight="bold")
legend=[Patch(facecolor=CONFIG["class_colors"][c],label=c) for c in CONFIG["class_order"] if c in set(e.chemical_class)]
ax.legend(handles=legend,loc="upper left",ncol=2,fontsize=8)
save(fig,"Dietary_Exposure_Range.png")

# Evidence-domain mapping function
def domain(row):
    text=(str(row.mechanism_category)+" "+str(row.mechanism_subcategory)+" "+str(row.pathway)).lower()
    if "orac" in text or "radical chain" in text: return "direct radical scavenging"
    if "reducing" in text or "electron" in text: return "reducing power"
    if "chelat" in text: return "metal chelation"
    if "lipid" in text and "ferro" not in text: return "lipid peroxidation"
    if "nrf2" in text or "keap1" in text: return "NRF2"
    if "gpx" in text or "glutathione" in text or "thioredoxin" in text: return "GSH/GPX"
    if "sod" in text or "catalase" in text: return "SOD/CAT"
    if "nox" in text or "mitochond" in text: return "NOX/mitochondrial ROS"
    if "ferro" in text: return "ferroptosis/lipid"
    if "inflamm" in text or "nf-k" in text: return "redox-inflammatory"
    if "mineral" in text or "cofactor" in text: return "mineral cofactor"
    return "lipid peroxidation" if "tocopherol" in str(row.compound).lower() else "direct radical scavenging"
ev["domain"]=ev.apply(domain,axis=1)
ev["score"]=ev.evidence_strength.map(CONFIG["evidence_code"]).fillna(0)
order=list(organic.compound)+list(panel[panel.panel_status=="micronutrient_context"].compound)
heat=ev.pivot_table(index="compound",columns="domain",values="score",aggfunc="max").reindex(index=order,columns=CONFIG["mechanism_order"]).fillna(0)
cmap=ListedColormap(["#F2F2F2","#D9D4E7","#A5C8E1","#70AD47","#1B7837"])
norm=BoundaryNorm([-0.01,.25,.75,1.5,2.5,3.1],cmap.N)
fig,ax=plt.subplots(figsize=(CONFIG["heatmap_width"],CONFIG["heatmap_height"]))
im=ax.imshow(heat.values,aspect="auto",cmap=cmap,norm=norm)
ax.set_yticks(range(len(heat))); ax.set_yticklabels(heat.index,fontsize=8)
ax.set_xticks(range(len(heat.columns))); ax.set_xticklabels(heat.columns,rotation=45,ha="right",fontsize=8)
ax.set_title("Compound–pathway evidence strength (design-based grading)",weight="bold")
legend=[Patch(facecolor=cmap(norm(v)),label=f"{k} = {v:g}") for k,v in [("Strong",3),("Moderate",2),("Limited",1),("Predictive",.5),("None",0)]]
ax.legend(handles=legend,bbox_to_anchor=(1.01,1),loc="upper left",fontsize=8)
save(fig,"Compound_Pathway_Evidence_Heatmap.png")

# Figure 4: evidence map
G=nx.Graph()
for _,r in panel.iterrows(): G.add_node(r.compound,kind="mineral" if r.panel_status=="micronutrient_context" else "compound",cl=r.chemical_class)
for d in CONFIG["mechanism_order"]: G.add_node(d,kind="mechanism",cl="mechanism")
for _,r in ev.iterrows():
    if r.compound in G and r.domain in G: G.add_edge(r.compound,r.domain,weight=r.score)
pos={}
comps=[n for n,d in G.nodes(data=True) if d['kind']!='mechanism']; mechs=CONFIG["mechanism_order"]
for i,n in enumerate(comps): pos[n]=(0,-i)
for i,n in enumerate(mechs): pos[n]=(2,-i*(max(1,len(comps)-1)/max(1,len(mechs)-1)))
fig,ax=plt.subplots(figsize=(CONFIG["network_width"],CONFIG["network_height"]))
for u,v,d in G.edges(data=True): nx.draw_networkx_edges(G,pos,edgelist=[(u,v)],width=.4+d['weight']*.45,alpha=.35,edge_color="#666",ax=ax)
nx.draw_networkx_nodes(G,pos,nodelist=comps,node_size=340,node_color=[CONFIG["class_colors"].get(G.nodes[n]['cl'],"#888") for n in comps],edgecolors="white",ax=ax)
nx.draw_networkx_nodes(G,pos,nodelist=mechs,node_size=650,node_shape="s",node_color="#333333",ax=ax)
nx.draw_networkx_labels(G,pos,font_size=7,font_color="black",labels={n:n for n in comps},ax=ax)
nx.draw_networkx_labels(G,pos,font_size=7,font_color="white",labels={n:n for n in mechs},ax=ax)
ax.set_title("Antioxidant evidence map: compounds, mechanisms and mineral context",weight="bold")
ax.axis("off")
save(fig,"Antioxidant_Evidence_Map.png")

print(f"Generated 4 figures in {OUT}")
