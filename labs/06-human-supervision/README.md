# Lab 6: human-supervised task states

Run `python labs/06-human-supervision/main.py`. The event log shows proposal → approval → start → stop; a direct restart is rejected; reset clears the task and requires a new proposal and approval.

This example has no authenticated operator, network, motor interface, real-time guarantees, hardware emergency stop, or certified safety function. Anyone calling `approve()` in this local process can approve. It illustrates state transitions, not a deployed authorization or robot safety system.

Test start-before-approval, changing tasks after approval, stop-before-start, repeated stop, reset, and completion. Next, separate operator identity and approval records from the controller, define what happens on connection loss, and validate physical stop behavior independently with qualified hardware support.
