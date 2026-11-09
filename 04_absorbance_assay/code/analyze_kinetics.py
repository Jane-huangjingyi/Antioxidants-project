"""Conservative trapezoidal-AUC preparation for actual, independently QC-cleared absorbance data."""
from pathlib import Path
import argparse,csv,collections,math,hashlib,json

TRACE_FIELDS=['candidate_id','concentration_uM','role','pair_id','counter_screen_pass','protocol_id','preparation_id','vehicle_id','time_origin']
ROLES={'SAMPLE','TROLOX','VEHICLE','MATCHED_NO_PROBE','PROBE_NO_INITIATOR','REAGENT_BLANK'}
def integrate(times,values):
 if len(times)<2 or len(times)!=len(values) or any(b<=a for a,b in zip(times,times[1:])):raise ValueError('Strictly increasing common time grid required')
 if not all(math.isfinite(v) for v in times+values):raise ValueError('Non-finite data cannot be imputed')
 return sum((b-a)*(x+y)/2 for a,b,x,y in zip(times,times[1:],values,values[1:]))
def analyze(rows):
 groups=collections.defaultdict(list)
 for r in rows:
  if any(r.get(f) is None or not str(r[f]).strip() for f in ['batch_id','plate_id','well']+TRACE_FIELDS):raise ValueError('Missing trace identity or protocol metadata')
  if r['role'] not in ROLES:raise ValueError('Unrecognized trace role: '+r['role'])
  if r['time_origin']!='INITIATOR_ADDITION':raise ValueError('time_min must be elapsed time since corresponding initiator addition; use the matched scheduled event for no-initiator controls')
  dose=float(r['concentration_uM'])
  if not math.isfinite(dose) or dose<0:raise ValueError('Finite nonnegative final concentration required')
  groups[(r['batch_id'],r['plate_id'],r['well'])].append(r)
 traces={}
 for key,items in groups.items():
  items.sort(key=lambda r:float(r['time_min']));meta=items[0]
  for r in items:
   for f in TRACE_FIELDS:
    if r[f]!=meta[f]:raise ValueError('Changing trace metadata: '+str(key))
  times=[float(r['time_min']) for r in items];values=[float(r['absorbance']) for r in items]
  if any(t<0 for t in times):raise ValueError('Negative elapsed time cannot enter post-initiation AUC')
  integrate(times,values)  # Validate all recorded traces, including controls.
  traces[key]=(meta,times,values)
 out=[]
 for key,(meta,times,values) in traces.items():
  if meta['role'] not in {'SAMPLE','TROLOX','VEHICLE'}:continue
  if meta['counter_screen_pass']!='YES':raise ValueError('No recorded interference clearance for '+str(key))
  pairs=[(m,t,v) for (batch,plate,_),(m,t,v) in traces.items() if (batch,plate)==key[:2] and m['pair_id']==meta['pair_id'] and m['role']=='MATCHED_NO_PROBE']
  if len(pairs)!=1:raise ValueError('One matched no-probe trace is required: '+str(key))
  background,bt,bv=pairs[0]
  for f in ['protocol_id','preparation_id','vehicle_id','time_origin']:
   if background[f]!=meta[f]:raise ValueError('Background protocol or preparation mismatch: '+f)
  if background['counter_screen_pass']!='YES':raise ValueError('Matched background lacks QC clearance')
  if background['candidate_id']!=meta['candidate_id'] or background['concentration_uM']!=meta['concentration_uM']:raise ValueError('Background dose or identity mismatch')
  if times!=bt:raise ValueError('Do not silently interpolate mismatched time grids')
  corrected=[v-b for v,b in zip(values,bv)]
  if corrected[0]<=0:raise ValueError('Non-positive corrected initial absorbance')
  auc=integrate(times,[v/corrected[0] for v in corrected])
  grid_hash=hashlib.sha256(json.dumps(times,separators=(',',':')).encode()).hexdigest()
  out.append({'batch_id':key[0],'plate_id':key[1],'well':key[2],'candidate_id':meta['candidate_id'],'role':meta['role'],'concentration_uM':meta['concentration_uM'],**{f:meta[f] for f in ['protocol_id','preparation_id','vehicle_id','time_origin']},'no_probe_well':background['well'],'window_start_min':times[0],'window_end_min':times[-1],'time_points':len(times),'time_grid_sha256':grid_hash,'corrected_initial_absorbance':corrected[0],'corrected_final_absorbance':corrected[-1],'corrected_min_absorbance':min(corrected),'corrected_max_absorbance':max(corrected),'normalized_auc_min':auc,'interpretation':'Diagnostic AUC normalized at first recorded time; no calibration, initial-signal acceptance or capacity validation inferred'})
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 with a.input.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not rows:raise SystemExit('No experimental data. No experimental result is generated.')
 out=analyze(rows)
 if not out:raise SystemExit('No SAMPLE, TROLOX or VEHICLE traces. No result generated.')
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
