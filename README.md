# cpo-lab2
Computational Process Organization lab2

## Title: StateMachine

eDSL for finite state machine (mealy).

## List of group members

- Zhao Ji
  - ID: 192050213
  - Email :[1986081114@qq.com](mailto:1986081114@qq.com)
- Duan Shoujian
  - ID: 192050215

## Laboratory work number: 2

## Variant description

eDSL for finite state machine (mealy).

- Visualization as a state diagram (GraphViz DOT) or table (ASCII).
- Provide complex an example like a controller for an elevator, crossroad with a traffific light, etc.

## To work together:

Complete the disevent class together，Zhao Ji finished disevent.py  code module writing.
Duan Shoujian completed the disevent_test modules and Visualization.



## Code Introduction:

#### src/disevent.py:

class StateMachineis a class of finite state machine . 

member variables:

```python
self.handlers = {}  # State transfer function dictionary
self.startState = None  # initial state
self.endStates = []  # Final state list
self.runResult = 0  # The result of function run
self.state = []  # To collect all state
self.trans = {}  # Transfer process information
self.trans_to = {} # "Key" state can be transferred to "value" state
```

member methods:

```python
def add_state(self, name, handler, trans_to, end_state=0):
    '''
    Function introduction:Add state
    :param name:Name of the added state
    :param handler:State transition function of the state
    :param trans_to:The next state that this state allows to move to
    :param end_state:Is the state final state or not.
    :return:
    '''
```

```python
def add_trans_status(self, state, move):
    '''
    Function introduction:Add state transition information
    :param state:State name.
    :param move:Actions performed in this state/
    :return:
    '''
```

```python
def set_start(self, name):
    '''
    Function introduction:Set start state.
    :param name:State name.
    :return:
    '''
```

```python
def run(self, cargo):
    '''
    Function introduction:Running FSM.
    :param cargo:Input action list.
    :return:
    '''
```

```python
def visualize(self):
    '''
    Function introduction:Create dot code for graphviz.
    :return:
    '''
```

## conclusion:



1.The application of decorator pattern is necessary to effectively limit the format of input data and enhance the robustness of the code

2.Graphviz is a handy tool for data visualization, turning obscure lines of code into readable ones

3.According to the elevator example, different actions are performed by entering different values through the state machine.Understand the basic purpose of a finite state machine: to "run" in response to a series of events

