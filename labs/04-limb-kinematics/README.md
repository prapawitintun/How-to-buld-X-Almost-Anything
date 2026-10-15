# Lab 4: humanoid limb kinematics

Run `python labs/04-limb-kinematics/main.py` from the repository root. Open `outputs/limb.svg`. Only Python's standard library is needed.

The model is an open planar chain with revolute joints, not a full humanoid. Lengths are in meters; joint angles are relative angles in radians, accumulated along the chain. `jacobian()` returns one `[dx/dq, dy/dq]` column per joint.

The script compares the analytic endpoint Jacobian with central finite differences and reports the largest error. Expected error on the included sample is below `1e-7`. Test a straight limb, a folded limb, and invalid lengths with `scripts/validate.py`.

This checks geometric calculations only. There are no torques, limits, collisions, contacts, motors, or learning policies. Next, reproduce a comparable limb in a selected robot-model framework and compare frame conventions before adding dynamics.
