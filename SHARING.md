# Share one reproducible result

Start with one demo a reader can run. Adapt your description to each community and follow its posting rules. This guide does not send any messages.

## Demo: CAD panels to robot pick targets

**Audience:** computational design, digital fabrication, and robotics learners.

**Show:** the panel, two layout orderings, and recorded robot target positions. Explain that this is an educational 2D calculation, not a deployed assembly robot.

**Command:** `python labs/07-cad-to-robotics/main.py`

**Evidence:** the same four-part case uses two sheets in its original order and one after height sorting; computed arm endpoints reproduce planned pick targets. This selected case does not prove general packing superiority or physical assembly feasibility.

**Suggested post:**

> I connected a small CAD example to sheet packing and planar robot kinematics. Four labeled parts become a layout, a dependency order, and robot pick targets, with forward-kinematics checks. It runs offline with standard Python. I would welcome feedback on frame conventions, failure cases, and a useful next simulation experiment.

Link to the repository and exact lesson. Invite a specific contribution.

## Other demos to share separately

| Demo | Suitable readers | Useful feedback |
| --- | --- | --- |
| Numbered CAD panel | Beginner CAD and maker educators | Are the units and first-run steps clear? |
| Slot-fit intervals | Digital fabrication learners | Which measured material/kerf dataset should be tested next? |
| Limb Jacobian check | Robotics learners | Which singular or boundary case should be included? |

Record what readers reproduced and improve the lesson before sharing it more widely. Do not describe the project as officially endorsed by MIT or CodeCrafters.
