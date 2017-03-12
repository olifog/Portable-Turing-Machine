# Turing Machine Simulator
# <Current state> <Current symbol> <New symbol> <Direction> <New state>

class Otm(object):
    def __init__(self, tape=' '):
        self.active = True
        self.state = "0"
        self.line = None
        self.lastdir = None
        self.tape = list(tape)
        self.index = 0
        self.char = self.tape[self.index].replace(" ", "_")
        self.prog = {}

    def __str__(self):
        return ''.join(self.tape)

    def findchars(self):
        ret = [" "]
        for line in self.lisprog:
            if not line == "\n" and not line[0] == ";" and line[:len(line) - 1].split(" ")[1] not in ret:
                ret.append(line[:len(line) - 1].split(" ")[1])
        return ret

    def cropprog(self, height):
        ret = []
        try:
            possymbols = self.prog[self.state]
        except:
            return ["Finished!"]
        for symb in possymbols:
            realsymb = symb[0]
            if realsymb[0] == self.char or realsymb[0] == "*":
                linenumber = symb[1]
                break
        for x in range(height * 2):
            try:
                if linenumber - (height - x) < 0:
                    ret.append('\n')
                else:
                    ret.append(self.lisprog[linenumber - (height - x)])
            except:
                ret.append('\n')
        return ret

    def croptape(self, width):
        ret = ''
        if self.index - width < 0:
            for x in range(abs(self.index - width) - 1):
                ret += ' '
            ret += ''.join(self.tape)[:width + self.index]
            for x in range(width * 2 - len(ret) - 1):
                ret += ' '
        elif self.index + width > len(self.tape):
            ret += ''.join(self.tape[self.index - width + 1:])
            for x in range(width * 2 - len(ret) - 1):
                ret += ' '
        else:
            ret = ''.join(self.tape)[max(self.index - width + 1, 0):min(self.index + width, len(self.tape))]
        return ret.replace("_", " ")

    def load(self, fil):
        fil = open("../../otmp/" + fil + ".txt", "r").readlines()
        ret = {}
        for line in fil:
            if not line[0] == ";" and not line == "\\n":
                linelis = line[:len(line) - 1].split(" ")
                if linelis[0] in ret.keys():
                    ret[linelis[0]].append([linelis[1:], fil.index(line)])
                else:
                    ret[linelis[0]] = [[linelis[1:], fil.index(line)]]
        self.prog = ret
        self.lisprog = fil

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

    def tick(self):
        notfound = True
        try:
            test = self.prog[self.state]
        except:
            if self.state[:4] == "halt":
                self.active = False
            else:
                print("Error: no rule defined for state " + self.state)
            return

        for condition in self.prog[self.state]:
            conds = condition[0]
            if conds[0] == self.char or conds[0] == "*":
                notfound = False
                if not conds[1] == "*":
                    self.tape[self.index] = conds[1]
                lastdir = None
                if conds[2] == "r":
                    self.moveright()
                    self.lastdir = 'r'
                elif conds[2] == "l":
                    self.moveleft()
                    self.lastdir = 'l'
                self.char = self.tape[self.index].replace(" ", "_")
                self.state = conds[3]
                break
        self.prune()
        if notfound:
            print("Error: no case for symbol " + self.char)

if __name__ == "__main__":
    turmac = Otm(input("Starting Tape:\t\t\t"))
    turmac.load(input("Program:\t\t\t\t"))
    if input("Quiet mode?\t\t\t\t") == "y":
        loud = False
    else:
        loud = True
    while turmac.active:
        turmac.tick()
        if loud:
            print(turmac)
    print("Final tape:")
    print(turmac)
