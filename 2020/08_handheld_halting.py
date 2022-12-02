with open(datafile) as fh:
    data = [x.strip() for x in fh]

    
class Gameboy:
    def __init__(self, prg):
        self.prg = prg.copy()
        self.restart()
    
    def restart(self):
        self.counter = 0
        self.accum = 0
        self.p = 0
        self.visited = set()
    
    def step(self):
        inst = self.prg[self.p]
        cmd, arg = inst.split()
        arg = int(arg)
        if cmd == 'nop':
            nextp = self.p + 1
        elif cmd == 'acc':
            self.accum += arg
            nextp = self.p + 1
        elif cmd == 'jmp':
            nextp = self.p + arg
        else:
            raise ValueError('Unknown command: %s' % cmd)
        
        if nextp in self.visited:
            raise ProgramError("Infinite loop! counter=%s, p=%s, nextp=%s, accum=%s" %
                               (self.counter, self.p, nextp, self.accum))
        
        self.visited.add(self.p)
        self.p = nextp
        self.counter += 1
    
    def run(self):
        halting_pos = len(self.prg)
        while self.p != halting_pos:
            self.step()
        return self.accum
       
            
class ProgramError(Exception):
    pass


gb = Gameboy(data)
try:
    gb.run()
except ProgramError as e:
    part_1 = gb.accum
else:
    print("Nothing wrong with this Gameboy")
    part_1 = None


class GameboyDebugger:
    def __init__(self, gameboy):
        self.gb = gameboy

    def setup(self):
        try:
            self.gb.run()
        except ProgramError as e:
            print("Gameboy error: ", e)
            print("Run debug to repair")
        else:
            print("Gameboy ran to completion, nothing to debug")
            return False
        self.gb_prg_indices = sorted(x for x in self.gb.visited
                                     if self.gb.prg[x].startswith(('nop', 'jmp')))
        return True

    def debug(self):
        for gbi in self.gb_prg_indices:
            self.gb.restart()
            inst = self.gb.prg[gbi]
            cmd, arg = inst.split()
            if cmd == 'nop':
                newcmd = 'jmp'
            else:
                newcmd = 'nop'
            self.gb.prg[gbi] = newcmd + ' ' + arg
            try:
                self.gb.run()
            except ProgramError:
                self.gb.prg[gbi] = inst
            else:
                print("Debug complete, your Gameboy is fine now")
                self.gb.restart()
                return True
        print("Sorry, couldn't fix your Gameboy")
        return False

    
gb = Gameboy(data)
gbdb = GameboyDebugger(gb)
gbdb.setup()
gbdb.debug()
part_2 = gb.run()
