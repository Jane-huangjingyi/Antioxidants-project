"""Conservative trapezoidal-AUC preparation for actual, independently QC-cleared absorbance data."""
from pathlib import Path
import argparse,csv,collections,math
def integrate(times,values):
 if len(times)<2 or len(times)!=len(values) or any(b<=a for a,b in zip(times,times[1:])):raise ValueError('Strictly increasing common time grid required')
 if not all(math.isfinite(v) for v in times+values):raise ValueError('Non-finite data cannot be imputed')
 return sum((b-a)*(x+y)/2 for a,b,x,y in zip(times,times[1:],values,values[1:]))
def analyze(rows):
 groups=collections.defaultdict(list)
 for r in rows:groups[(r['batch_id'],r['plate_id'],r['well'])].append(r)
 traces={}
 for key,items in groups.items():
  items.sort(key=lambda r:float(r['time_min']));meta=items[0]
  for r in items:
   for f in ['candidate_id','concentration_uM','role','pair_id','counter_screen_pass']:
    if r[f]!=meta[f]:raise ValueError('Changing trace metadata: '+str(key))
  traces[key]=(meta,[float(r['time_min']) for r in items],[float(r['absorbance']) for r in items])
 out=[]
 for key,(meta,times,values) in traces.items():
  if meta['role'] not in {'SAMPLE','TROLOX','VEHICLE'}:continue
  if meta['counter_screen_pass']!='YES':raise ValueError('No approved interference clearance for '+str(key))
  pairs=[(m,t,v) for (batch,plate,_),(m,t,v) in traces.items() if (batch,plate)==key[:2] and m['pair_id']==meta['pair_id'] and m['role']=='MATCHED_NO_PROBE']
  if len(pairs)!=1:raise ValueError('One matched no-probe trace is required: '+str(key))
  background,bt,bv=pairs[0]
  if background['candidate_id']!=meta['candidate_id'] or background['concentration_uM']!=meta['concentration_uM']:raise ValueError('Background dose or identity mismatch')
  if times!=bt:raise ValueError('Do not silently interpolate mismatched time grids')
  corrected=[v-b for v,b in zip(values,bv)]
  if corrected[0]<=0:raise ValueError('Non-positive corrected initial absorbance')
  auc=integrate(times,[v/corrected[0] for v in corrected])
  out.append({'batch_id':key[0],'plate_id':key[1],'well':key[2],'candidate_id':meta['candidate_id'],'role':meta['role'],'concentration_uM':meta['concentration_uM'],'window_start_min':times[0],'window_end_min':times[-1],'normalized_auc_min':auc,'interpretation':'AUC only; Trolox calibration and vehicle subtraction require a separately approved model'})
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 with a.input.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not rows:raise SystemExit('No experimental data. No experimental result is generated.')
 out=analyze(rows);a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
