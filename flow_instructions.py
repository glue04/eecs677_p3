# if a line is one of these instructions, call it's respective function to operate on the critical data


def store(cl, cd):
    if cl[2] in cd.reg and cl[4] not in cd.reg:
        cd.regadd(cl[4])
    
    elif cl[2] not in cd.reg and cl[4] in cd.reg:
        cd.tainted = True
    

def load(cl, cd):
    if cl[5] in cd.reg and cl[0] not in cd.reg:
        cd.regadd(cl[0])

def alloca(cl, cd):
    pass

def SOURCE(cl, cd):
    cd.regadd(cl[0])

def SINK(cl, cd):
    if cl[3] in cd.reg and not cd.tainted:
        return "FLOW"
    
    else:
        return "NO FLOW"