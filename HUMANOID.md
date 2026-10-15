# Build your own humanoid: a staged learning path

**Goal:** understand and evaluate articulated robot systems, progressing from small geometric exercises to simulated whole-body tasks. This release contains educational code and references; it does not supply a complete humanoid platform.

## Begin with software

1. Run [limb kinematics](labs/04-limb-kinematics/README.md). Check coordinates and the Jacobian numerically.
2. Run [static balance](labs/05-static-balance/README.md). Explore where its assumptions fail.
3. Run [human supervision](labs/06-human-supervision/README.md). Test invalid execution and restart attempts.

All three use standard Python and require no physical actuators.

## Select a simulation route

| Route | Role | What you must verify |
| --- | --- | --- |
| [MuJoCo](https://mujoco.readthedocs.io/en/stable/) + [Menagerie](https://github.com/google-deepmind/mujoco_menagerie) | Physics engine and robot-model collection | Model-specific license, frames, contact settings, engine version |
| [Drake](https://drake.mit.edu/) | Modeling, dynamics, planning, and control tools | Supported model format, solver setup, units, reproducibility |
| [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) | Robot-learning environments, including bipeds | Accelerator/dependency requirements, seeds, task and evaluation settings |
| [Isaac Lab](https://github.com/isaac-sim/IsaacLab) | Robot-learning simulation framework | Supported hardware/software stack and resource requirements |
| [LeRobot](https://huggingface.co/docs/lerobot/index) | Demonstration datasets and learning workflows | Supported robot interface and policy; it is not by itself a complete walking controller |
| [ROS 2](https://github.com/ros2/ros2_documentation), [ros2_control](https://github.com/ros-controls/ros2_control), [MoveIt](https://moveit.picknik.ai/main/index.html) | Communication, controller interfaces, and motion-planning infrastructure | Distribution compatibility, model interfaces, controller assumptions |

These are complementary resources, not interchangeable products. Choose one minimal route before adding another. No external framework was installed or benchmarked for this release.

## Progression and evidence gates

| Stage | Deliverable | Evidence needed before progressing |
| --- | --- | --- |
| 1. Geometry | Limb and frame definitions | Analytical examples and finite-difference checks agree |
| 2. Description | Model tree, limits, inertias, contacts | Parser validation, frame inspection, plausible mass properties |
| 3. Dynamics | Standing/contact scenario | Sensitivity study, force/contact observations, documented failures |
| 4. Control | One simulated reach or balance task | Tracking error, constraint violations, perturbation trials |
| 5. Learning | Imitation or reinforcement-learning baseline | Separate train/test conditions, multiple seeds, fixed comparison budget |
| 6. Integration | Supervised simulated assembly task | Task success, collision events, stop behavior, recovery, intervention count |
| 7. Physical pilot | One bounded task on suitable hardware | Independent process review, calibrated hardware, measured limits and stop behavior |

Walking, manipulation, conversation, and useful work are distinct claims. Demonstrating one does not establish the others. Simulation success is not evidence of successful transfer to a real robot.

## Runnable bridge from CAD to robotics

[Lab 7](labs/07-cad-to-robotics/README.md) implements the first numerical bridge: labeled panels → abstract sheet layout → dependency-ordered pick targets → two-link inverse kinematics → forward-kinematics checks. Run it before selecting a heavier simulation framework.

## Pilot connected to Pam's fabrication work

**Task:** arrange four labeled planar parts on a table in simulation, following an approved assembly sequence.

- **Input:** four panel outlines and identities, target poses, assembly dependencies, and an operator-approved task.
- **First baseline:** deterministic placement sequence on a fixed scene.
- **Candidate:** a planner that accounts for part availability and access constraints.
- **Hold constant:** geometry, scene, pose tolerance, collision constraints, and trial budget.
- **Measure:** successful placements, pose error, collisions, execution time, interventions, and failure recovery.
- **Later extension:** evaluate whether a humanoid body adds useful reach or mobility compared with a fixed arm. A humanoid is a hypothesis, not a required answer to every fabrication task.

This pilot connects CAD and planar grammar to robot evaluation while keeping the first task small enough to inspect and reproduce.

## Twelve linked subjects

Browse the Humanoid Robotics section in [README.md](README.md) for morphology, descriptions, kinematics, dynamics, balance, locomotion, manipulation, teleoperation, imitation learning, reinforcement learning, sim-to-real, and human supervision.
