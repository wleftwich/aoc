class Intcode:
    def __init__(self, program=None, pos=0, verbose=False):
        self.program = program
        self.pos = pos
        self.verbose = verbose
        self.input_buffer = []
        self.output = None
        self.xtramem = {}
        self.awaiting_input = False

    def run(self, inp=None, pos=0):
        if inp is None:
            inp = []
        if isinstance(inp, int):
            inp = [inp]
        self.input_buffer.extend(list(inp))
        self.output = None
        while pos is not None:
            pos = self.dispatch(pos)
        return self.output

    def step(self, inp=None):
        if self.pos is None:
            return self.output
        pos = self.pos
        if inp is None:
            inp = []
        if isinstance(inp, int):
            inp = [inp]
        self.input_buffer.extend(list(inp))
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
        opcode, param_modes = self.parse_opcode(self.program[pos])
        try:
            return self.functions[opcode](self, pos, param_modes)
        except KeyError:
            print('Bad opcode at pos', pos, self.program[pos])
            raise

    def get_opcode(self, pos):
        try:
            return self.program[pos]
        except IndexError:
            return self.xtramem[pos]

    def set_opcode(self, pos, opcode):
        try:
            self.program[pos] = opcode
        except IndexError:
            self.xtramem[pos] = opcode

    @staticmethod
    def parse_opcode(n):
        quotient, opcode = divmod(n, 100)
        L = []
        while quotient > 0:
            quotient, remainder = divmod(quotient, 10)
            L.append(remainder)
        return opcode, dict(enumerate(L))

    def f99(self, pos, param_modes=None):
        """Halt"""
        return

    def f1(self, pos, param_modes=None):
        """Add"""
        param_modes = param_modes or {}
        params = self.program[pos + 1:pos + 4]
        for i, param in enumerate(params[:2]):
            params[i] = param if param_modes.get(i) else self.program[param]
        self.program[params[2]] = params[0] + params[1]
        return pos + 4

    def f2(self, pos, param_modes=None):
        """Multiply"""
        param_modes = param_modes or {}
        params = self.program[pos + 1:pos + 4]
        for i, param in enumerate(params[:2]):
            params[i] = param if param_modes.get(i) else self.program[param]
        self.program[params[2]] = params[0] * params[1]
        return pos + 4

    def f3(self, pos, param_modes=None):
        """Input"""
        try:
            self.program[self.program[pos + 1]] = self.input_buffer.pop(0)
        except IndexError:
            self.awaiting_input = True
            return pos
        self.awaiting_input = False
        return pos + 2

    def f4(self, pos, param_modes=None):
        """Output"""
        param_modes = param_modes or {}
        param = pos + 1 if param_modes.get(0) else self.program[pos + 1]
        self.output = self.program[param]
        if self.verbose:
            print('Output', pos, self.program[param])
        return pos + 2

    def f5(self, pos, param_modes=None):
        """Jump if true"""
        param_modes = param_modes or {}
        params = self.program[pos+1:pos+3]
        for i, param in enumerate(params):
            params[i] = param if param_modes.get(i) else self.program[param]
        if params[0] != 0:
            return params[1]
        else:
            return pos + 3

    def f6(self, pos, param_modes=None):
        """Jump if false"""
        param_modes = param_modes or {}
        params = self.program[pos+1:pos+3]
        for i, param in enumerate(params):
            params[i] = param if param_modes.get(i) else self.program[param]
        if params[0] == 0:
            return params[1]
        else:
            return pos + 3

    def f7(self, pos, param_modes=None):
        """Less than"""
        param_modes = param_modes or {}
        params = self.program[pos + 1:pos + 4]
        for i, param in enumerate(params[:2]):
            params[i] = param if param_modes.get(i) else self.program[param]
        self.program[params[2]] = 1 if params[0] < params[1] else 0
        return pos + 4

    def f8(self, pos, param_modes=None):
        """Equals"""
        param_modes = param_modes or {}
        params = self.program[pos + 1:pos + 4]
        for i, param in enumerate(params[:2]):
            params[i] = param if param_modes.get(i) else self.program[param]
        self.program[params[2]] = 1 if params[0] == params[1] else 0
        return pos + 4

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
    }
