from collections import OrderedDict, namedtuple
import copy


event = namedtuple("Event", "clock node var val")
source_event = namedtuple("SourceEvent", "var val latency")


class StateMachine:
    def __init__(self):
        self.handlers = {}  # State transfer function dictionary
        self.startState = None  # initial state
        self.endStates = []  # Final state list
        self.runResult = 0  # The result of function run
        self.state = []  # To collect all state
        self.trans = {}  # Transfer process information
        self.trans_to = {} # "Key" state can be transferred to "value" state


    def ParamCheck(*ty2):
        def common(fun):
            def deal(*fun_x):
                ty = map(to_check_fun, ty2)
                if ty:
                    x_list = [a for a in fun_x]
                    x_list_it = iter(x_list)
                    RESULT.clear()
                    for t_check in ty:
                        r = t_check(x_list_it.__next__())
                        if r is False:
                            RESULT.append('false property')
                            return 'false property'
                    RESULT.append('true property')
                return fun(*fun_x)

            return deal
        return common



    @ParamCheck(object,str,object,(list,type(None)),int)
    def add_state(self, name, handler, trans_to, end_state=0):
        self.handlers[name] = handler
        self.state.append(name)
        self.trans_to[name] = trans_to
        if end_state:
            self.endStates.append(name)

    def add_trans_status(self, state, move):
        self.trans[state] = move

    @ParamCheck(object,str)
    def set_start(self, name):
        self.startState = name


    @ParamCheck(object,list)
    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            self.runResult ="must call .set_start() before .run()"
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            self.runResult ="at least one state must be an end_state"
            raise InitializationError("at least one state must be an end_state")

        flag = 0
        for input_data in cargo:
            new_state = handler(input_data)
            if new_state in self.endStates:
                self.runResult = "arrived "+new_state
                flag = 1
                break
            else:
                handler = self.handlers[new_state]
        if flag is 0:
            self.runResult = "not arrive end state"

    @ParamCheck(object)
    def visualize(self):
        res = []
        res.append("digraph G {")
        res.append("  rankdir=LR;")
        for v in self.state:
            res.append("  {}[];".format(v))


        for v in self.state:
            if self.handlers[v] is not None:
                for value in self.trans_to[v]:
                    res.append('  {} -> {}[label="{}"];'.format(v, value, self.trans[value]))


        res.append("}")

        return "\n".join(res)

def trace(f):
    def traced(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            print("{} FINISH".format(f.__name__))
    return traced



class InitializationError(Exception):
    def __init__(self,arg):
        self.arg = arg

    def __str__(self):
        print(self.arg)

RESULT = []
def to_check_fun(t):

        return lambda x: isinstance(x, t)

class Node(object):

    def __init__(self, name, function):
        self.function = function
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()

    def __repr__(self):
        return "{} inputs: {} outputs: {}".format(self.name, self.inputs, self.outputs)

    def arg_type(num_args, type_args):
        def trace(f):
            def traced(self, *args, **kwargs):
                if type(args[num_args - 1]) == type_args:
                    return f(self, *args, **kwargs)
                else:
                    print(type(args[num_args - 1]))
                    return 'Wrong Input!'

            return traced

        return trace

    @arg_type(1, str)
    def input(self, name, latency=1):

        assert name not in self.inputs
        self.inputs[name] = latency

    @arg_type(1, str)
    def output(self, name, latency=1):

        assert name not in self.outputs
        self.outputs[name] = latency

    @arg_type(1, dict)
    def activate(self, state):

        args = []
        for v in self.inputs:
            args.append(state.get(v, None))
        res = self.function(*args)
        if not isinstance(res, tuple):
            res = (res,)
        output_events = []
        for var, val in zip(self.outputs, res):
            latency = self.outputs[var]
            output_events.append(
                source_event(var, val, latency)
            )
        return output_events



