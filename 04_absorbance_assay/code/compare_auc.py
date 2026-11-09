"""Explicit, matched-vehicle AUC contrasts; no capacity fit or uncertainty claim."""
import argparse
import csv
import json
import math
from pathlib import Path

MATCH_FIELDS=('batch_id','plate_id','protocol_id','preparation_id','vehicle_id',
              'time_origin','window_start_min','window_end_min','time_points','time_grid_sha256')

def key(row):
    return tuple(row[field] for field in ('batch_id','plate_id','well'))

def compare(rows,contrasts):
    if not rows or not contrasts:
        raise ValueError('Actual AUC rows and explicit vehicle assignments are required')
    bykey={key(row):row for row in rows}
    if len(bykey)!=len(rows):
        raise ValueError('Duplicate AUC trace keys')
    output=[]
    seen=set()
    for contrast in contrasts:
        sample_key=key(contrast['sample'])
        if sample_key in seen:
            raise ValueError('One vehicle assignment per sample is required')
        seen.add(sample_key)
        if sample_key not in bykey:
            raise ValueError('Assigned sample missing from AUC input')
        sample=bykey[sample_key]
        if sample['role'] not in {'SAMPLE','TROLOX'}:
            raise ValueError('Only SAMPLE or TROLOX receives a diagnostic contrast')
        vehicle_keys=[key(row) for row in contrast['vehicles']]
        if not vehicle_keys or len(set(vehicle_keys))!=len(vehicle_keys):
            raise ValueError('Nonempty unique vehicle references required')
        vehicles=[]
        for vehicle_key in vehicle_keys:
            if vehicle_key not in bykey:
                raise ValueError('Assigned vehicle missing from AUC input')
            vehicle=bykey[vehicle_key]
            if vehicle['role']!='VEHICLE':
                raise ValueError('Assigned reference is not a VEHICLE trace')
            for field in MATCH_FIELDS:
                if sample.get(field) is None or not str(sample[field]).strip() or str(sample[field])!=str(vehicle.get(field,'')):
                    raise ValueError('Incompatible sample/vehicle '+field)
            vehicles.append(vehicle)
        values=[float(row['normalized_auc_min']) for row in [sample]+vehicles]
        if not all(math.isfinite(value) for value in values):
            raise ValueError('Non-finite AUC cannot be imputed')
        mean_vehicle=sum(values[1:])/len(vehicles)
        net=values[0]-mean_vehicle
        output.append({**sample,'vehicle_wells_json':json.dumps([row['well'] for row in vehicles]),
                       'vehicle_technical_wells':len(vehicles),'vehicle_mean_auc_min':mean_vehicle,
                       'net_auc_min':net,'response_sign':'POSITIVE' if net>0 else 'NONPOSITIVE',
                       'interpretation':'Diagnostic matched-vehicle contrast; shared reference IDs retained; no TE, independent sample size, uncertainty or ranking inferred'})
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--assignments',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with args.input.open(encoding='utf-8-sig',newline='') as handle:
        rows=list(csv.DictReader(handle))
    assignments=json.loads(args.assignments.read_text(encoding='utf-8'))
    try:
        output=compare(rows,assignments['contrasts'])
    except (ValueError,KeyError) as error:
        raise SystemExit('No result generated: '+str(error))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(output[0]))
        writer.writeheader();writer.writerows(output)
