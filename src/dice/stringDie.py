import random
# Lambda Functions
isIn = lambda a, *args: all([arg in a for arg in args])
anyIsIn = lambda a, *args: any([arg in a for arg in args])


class stringDie:
    def __init__(self, s):
        sym = "+-*/"
        inequ = '<>='
        rerolls = [
            'dl',  # drop lowest
            'kl',  # keep lowest
            'kh',  # keep highest
            'dh',  # drop highest
            'r',  # reroll
            'e'  # explode
        ]
        # print(*args)
        # TODO Add
        if isinstance(s, stringDie):
            self.copyFromDie(s)
        # check for constants
        elif s.isnumeric():
            s = self.buildBase(s)
            self.diequant = int(s)
            print('Caught Constant early')
        else:
            s = self.buildBase(s)
            slen = len(s)
            # Split by '+' and '-' and if none exist, '*' and '/'
            sd=[]
            signs=["+"]
            ind_md = [0]
            ind_inequ = [0]
            ind_as=[0]
            n=0
            obr = "{("
            cbr = "})"
            for i, l in enumerate(s):
                # Check if the number is inside a bracket
                n += 1 if l in obr else 0
                n -= 1 if l in cbr else 0
                # Split the string but signs that are not in brackets
                # print(l, n, i, ind)
                # print()
                if l in sym and n == 0:
                    signs.append(l)
                    if l in sym[:2]:
                        ind_as.append(i)
                    if l in sym[2:]:
                        ind_md.append(i)
                elif l in inequ and i > 0:
                    # Checking if the inequality symbol came after number/die/bracket or reroll condition
                    if not s[i-1].isalpha() and s[i-1] not in inequ:
                        ind_inequ.append(i)
            die = len(ind_as)
            # Multiple Die in string outside of brackets
            if len(ind_inequ)>1:
                # Checks if there were any inequalities
                print('Comparison Found')
                # print(ind_md)
                ind_inequ.append(slen)
                sd = [s[ind_inequ[i]:ind_inequ[i + 1]] for i in range(len(ind_inequ) - 1)]
            elif len(ind_md)>1:
                # Checks if there were any multiplication symbols
                print('Multiplication Found')
                # print(ind_md)
                ind_md.append(slen)
                sd = [s[ind_md[i]:ind_md[i + 1]] for i in range(len(ind_md)-1)]
                # print(ind_md,sd)
            elif die > 1:
                print('Addition Found')
                ind_as.append(slen)
                sd = [s[ind_as[i]:ind_as[i+1]]for i in range(die)]
            # Bracketed rolls
            elif not isIn(s,"{","}") and not isIn(s,"(",")"):
                # Check if there's any reroll modifiers
                r = [slen-s[::-1].find(re[::-1])-len(re) for re in rerolls if re in s]

                if len(r)>0:
                    print('Funky Roll', end='; ')
                    # print('%s is a funky roll ' % s)
                    # print("test check", s[max(r):])
                    dieStr, dq, dn = testDieString(s[:max(r)])
                    if dieStr:
                        sd = ['1d%s' % dn] * int(dq)
                        # print('Ignored SubDice: %s*1d%s'%(dq,dn))
                    else:
                        sd = [s[:max(r)]]
                    self.ignoreCond = s[max(r):]
                    print('Ignore Condition: %s' % (self.ignoreCond))
                else:
                    # Normal Die Roll
                    if s.isnumeric():
                        # print('%s is a constant ' % s)
                        print('Constant')
                        self.diequant = int(s)
                    else:
                        # print('%s is a standard die ' % s)
                        print('Standard Die')
                        br = s.find('d')
                        if s[:br] == "1":
                            self.dienum = int(s[br+1:])
                        else:
                            sd = ['1%s'%s[br:]] * int(s[:br])

            # Whole die string is in brackets
            elif (s[0], s[-1]) in [("{", "}"), ("(", ")")]:
                print('%s is in brackets' %s[1:-1])
                sd = s[1:-1].split(';')
                print(sd)
            # There's brackets but something at the end
            else:
                # Find the last reroll condition
                r = [slen - s[::-1].find(re[::-1])-len(re) for re in rerolls if re in s]
                print(slen, r, s[max(r):])
                print('%s is partially in brackets' % s)
                # If teh reroll condition is right after the brackets
                dieStr, dq, dn = testDieString(s[:max(r)])
                if dieStr:
                    print("a", "Text before reroll cond:", s[:max(r)],dn,dq)
                    sd = ['1d%s' % dn] * int(dq)
                elif (s[0], s[max(r)-1]) == ("{", "}"):
                    # Remove the brackets, pass the inside
                    print('%s is in brackets' % s[1:max(r)-1])
                    sd = s[1:max(r)-1].split(';')
                    dieStr, dq, dn = testDieString(sd[0])
                    if dieStr and len(sd) == 1:
                        sd = ['1d%s' % dn] * int(dq)
                    elif len(sd) > 1:
                        sd = [';%s'%a for a in sd]
                else:
                    # Pass the remaining string
                    sd = [s[:max(r)]]
                self.ignoreCond = s[max(r):]
                print('new roll: %s, ignore condititon %s' % (sd, self.ignoreCond))
            if len(sd) > 0:
                # print('Sub Dice', sd)
                self.subdice = [stringDie(die) for die in sd]
                self.diequant = len(sd)
    
    def buildBase(self, s):
        s = s.replace(" ", "").lower()
        self.string = s
        self.diequant = 0
        self.dienum = 1
        self.sign = '+'
        self.subdice = []
        # 0 to ignore the dice, 1 to keep it
        self.ignore = [1]
        self.constant = False
        self.value = None
        self.ignoreRoll = None
        self.ignoreCond = ""
        print("Rolling:", s, end='; ')
        # Remove spaces
        sign = '+'
        sym = "+-*/;"
        inequ = '<>='
        if s[0] in sym:
            sign = s[0]
            s = s[1:]
        elif s[0] in inequ and len(s)>1:
            i = 1 + (s[1] in inequ)
            sign = s[:i]
            s = s[i:]
        # print('sign is %s' % sign)
        self.sign = sign
        return s

    def copyFromDie(self, o):
        for k in list(o.__dict__.keys()):
            self.__setattr__(k, o.__getattribute__(k))
        self.subdice = [stringDie(sd) for sd in o.subdice]
        self.ignore = [1*i for i in self.ignore]
        if self.ignoreRoll:
            self.ignoreRoll = stringDie(self.ignoreRoll)

    def total(self):
        signDict = {
            '+': 1,
            '-': -1,
            '*': 1,
            '/': -1,
            ';': 0
        }
        dice = len(self.subdice)

        if dice > 0:
            [d.total() for d in self.subdice]
            self.checkignore()
            # [print(d.string, d.sign) for d in self.subdice]
            if self.isInequ():
                print()
                if dice>1:
                    for i,d in enumerate(self.subdice[1:]):
                        e = self.subdice[i]
                        inequBool, equalBool = False, False
                        if '<' in d.sign:
                            inequBool = e.value < d.value
                        elif '>' in d.sign:
                            inequBool = e.value > d.value
                        equalBool = e.value == d.value if '=' in d.sign else False
                        self.value = 1 if any([inequBool, equalBool]) else 0
                else:
                    self.value = 1
            elif self.isMult():
                self.value = self.subdice[0].value
                for i, d in enumerate(self.subdice[1:]):
                    if self.ignore[i+1] == 1:
                        self.value *= d.value ** signDict[d.sign]
            else:
                self.value = sum([self.ignore[i] * d.value * signDict.get(d.sign,1) for i, d in enumerate(self.subdice)])
        else:
            self.value = random.randint(1, self.dienum) if self.dienum > 1 else self.diequant
        # print(self.string,":",self.value)
        return self.value

    def subDiceFlatten(self):
        for die in self.subdice:
            die.subDiceFlatten()
            pass

    def isMult(self):
        return any([d.sign in '*/' for d in self.subdice])

    def isComp(self):
        return any([d.sign == ';' for d in self.subdice])

    def isInequ(self):
        return any([anyIsIn(d.sign, '<','>','=') for d in self.subdice])

    def dieLen(self):
        return len(self.subdice)

    def valueString(self):
        # TODO Update for ;
        string = ''
        string += self.sign
        l = len(self.sign)
        if len(self.subdice) < 1:
            string += str(self.value)
        # elif self.isMult():
        #     pass
        elif self.isComp():
            k = '; '.join([e.valueString() for e in self.subdice])
            string += "{%s}" % k
        else:
            for i, d in enumerate(self.subdice):
                # Check if there's several die to put the block in parentheses
                string += d.sign if i > 0 else ""
                if len(d.subdice)>0:
                    k = ''.join([e.sign+e.valueString() for e in d.subdice])
                    string += "(%s)"% k[len(d.sign):]
                # if not just add to the string
                else:
                    string += d.valueString()
                string += '*0' if self.ignore[i]==0 else ""
        return string[l:]

    def rolledMax(self):
        if len(self.subdice) > 0:
            return all([d.rolledMax() for d in self.subdice])
        elif self.dienum == 1:
            return True
        else:
            return self.value == self.dienum

    def rerollSubdice(self, *index, ignoreRerolled=True, offset = 0):
        print(index)
        print("Rerolling", index, ignoreRerolled, len(self.subdice), offset)
        for i in index:
            self.subdice.append(stringDie(self.subdice[i+offset]))
            self.subdice[-1].total()
            self.ignore.append(1)
            if ignoreRerolled:
                self.ignore[i+offset]=0

    def checkignore(self):
        self.ignore = [1]*len(self.subdice)
        if self.ignoreCond != "":
            v = [d.value for d in self.subdice]
            # Reroll
            if "r" in self.ignoreCond:
                print('Rerolling')
                once = self.ignoreCond[1] == 'o'
                equal = '=' in self.ignoreCond
                # Check for greater or less than operators
                ineq = ''
                ineqList = [i for i in '<>' if i in self.ignoreCond]
                if len(ineqList)>0:
                    ineq = ineqList[0]
                # Default to less than, in case of 'r6'
                elif not equal:
                    ineq = '<'
                print('rNum', self.ignoreCond, ineqList,once,self.ignoreCond[(1+len(ineqList)+once+equal):])
                # Create list of the index of every die that meets that condition
                # Find the comparison number
                self.ignoreRoll = stringDie(self.ignoreCond[(1 + len(ineqList) + once + equal):])
                rNum = self.ignoreRoll.total()

                rrDie = [i for i, d in enumerate(v)
                         if (d > rNum and ineq == '>') or (d == rNum and equal) or (d < rNum and ineq == '<')]
                # rrDie = []
                # for i, d in enumerate(v):
                #     print('Big Roll:' ,d, ineq, rNum, equal, (d > rNum and ineq == '>'), (d == rNum and equal), (d < rNum and ineq == '<'))
                #     if (d > rNum and ineq == '>') or (d == rNum and equal) or (d < rNum and ineq == '<'):
                #         rrDie.append(i)
                # If that list has any results, add to reroll list
                if len(rrDie) > 0:
                    self.rerollSubdice(*rrDie)

                #check if the new rolls meet the conditions.
                while not once and len(rrDie) > 0:
                    v = [d.value for d in self.subdice[-len(rrDie):]]
                    rrDie = [i for i, d in enumerate(v) if
                             (d > rNum and ineq == '>') or (d == rNum and equal) or (d < rNum and ineq == '<')]
                    offset = len(self.subdice)-len(rrDie)
                    self.rerollSubdice(*rrDie, offset=offset)
                    # self.explode(self.subdice[-len(exDie):], len(self.subdie)-len(exDie))
                    # reapply roll criteria function. nested?

            # Explode
            elif "e" in self.ignoreCond:
                self.explodeDice(v)
            else:
                print("Dropping", self.ignoreCond)
                # Drop
                self.keepDrop(v)

                # v[:kNum]

    def keepDrop(self, v):
        high = anyIsIn(self.ignoreCond, 'kh', 'dl')
        # Checking to see if the highest values are relevant.
        # kNum = int(self.ignoreCond[2:])
        # Keep Number
        self.ignoreRoll = stringDie(self.ignoreCond[2:])
        kNum = self.ignoreRoll.total()
        print('Keep Number:', kNum)
        # If the ignore cond is to drop dice, then the
        if 'd' in self.ignoreCond[:2]:
            kNum = len(self.subdice) - kNum
        #                 Find indexes of the highest kNum results.
        #                 kNum = min(kNum, len(self.subdice))
        vInd = [*v]
        # for d in self.subdice:
        #     vInd.append(d.value)
        #     v.append(d.value)
        print('Initial Values:', v)
        # Sort the values in descending order
        v.sort(reverse=True)
        print('Sorted Values:', v)
        # Take only the highest kNum values
        v = v[:kNum]
        print('Limited Values:', v)
        for i, val in enumerate(vInd):
            # Everytime v is
            if val in v:
                self.ignore[i] = 0
                v.remove(val)
            if high:
                self.ignore[i] = 1 - self.ignore[i]
        print('Ignored Indecies:',self.ignore)

    def explodeDice(self, v, offset=0):
        # Check exploding condition:
        self.ignoreRoll = stringDie(self.ignoreCond[1:])
        eNum = self.ignoreRoll.total()
        # Create list of the index of every die that meets that condition
        print('Exploding', v, eNum)
        exDie = [i for i, d in enumerate(v) if d >= eNum]
        # If that list has any results, reroll those die
        if len(exDie) > 0:
            self.rerollSubdice(*exDie, ignoreRerolled=False, offset=offset)
            sd = [d.value for d in self.subdice[-len(exDie):]]
            self.explodeDice(sd, len(self.subdice)-len(exDie))

    def toDict(self):
        d = { k: self.__getattribute__(k) for k in list(self.__dict__.keys())}
        d['subdice']=[sd.toDict() for sd in d['subdice']]
        if d['ignoreRoll'] != None:
            d['ignoreRoll'] = self.ignoreRoll.toDict()
        return d

def testDieString(s):
    # print("Testing", s)
    br = s.find('d')
    s = s.replace('d','')
    diequant: int = 0
    dienum: int = 0
    if br <= 1:
        diequant = s[:br]
        dienum = s[br:]
    return s.isnumeric() and br != 0, diequant, dienum


# test = [
#     # "{2d20; 10}kh1",
#     # "{2d20}+5",
# #     "{6d20}kh2",
# # "{6d20}dh2",
# # "{6d20}kl2",
# # "{6d20}dl2",
#     # "2d20-1d4","2d20kh1", "5",
#     #     "6*2d20", '2d10/2','6d4kh(1d4)',
#     # '{100d100; 5d2000}kh1',
#     '4d6e5',
#     '5d6r4',
#     '5d6ro>=3',
#     # '1d20+4>=10',
#     # '2d20kh1+5>=10'
# ]
# for d in test:
#     s = stringDie(d)
#     s.total()
#     print('Dice: %s=%s'%(s.value,s.valueString()))
#     print()
# k = stringDie(s)
# k.dienum = 6
# print(k.toDict())
# print(s.toDict())
# print(s.isInequ())
# #

# # print(1*True, 1*False)
