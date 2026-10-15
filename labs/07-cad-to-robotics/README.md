# Lab 7: CAD → fabrication layout → robot pick targets

Run `python labs/07-cad-to-robotics/main.py` from the repository root. The script uses Python's standard library and writes `outputs/cad-to-robotics.json`.

## What it connects

1. Four labeled rectangular CAD parts use millimeter dimensions.
2. The same parts are packed in original order and descending-height order on a 100 × 100 mm abstract sheet.
3. A dependency graph produces a deterministic pick sequence.
4. Part centers are converted into a robot frame in meters.
5. Analytic inverse kinematics calculates joint angles for a two-link planar arm; forward kinematics checks every target.

## Expected result

- Original ordering: **2 sheets**, **45% utilization**.
- Height ordering: **1 sheet**, **90% utilization**.
- Pick sequence: **P1 → P2 → P3 → P4**.
- Maximum endpoint error: below **1e-9 m** for the supplied numerical example.

The test suite checks unreachable targets, cyclic dependencies, missing parts, and unit conversion. Modify the dimensions or dependency graph to explore other cases; improvement is not guaranteed on every input.

## Limits

This is a bridge between geometry and robot calculations. It does not model grippers, joint limits, collisions, trajectories, vertical motion, friction, actual cutting spacing, or assembly forces. A reachable endpoint does not prove a feasible motion or successful physical handling.

Next, reproduce the target poses in a selected simulation framework and evaluate collision-aware paths before physical trials. See [HUMANOID.md](../../HUMANOID.md).
