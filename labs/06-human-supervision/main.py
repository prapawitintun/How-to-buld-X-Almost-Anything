"""Illustrative task approval and latched stop state machine. No hardware interface."""
from enum import Enum
import json

class State(str,Enum):
    IDLE='idle';PROPOSED='proposed';APPROVED='approved';RUNNING='running';STOPPED='stopped'

class Supervisor:
    def __init__(self):self.state=State.IDLE;self.task=None;self.events=[]
    def _event(self,event):self.events.append({'event':event,'state':self.state.value,'task':self.task})
    def propose(self,task):
        if self.state!=State.IDLE or not isinstance(task,str) or not task.strip():raise ValueError('A new task requires idle state and nonempty text.')
        self.task=task;self.state=State.PROPOSED;self._event('propose')
    def approve(self):
        if self.state!=State.PROPOSED:raise ValueError('Only a proposed task may be approved.')
        self.state=State.APPROVED;self._event('approve')
    def start(self):
        if self.state!=State.APPROVED:raise ValueError('Execution requires task approval.')
        self.state=State.RUNNING;self._event('start')
    def stop(self):
        self.state=State.STOPPED;self._event('stop')
    def reset(self):
        if self.state!=State.STOPPED:raise ValueError('Reset requires stopped state.')
        self.task=None;self.state=State.IDLE;self._event('reset')
    def complete(self):
        if self.state!=State.RUNNING:raise ValueError('Only a running task can complete.')
        self.state=State.IDLE;self._event('complete');self.task=None

if __name__=='__main__':
    s=Supervisor();s.propose('SIMULATED: place panel P001 on table');s.approve();s.start();s.stop()
    try:s.start()
    except ValueError as e:print('Blocked restart:',e)
    s.reset();s.propose('SIMULATED: place panel P001 on table');s.approve();s.start();s.complete()
    print(json.dumps({'scope':'software-only teaching model; no operator authentication or motor stop','events':s.events,'final_state':s.state.value},indent=2))
