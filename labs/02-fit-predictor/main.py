"""Predict clearance under a simplified centerline-cut model. Units: mm."""
import math
import json

def predict_fit(nominal_slot, thickness, kerf, thickness_uncertainty=0, kerf_uncertainty=0, acceptable=(0.02,0.15)):
    values=(nominal_slot,thickness,kerf,thickness_uncertainty,kerf_uncertainty,*acceptable)
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Inputs must be finite.')
    if nominal_slot<=0 or thickness<=0 or min(kerf,thickness_uncertainty,kerf_uncertainty)<0:
        raise ValueError('Dimensions must be positive and uncertainties nonnegative.')
    if thickness_uncertainty>=thickness or kerf_uncertainty>kerf or acceptable[0]>acceptable[1]:
        raise ValueError('Invalid uncertainty or acceptable interval.')
    # For an uncompensated centerline cut around an internal opening,
    # the material removed increases the opening by approximately one full kerf.
    clearance=nominal_slot+kerf-thickness
    uncertainty=thickness_uncertainty+kerf_uncertainty
    low,high=clearance-uncertainty,clearance+uncertainty
    eps=1e-9  # Avoid changing interval classifications due to floating-point rounding.
    if low>=acceptable[0]-eps and high<=acceptable[1]+eps: label='within_assumed_clearance_range'
    elif high<acceptable[0]-eps or low>acceptable[1]+eps: label='outside_assumed_clearance_range'
    else: label='uncertain'
    return {'clearance_mm':round(clearance,4),'interval_mm':[round(low,4),round(high,4)],'prediction':label}

if __name__=='__main__':
    print('SYNTHETIC demonstration — substitute measured thickness and kerf before experiments.')
    for slot in [2.85,2.90,2.95,3.00]:
        print(json.dumps({'nominal_slot_mm':slot,**predict_fit(slot,3.0,0.2,0.03,0.02)}))
