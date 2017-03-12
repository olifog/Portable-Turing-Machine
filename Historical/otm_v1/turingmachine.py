# Turing Machine Simulator
# <Current state> <Current symbol> <New symbol> <Direction> <New state>

class TuringMachine(object):
    def __init__(self, tape):
        self.active = True
        self.state = "0"
        self.index = 0
        self.tape = list(tape)
        self.char = self.tape[self.index].replace(" ", "_")

    def __str__(self):
        return ''.join(self.tape)

    def load(fil):
    fil = open(fil, "r").readlines()
    ret = {}
    for line in fil:
        if not line[0] == ";" and not line == "\\n":
            linelis = line[:len(line) - 1].split(" ")
            if linelis[0] in ret.keys():
                ret[linelis[0]].append(linelis[1:])
            else:
                ret[linelis[0]] = [linelis[1:]]
    return ret

    def prune(self):
        while self.tape[0] == "_":
            if self.index > 0:
                self.index -= 1
                self.tape.pop(0)
            else:
                break
        while self.tape[len(self.tape) - 1] == "_":
            if self.index + 1 < len(self.tape):
                self.tape.pop(len(self.tape) - 1)
            else:
                break

    def moveright(self):
        self.index += 1
        if len(self.tape) < self.index + 1:
            self.tape.append(" ")

    def moveleft(self):
        self.index -= 1
        if self.index < 0:
            self.tape.insert(0, " ")
            self.index += 1

    def tick(self, program):
        notfound = True
        try:
            test = program[self.state]
        except:
            if self.state[:4] == "halt":
                self.active = False
            else:
                print("Error: no rule defined for state " + self.state)
            return

        for condition in program[self.state]:
            if condition[0] == self.char or condition[0] == "*":
                notfound = False
                if not condition[1] == "*":
                    self.tape[self.index] = condition[1]
                if condition[2] == "r":
                    self.moveright()
                elif condition[2] == "l":
                    self.moveleft()
                self.char = self.tape[self.index].replace(" ", "_")
                self.state = condition[3]
                break
        self.prune()
        if notfound:
            print("Error: no case for symbol " + self.char)

turmac = TuringMachine(input("Starting Tape:\t\t\t"))
prog = turmac.load(input("Program:\t\t\t\t"))
if input("Quiet mode?\t\t\t\t") == "y":
    loud = False
else:
    loud = True
while turmac.active:
    turmac.tick(prog)
    if loud:
        print(turmac)
print("Final tape:")
print(turmac)

