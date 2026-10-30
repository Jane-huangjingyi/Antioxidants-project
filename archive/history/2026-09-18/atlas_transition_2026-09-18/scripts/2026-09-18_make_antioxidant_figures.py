"""Generate all four active figures using only Python stdlib + Pillow."""
from pathlib import Path
import csv, math
from PIL import Image, ImageDraw, ImageFont

# ================================ CONFIG ====================================
CONFIG={
 "dpi":300,"font_size":24,"small_font_size":18,"title_size":32,
 "dimensions":{"bar":(2600,1500),"exposure":(3000,1800),"heatmap":(3200,2200),"map":(3200,2300)},
 "point_size":16,"line_width":3,"label_rotation":55,
 "ordering":["Polyphenol","Phenolic acid","Phenolic conjugate","Vitamin","Carotenoid","Organosulfur","Other food phenolic"],
 "legend_location":"right","axis_limits":{"exposure":(-1.2,3.7)},"exposure_threshold_fold":100,
 "class_colors":{"Polyphenol":"#4C78A8","Phenolic acid":"#72B7B2","Phenolic conjugate":"#54A24B","Vitamin":"#F58518","Carotenoid":"#ECA82C","Organosulfur":"#B279A2","Other food phenolic":"#FF9DA6","Mineral micronutrient":"#79706E"},
 "evidence_coding":{"Strong":3.0,"Moderate":2.0,"Limited":1.0,"Predictive":0.5,"None":0.0},
 "evidence_colors":{3.0:"#1B7837",2.0:"#70AD47",1.0:"#A5C8E1",0.5:"#D9D4E7",0.0:"#F2F2F2"},
 "mechanism_order":["direct radical scavenging","reducing power","metal chelation","lipid peroxidation","NRF2","GSH/GPX","SOD/CAT","NOX/mitochondrial ROS","ferroptosis/lipid","redox-inflammatory","mineral cofactor"]
}
# ============================================================================
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
def read(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
P=read(ROOT/'Antioxidant_Panel_Master.csv'); E=read(ROOT/'Antioxidant_Mechanism_Evidence_Master.csv')
ORG=[r for r in P if r['panel_status']!='micronutrient_context']
def font(size,bold=False):
 for p in [Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'),Path('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc')]:
  if p.exists(): return ImageFont.truetype(str(p),size)
 return ImageFont.load_default()
F=font(CONFIG['font_size']); FS=font(CONFIG['small_font_size']); FT=font(CONFIG['title_size'],True)
def base(kind,title):
 im=Image.new('RGB',CONFIG['dimensions'][kind],'white'); d=ImageDraw.Draw(im); d.text((90,45),title,font=FT,fill='#111111'); return im,d
def save(im,name): im.save(OUT/name,dpi=(CONFIG['dpi'],CONFIG['dpi']))

im,d=base('bar','Class-balanced dietary antioxidant functional-factor panel (v1.0)')
counts={c:sum(r['chemical_class']==c for r in ORG) for c in CONFIG['ordering']}; x0,y0,x1,y1=180,250,2450,1260; bw=(x1-x0)//len(counts)
for i,(c,v) in enumerate(counts.items()):
 x=x0+i*bw+25; h=v/6*(y1-y0); d.rectangle((x,y1-h,x+bw-50,y1),fill=CONFIG['class_colors'][c]); d.text((x+bw//2-10,y1-h-45),str(v),font=F,fill='#111'); d.text((x,y1+25),c,font=FS,fill='#111')
d.line((x0,y1,x1,y1),fill='#222',width=3); d.text((1700,150),'Minerals (n=5) are a separate context layer',font=FS,fill='#555'); save(im,'Class_Balanced_Antioxidant_Panel.png')

im,d=base('exposure','Dietary exposure range: intake estimates, not systemic exposure')
vals=sorted([(r['compound'],float(r['log10_exposure']),r['chemical_class'],r['panel_status']) for r in ORG if r['log10_exposure']],key=lambda x:x[1]); x0,y0,x1,y1=160,250,2840,1400; lo,hi=CONFIG['axis_limits']['exposure']; core=[v for _,v,_,s in vals if s=='core_panel']; wlo=min(core); whi=wlo+math.log10(CONFIG['exposure_threshold_fold']); Y=lambda v:y1-(v-lo)/(hi-lo)*(y1-y0)
d.rectangle((x0,Y(whi),x1,Y(wlo)),fill='#EBF2F8'); d.text((x0+10,Y(whi)+10),'100-fold core window',font=FS,fill='#355C7D')
for k in range(-1,4): d.line((x0,Y(k),x1,Y(k)),fill='#DDDDDD',width=2); d.text((80,Y(k)-10),str(k),font=FS,fill='#333')
dx=(x1-x0)/max(1,len(vals)-1)
for i,(name,v,cl,st) in enumerate(vals):
 x=x0+i*dx; col=CONFIG['class_colors'][cl]; d.ellipse((x-12,Y(v)-12,x+12,Y(v)+12),fill=col,outline='black',width=2); d.text((x-20,y1+35+(i%2)*45),name,font=FS,fill='#111')
d.text((50,180),'y = log10(µmol/day)',font=F,fill='#111'); save(im,'Dietary_Exposure_Range.png')

def domain(r):
 t=(r['mechanism_category']+' '+r['mechanism_subcategory']+' '+r['pathway']).lower()
 if 'orac' in t or 'radical chain' in t:return 'direct radical scavenging'
 if 'reducing' in t or 'electron' in t:return 'reducing power'
 if 'chelat' in t:return 'metal chelation'
 if 'nrf2' in t or 'keap1' in t:return 'NRF2'
 if 'gpx' in t or 'glutathione' in t or 'thioredoxin' in t:return 'GSH/GPX'
 if 'sod' in t or 'catalase' in t:return 'SOD/CAT'
 if 'nox' in t or 'mitochond' in t:return 'NOX/mitochondrial ROS'
 if 'ferro' in t:return 'ferroptosis/lipid'
 if 'inflamm' in t or 'nf-k' in t:return 'redox-inflammatory'
 if 'mineral' in t or 'cofactor' in t:return 'mineral cofactor'
 if 'lipid' in t:return 'lipid peroxidation'
 return 'direct radical scavenging'

im,d=base('heatmap','Compound–pathway evidence strength (design-based grading)')
names=[r['compound'] for r in P]; mechs=CONFIG['mechanism_order']; grid={}
for r in E: grid[(r['compound'],domain(r))]=max(grid.get((r['compound'],domain(r)),0),CONFIG['evidence_coding'].get(r['evidence_strength'],0))
x0,y0=660,300; cw,ch=220,66
for j,m in enumerate(mechs): d.text((x0+j*cw+5,190),m,font=FS,fill='#111')
for i,n in enumerate(names):
 d.text((80,y0+i*ch+18),n,font=FS,fill='#111')
 for j,m in enumerate(mechs):
  v=grid.get((n,m),0); d.rectangle((x0+j*cw,y0+i*ch,x0+(j+1)*cw-3,y0+(i+1)*ch-3),fill=CONFIG['evidence_colors'][v],outline='white')
for idx,(k,v) in enumerate(CONFIG['evidence_coding'].items()):
 yy=200+idx*45; d.rectangle((2840,yy,2875,yy+30),fill=CONFIG['evidence_colors'][v],outline='#555'); d.text((2890,yy),f'{k} = {v:g}',font=FS,fill='#111')
save(im,'Compound_Pathway_Evidence_Heatmap.png')

im,d=base('map','Antioxidant evidence map: compounds, mechanisms and mineral context')
leftx,rightx=390,2600; top,bottom=220,2160; posL={n:(leftx,top+i*(bottom-top)/max(1,len(names)-1)) for i,n in enumerate(names)}; posR={m:(rightx,top+i*(bottom-top)/max(1,len(mechs)-1)) for i,m in enumerate(mechs)}
for r in E:
 m=domain(r); n=r['compound']; v=CONFIG['evidence_coding'].get(r['evidence_strength'],0); d.line((posL[n][0],posL[n][1],posR[m][0],posR[m][1]),fill='#B0B0B0',width=max(1,int(v*2)))
for r in P:
 n=r['compound']; x,y=posL[n]; col=CONFIG['class_colors'].get(r['chemical_class'],'#888'); d.ellipse((x-14,y-14,x+14,y+14),fill=col,outline='white'); d.text((x+24,y-13),n,font=FS,fill='#111')
for m,(x,y) in posR.items(): d.rounded_rectangle((x-220,y-25,x+390,y+25),radius=8,fill='#333333'); d.text((x-205,y-16),m,font=FS,fill='white')
save(im,'Antioxidant_Evidence_Map.png')
print(f'Generated 4 figures in {OUT}')
