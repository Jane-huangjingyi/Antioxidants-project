"""Dimensionless thought experiment; no compound measurements or fitted assay model."""
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CONFIG=HERE/'inputs/simulation_scenarios.json'

def derivative(state,rate,flux,sink):
    probe,capacity,spent_sink=state
    denominator=probe+rate*capacity+sink
    return (-flux*probe/denominator,-flux*rate*capacity/denominator,flux*sink/denominator)

def trajectory(config,capacity,rate,step):
    """RK4; the third state records flux diverted to the fixed background sink."""
    count=round(config['end_time']/step)
    assert math.isclose(count*step,config['end_time'])
    state=(config['probe_initial'],capacity,0.0)
    states=[state]
    for _ in range(count):
        k1=derivative(state,rate,config['flux'],config['background_sink'])
        k2=derivative(tuple(x+step*k/2 for x,k in zip(state,k1)),rate,config['flux'],config['background_sink'])
        k3=derivative(tuple(x+step*k/2 for x,k in zip(state,k2)),rate,config['flux'],config['background_sink'])
        k4=derivative(tuple(x+step*k for x,k in zip(state,k3)),rate,config['flux'],config['background_sink'])
        state=tuple(x+step*(a+2*b+2*c+d)/6 for x,a,b,c,d in zip(state,k1,k2,k3,k4))
        assert all(math.isfinite(x) and x>=0 for x in state),'Invalid numerical state'
        states.append(state)
    # Radicals lost by probe and capacity plus sink consumption equal imposed flux.
    residual=max(abs(config['probe_initial']+capacity-s[0]-s[1]+s[2]-config['flux']*i*step) for i,s in enumerate(states))
    assert residual<1e-9
    return states,residual

def auc(states,start,end,step):
    first=round(start/step);last=round(end/step)
    assert math.isclose(first*step,start) and math.isclose(last*step,end)
    baseline=states[first][0]
    assert baseline>0 and first<last
    values=[s[0]/baseline for s in states[first:last+1]]
    return step*(sum(values)-(values[0]+values[-1])/2)

def calculate(config,step,fit):
    data={};max_balance_error=0.0
    for scenario in config['scenarios']:
        for dose in config['dose_grid']:
            states,residual=trajectory(config,scenario['capacity_per_dose']*dose,scenario['relative_capture_rate'],step)
            data[(scenario['id'],dose)]=states;max_balance_error=max(max_balance_error,residual)
    reference=next(s for s in config['scenarios'] if s['id']=='REFERENCE')
    vehicle=data[('REFERENCE',0.0)]
    # With no available antioxidant equivalents, capture-rate parameter has no effect.
    assert all(max(abs(a[0]-b[0]) for a,b in zip(data[(s['id'],0.0)],vehicle))<1e-12 for s in config['scenarios'])
    rows=[]
    for start in config['read_start']:
        for end in config['windows_end']:
            vehicle_auc=auc(vehicle,start,end,step)
            ref_points=[(dose,auc(data[('REFERENCE',dose)],start,end,step)-vehicle_auc) for dose in config['dose_grid']]
            ref_fit=fit(ref_points)
            assert ref_fit['slope']>0
            for scenario in config['scenarios']:
                points=[(dose,auc(data[(scenario['id'],dose)],start,end,step)-vehicle_auc) for dose in config['dose_grid']]
                fitted=fit(points)
                rows.append(dict(scenario=scenario['id'],label=scenario['label'],true_synthetic_capacity=scenario['capacity_per_dose'],
                                 capture_rate=scenario['relative_capture_rate'],read_start=start,window_end=end,
                                 slope=fitted['slope'],intercept=fitted['intercept'],residual_ss=fitted['residual_ss'],
                                 synthetic_reference_slope=ref_fit['slope'],diagnostic_slope_ratio=fitted['slope']/ref_fit['slope'],
                                 simulation_only='YES',unit='DIMENSIONLESS_NOT_MOLAR_TE',human_review_status='NOT_REVIEWED',change_applied='NO'))
    return rows,data,max_balance_error

