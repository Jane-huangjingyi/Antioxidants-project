"""Candidate operational molar-capacity formula, with synthetic checks only.

Inputs are interference-cleared dose-level mean net AUCs, after vehicle subtraction,
for compound and Trolox measured under the same protocol. This function does not
approve linearity, choose assay settings, estimate pooled variance or fit new data.
"""
import math
def slope_with_intercept(points):
 if len(points)<3:raise ValueError('At least three distinct dose levels are required for this diagnostic fit')
 x=[float(p[0]) for p in points];y=[float(p[1]) for p in points]
 if not all(math.isfinite(v) for v in x+y) or min(x)<0:raise ValueError('Finite nonnegative concentrations and finite responses required')
 if len(set(x))!=len(x):raise ValueError('Supply one mean per dose; do not count technical wells as distinct doses')
 xm=sum(x)/len(x);ym=sum(y)/len(y);sxx=sum((v-xm)**2 for v in x)
 slope=sum((a-xm)*(b-ym) for a,b in zip(x,y))/sxx
 intercept=ym-slope*xm;residual_ss=sum((b-intercept-slope*a)**2 for a,b in zip(x,y))
 return {'slope':slope,'intercept':intercept,'residual_ss':residual_ss,'dose_levels':len(x)}
def molar_capacity_candidate(compound_points,trolox_points):
 compound=slope_with_intercept(compound_points);reference=slope_with_intercept(trolox_points)
 if reference['slope']<=0:raise ValueError('Trolox response must have a positive slope')
 ratio=compound['slope']/reference['slope']
 return {'molar_TE_candidate':ratio,'compound_fit':compound,'reference_fit':reference,'status':'CONDITIONAL_FORMULA_NOT_ASSAY_VALIDATION','interpretation':'POSITIVE_PROTECTION' if ratio>0 else 'NONPOSITIVE_RESPONSE_RETAINED_NOT_LOG_TRANSFORMED','uncertainty':'NOT_ESTIMATED_WITHOUT_BATCH_DESIGN_AND_SHARED_CALIBRATION_COVARIANCE'}
def synthetic_checks():
 reference=[(0,2),(1,5),(2,8)];compound=[(0,7),(1,13),(2,19)]
 assert math.isclose(molar_capacity_candidate(compound,reference)['molar_TE_candidate'],2)
 assert math.isclose(molar_capacity_candidate([(x,y+10) for x,y in compound],reference)['molar_TE_candidate'],2)
 assert molar_capacity_candidate([(0,2),(1,1),(2,0)],reference)['molar_TE_candidate']<0
 try:molar_capacity_candidate(compound,[(0,1),(1,1),(2,1)])
 except ValueError:pass
 else:raise AssertionError('Flat calibration must fail')
 print('Synthetic formula checks PASS; no experimental performance or ranking inferred.')
if __name__=='__main__':synthetic_checks()
