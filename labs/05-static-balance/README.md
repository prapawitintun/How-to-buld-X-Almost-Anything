# Lab 5: quasi-static support geometry

Run `python labs/05-static-balance/main.py`. Open `outputs/support.svg`.

The script takes coplanar contact points in meters, computes their counterclockwise convex hull, and measures the shortest distance from a supplied center-of-mass projection to that boundary. The sign is positive inside, zero on the boundary, and negative outside. The sample returns **0.08 m**.

Assumptions: fixed contacts on a horizontal plane, gravity only, adequate friction, and quasi-static behavior. The center of mass is a supplied input; it is not estimated from a full robot mass model. A positive margin does not prove walking stability, contact-force feasibility, friction feasibility, or resistance to perturbations.

Compare center, edge, outside, and degenerate contact cases. Next, use a dynamics framework to evaluate forces and contact transitions; record how the assumptions change.
