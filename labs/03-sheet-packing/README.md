# Lab 3: compare packing against a baseline

Run `python labs/03-sheet-packing/main.py`. Four synthetic rectangles use a 100 × 100 mm bed. The same shelf heuristic receives either the original order or a descending-height order.

Expected result: original order uses **2 sheets with 45% utilization**; height order uses **1 sheet with 90% utilization**. This selected example illustrates a measurable improvement over that baseline. It does not establish that the heuristic improves every input or is globally optimal.

The model omits rotation, irregular outlines, margins, kerf spacing, clamps, grain, and tool travel. Parts can touch, so its output is an abstract placement rather than a production-ready cut layout.

**Next experiment:** fix a dataset of multiple part sets and compare both methods with identical constraints. Report sheet count, utilization, runtime, infeasible cases, and cases where no improvement occurs. Inspect every placement for boundary violations and overlap.
