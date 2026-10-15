# Lab 1: numbered panel geometry

Run `python labs/01-panel-geometry/main.py --width 180 --height 120 --id P001` from the repository root. It writes `outputs/panel.svg`, with a closed rectangular boundary in millimeters and a text identifier.

Inspect the SVG at a 1:1 scale. Red is the suggested cut boundary and black is the suggested marking; machine software must be configured separately. The path describes the nominal edge. It has no automatic kerf compensation, toolpath, joints, or structural validation.

**Check:** compare dimensions with a trusted viewer and verify the boundary closes. **Next:** add explicit splitting and rejoining rules with preserved parent/child identities. This panel exercise is a starter for planar grammar, not a complete grammar implementation.
