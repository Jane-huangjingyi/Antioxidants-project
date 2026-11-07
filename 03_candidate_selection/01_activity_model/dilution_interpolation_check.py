"""Synthetic double-log interpolation check; not a validated ORAC implementation.

Does not define AUC, its sign, unit conversion or select Watanabe method A/B.
"""
import math
def target_dilution(d1,a1,d2,a2,target):
    if not all(math.isfinite(x) and x>0 for x in [d1,a1,d2,a2,target]):
        raise ValueError('Positive finite dilution factors and responses required')
    if d1==d2 or a1==a2:raise ValueError('Distinct dilution factors and responses required')
    if not min(a1,a2)<=target<=max(a1,a2):raise ValueError('Target must be bracketed; no extrapolation')
    return math.exp(math.log(d1)+(math.log(target)-math.log(a1))*(math.log(d2)-math.log(d1))/(math.log(a2)-math.log(a1)))
if __name__=='__main__':
    assert math.isclose(target_dilution(10,40,20,20,30),400/30)
    assert math.isclose(target_dilution(20,20,10,40,30),400/30)
    for args in [(10,40,20,20,50),(10,0,20,20,10),(10,20,20,20,20)]:
        try:target_dilution(*args)
        except ValueError:pass
        else:raise AssertionError('Invalid interpolation accepted')
    print('PASS: synthetic log interpolation only; not experimental or protocol validation')
