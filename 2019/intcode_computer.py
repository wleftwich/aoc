class Intcode:
    def __init__(self, program=None, pos=0, verbose=False):
        self.program = Program(program)
        self.pos = pos
        self.verbose = verbose
        self.input_buffer = None
        self.output = None
        self.relative_base = 0
        self.awaiting_input = False
        self.halted = False

    def run(self, inp=None, pos=0):
        if self.halted:
            raise StopIteration("Program has halted")
        if inp is None:
            inp = []
        if isinstance(inp, int):
            inp = [inp]
        self.input_buffer.extend(list(inp))
        self.output = None
        self.awaiting_input = False
        while pos is not None:
            pos = self.dispatch(pos)
            if self.awaiting_input:
                print("Awaiting input", pos)
                break
        return self.output

    def step(self, inp=None):
        if self.halted:
            raise StopIteration("Program has halted")
        if self.pos is None:
            return self.output
        pos = self.pos
        if inp is not None:
            self.input_buffer = inp
        self.awaiting_input = False
        while pos is not None:
            pos = self.dispatch(pos)
            if self.output is not None or self.awaiting_input:
                output = self.output
                self.output = None
                self.pos = pos
                return output
        self.pos = pos

    def dispatch(self, pos):
        opcode = self.program.get(pos)
        funkey, param_modes = self.parse_opcode(opcode)
        try:
            return self.functions[funkey](self, pos, param_modes)
        except KeyError:
            print(pos, opcode, funkey, param_modes)
            raise

    def get_params(self, pos, nparams):
        return [self.program.get(x) for x in range(pos+1, pos+1+nparams)]

    @staticmethod
    def parse_opcode(opcode):
        quotient, funkey = divmod(opcode, 100)
        L = []
        while quotient > 0:
            quotient, remainder = divmod(quotient, 10)
            L.append(remainder)
        return funkey, dict(enumerate(L))

    def modify_param(self, p, mode):
        mode = mode or 0
        if mode == 0:
            v = self.program.get(p)
        elif mode == 1:
            v = p
        elif mode == 2:
            v = self.program.get(p + self.relative_base)
        else:
            raise KeyError("Bad mode: %s" % mode)
        return v

    def modify_pos(self, p, mode):
        mode = mode or 0
        if mode == 2:
            v = p + self.relative_base
        else:
            v = p
        return v

    def f99(self, pos, param_modes=None):
        """Halt"""
        self.halted = True
        return

    def f1(self, pos, param_modes=None):
        """Add"""
        param_modes = param_modes or {}
        a, b, out = self.get_params(pos, 3)
        a = self.modify_param(a, param_modes.get(0))
        b = self.modify_param(b, param_modes.get(1))
        out = self.modify_pos(out, param_modes.get(2))
        self.program.set(out, a + b)
        return pos + 4

    def f2(self, pos, param_modes=None):
        """Multiply"""
        param_modes = param_modes or {}
        a, b, out = self.get_params(pos, 3)
        a = self.modify_param(a, param_modes.get(0))
        b = self.modify_param(b, param_modes.get(1))
        out = self.modify_pos(out, param_modes.get(2))
        self.program.set(out, a * b)
        return pos + 4

    def f3(self, pos, param_modes=None):
        """Input"""
        param_modes = param_modes or {}
        (out,)  = self.get_params(pos, 1)
        out = self.modify_pos(out, param_modes.get(0))
        if self.input_buffer is None:
            if self.verbose:
                print("Awaiting input", pos)
            self.awaiting_input = True
            return pos
        else:
            self.program.set(out, self.input_buffer)
            self.input_buffer = None

        self.awaiting_input = False
        return pos + 2

    def f4(self, pos, param_modes=None):
        """Output"""
        param_modes = param_modes or {}
        (val,)  = self.get_params(pos, 1)
        val = self.modify_param(val, param_modes.get(0))
        self.output = val
        if self.verbose:
            print('Output', pos, val)
        return pos + 2

    def f5(self, pos, param_modes=None):
        """Jump if true"""
        param_modes = param_modes or {}
        tst, iftrue = self.get_params(pos, 2)
        tst = self.modify_param(tst, param_modes.get(0))
        iftrue = self.modify_param(iftrue, param_modes.get(1))
        if tst != 0:
            return iftrue
        else:
            return pos + 3

    def f6(self, pos, param_modes=None):
        """Jump if false"""
        param_modes = param_modes or {}
        tst, iffalse = self.get_params(pos, 2)
        tst = self.modify_param(tst, param_modes.get(0))
        iffalse = self.modify_param(iffalse, param_modes.get(1))
        if tst == 0:
            return iffalse
        else:
            return pos + 3

    def f7(self, pos, param_modes=None):
        """Less than"""
        param_modes = param_modes or {}
        a, b, out = self.get_params(pos, 3)
        a = self.modify_param(a, param_modes.get(0))
        b = self.modify_param(b, param_modes.get(1))
        out = self.modify_pos(out, param_modes.get(2))
        result = 1 if a < b else 0
        self.program.set(out, result)
        return pos + 4

    def f8(self, pos, param_modes=None):
        """Equals"""
        param_modes = param_modes or {}
        a, b, out = self.get_params(pos, 3)
        a = self.modify_param(a, param_modes.get(0))
        b = self.modify_param(b, param_modes.get(1))
        out = self.modify_pos(out, param_modes.get(2))
        result = 1 if a == b else 0
        self.program.set(out, result)
        return pos + 4

    def f9(self, pos, param_modes=None):
        """Adjust relative base"""
        param_modes = param_modes or {}
        (adj,) = self.get_params(pos, 1)
        adj = self.modify_param(adj, param_modes.get(0))
        self.relative_base += adj
        return pos + 2

    functions = {
        99: f99,
        1: f1,
        2: f2,
        3: f3,
        4: f4,
        5: f5,
        6: f6,
        7: f7,
        8: f8,
        9: f9,
    }


class Program:
    def __init__(self, L):
        if L is not None:
            self.D = dict(enumerate(L))
        else:
            self.D = {}

    def get(self, pos):
        return self.D.get(pos, 0)

    def set(self, pos, val):
        self.D[pos] = val