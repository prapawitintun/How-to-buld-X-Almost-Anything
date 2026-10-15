# Lab 2: slot clearance prediction

Run `python labs/02-fit-predictor/main.py`. All supplied values are synthetic. The assumed acceptable clearance interval is 0.02–0.15 mm; calibrate it for the material, joint, and process.

The model assumes an **uncompensated centerline cut around an internal opening**: effective slot width ≈ nominal width + kerf. Clearance is effective slot width minus measured material thickness. CAM kerf compensation changes this equation. The interval adds specified thickness and kerf uncertainty conservatively.

The labels describe predicted clearance only. They do not predict retention force, crushing, friction, swelling, delamination, strength, or assembly access.

**Physical validation:** measure thickness and cut kerf, calibrate on one coupon batch, freeze the parameters, predict a separate batch, and record measured clearance and fit outcomes. Report prediction errors and failed cases. Do not call this model validated until those experiments are complete.
