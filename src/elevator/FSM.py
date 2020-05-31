def ParamCheck(*ty, **argv):
    ty = map(to_check_fun, ty)
    argv = dict((i, to_check_fun(argv[i])) for i in argv)

    def common(fun):
        def deal(*fun_x, **fun_y):
            if ty:
                x_list = [a for a in fun_x]
                x_list_it = iter(x_list)
                result = []
                for t_check in ty:
                    r = t_check(next(x_list_it))
                    result.append(r)

                print('param check result: ', result)

            if argv:
                y_dic = dict((i, fun_y[i]) for i in fun_y)
                result = {}
                for k in argv.keys():
                    f = argv[k](y_dic.get(k))
                    result[k] = f
                print('param check result: ', result)

            return fun(*fun_x, **fun_y)

        return deal

    return common


def to_check_fun(t):

    return lambda x:isinstance(x,t)

class StateMachine:
    def __init__(self):
        self.handlers = {}  # State transfer function dictionary
        self.startState = None  # initial state
        self.endStates = []  # Final state list
        self.runResult = 0
    # def arg_zero(f):
    #     def arg_zerod(self, *args, **kwargs):
    #         # print("{}(*{}, **{}) START".format(f.__name__, args, kwargs))
    #         if len(args) == 0:
    #             return f(self, *args, **kwargs)
    #         else:
    #             print('Input error!')
    #             return 'Input error!'
    #     return arg_zerod

    # @arg_zero
    #The parameter "name" is the name of the state, the handler is the state transfer function,
    # and end_state indicates whether it is the final state
    @ParamCheck(object,str,object,int)
    def add_state(self, name, handler, end_state=0):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    # @arg_zero
    @ParamCheck(object,str)
    def set_start(self, name):
        self.startState = name


    # @arg_zero
    @ParamCheck(object,list)
    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise InitializationError("at least one state must be an end_state")

        # Start running from "Start state"
        flag = 0
        for input_data in cargo:
            new_state = handler(input_data)  # Transform to a new state after a state transition function
            if new_state in self.endStates:  # If it transitions to the end state, print the state and end the loop
                self.runResult = "arrived "+new_state
                print(self.runResult)
                flag = 1
                break
            else:  # Otherwise, switch the transfer function to the transfer function in the new state
                handler = self.handlers[new_state]
        if flag is 0:
            self.runResult = "not arrive end state"
            print(self.runResult)


class InitializationError(Exception):
    def __init__(self,arg):
        self.arg = arg

    def __str__(self):
        print(self.arg)