def write_csv(path,rows):
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def run():
    config=json.loads(CONFIG.read_text())
    assert config['status']=='SIMULATION_ONLY_NOT_ASSAY_PARAMETERS'
    module_path=HERE.parent/'01_endpoint_definition/capacity_formula.py'
    spec=importlib.util.spec_from_file_location('capacity_formula',module_path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    coarse,_,coarse_balance=calculate(config,config['step'],module.slope_with_intercept)
    fine,data,fine_balance=calculate(config,config['step']/2,module.slope_with_intercept)
    convergence=max(abs(a['diagnostic_slope_ratio']-b['diagnostic_slope_ratio']) for a,b in zip(coarse,fine))
    assert convergence<1e-5,'Halving integration step did not establish numerical stability'
    main={row['scenario']:row for row in fine if row['read_start']==0 and row['window_end']==4}
    equal_ratio=main['EQUAL_FAST']['diagnostic_slope_ratio']/main['EQUAL_SLOW']['diagnostic_slope_ratio']
    assert equal_ratio>1,'Expected rate-confounding counterexample not present'
    for row in fine:
        if row['scenario']=='REFERENCE':assert math.isclose(row['diagnostic_slope_ratio'],1.0)
    # Independent implicit solution for zero antioxidant: C + s ln(C) = C0 + s ln(C0) - Jt.
    analytic_errors=[]
    for time in [2.0,4.0]:
        initial=config['probe_initial'];sink=config['background_sink']
        target=initial+sink*math.log(initial)-config['flux']*time
        lower,upper=1e-100,initial
        for _ in range(100):
            middle=(lower+upper)/2
            if middle+sink*math.log(middle)>target:upper=middle
            else:lower=middle
        numerical=data[('REFERENCE',0.0)][round(time/(config['step']/2))][0]
        analytic_errors.append(abs(numerical-(lower+upper)/2))
    assert max(analytic_errors)<1e-7
    traces=[];step=config['step']/2;stride=round(.05/step)
    for scenario in config['scenarios']:
        states=data[(scenario['id'],config['trace_display_dose'])]
        for index in range(0,len(states),stride):
            traces.append(dict(scenario=scenario['id'],label=scenario['label'],time=index*step,probe_remaining=states[index][0],
                               available_synthetic_capacity=states[index][1],dose=config['trace_display_dose'],simulation_only='YES'))
    results=HERE/'results';results.mkdir(exist_ok=True)
    write_csv(results/'Synthetic_Endpoint_Sensitivity.csv',fine)
    write_csv(results/'Synthetic_Probe_Traces.csv',traces)
    group_ranges=[]
    for scenario in config['scenarios']:
        ratios=[r['diagnostic_slope_ratio'] for r in fine if r['scenario']==scenario['id']]
        group_ranges.append(dict(scenario=scenario['id'],ratio_min=min(ratios),ratio_max=max(ratios)))
    summary={'status':'SIMULATION_ONLY_NOT_EMPIRICAL_ASSAY_MODEL','equal_capacity_fast_to_slow_ratio_at_start0_end4':equal_ratio,
             'maximum_ratio_change_when_halving_step':convergence,'maximum_flux_balance_error':max(coarse_balance,fine_balance),
             'maximum_zero_dose_analytic_error':max(analytic_errors),
             'diagnostic_rows':len(fine),'scenario_ranges':group_ranges,'compound_measurements':0,'formal_model_fitted':False,
             'scientific_interpretation':'Under the specified toy assumptions, normalized-AUC slope ratios depend on capture rate and acquisition window. They do not identify intrinsic radical equivalents per molecule.',
             'boundary':'No fitted crocin chemistry, real compound parameter, assay recommendation or real-world ranking reversal is inferred.',
             'sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [CONFIG,module_path,Path(__file__)]}}
    (results/'simulation_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['status','equal_capacity_fast_to_slow_ratio_at_start0_end4','maximum_ratio_change_when_halving_step','maximum_flux_balance_error']}))

if __name__=='__main__':
    run()
