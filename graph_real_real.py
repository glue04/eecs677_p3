import instructions as inc

class critical_data:
    def __init__(self):
        self.reg = []
        self.tainted = False

    def regadd(self, new_reg):
        if new_reg not in self.reg:
            self.reg.append(new_reg)
    
    def __str__(self):
        return f"reg: {self.reg}"

def _clean_str(str):
    lststr = list(str)
    for i in range(0, len(lststr)):
        if lststr[i] == ',' or lststr[i] == ')':
            lststr[i] = ''
    
    return ''.join(lststr)

def clean_line(lst):
    for i in range(0, len(lst)):
        lst[i] = _clean_str(lst[i])
    
    return lst

def profile(fn):
    lines = []
    line_num = -1
    source_line = -1
    sink_line = -1

    inp = open(fn, "r")
    for line in inp:
        line_num += 1
        line = line.split()
        lines.append(clean_line(line))
        
        for arg in line:
            if "@SOURCE" in arg and "declare" not in line: # detects only the calls, not the declarations
                source_line = line_num

            elif "@SINK" in arg and "declare" not in line: # what he said
                sink_line = line_num

    inp.close()

    return lines, source_line, sink_line

def srcsnkanalysis(fn):
    lines, source_line, sink_line = profile(fn)
    print(lines)
    cd = critical_data()
    for i in lines:
        if '@SOURCE(' in i and i[0] != 'declare':
            inc.SOURCE(i, cd)
            print("SOURCE", cd)
        
        elif '@SINK(i32' in i and i[0] != 'declare':
            print(inc.SINK(i, cd))
            print("SINK", cd)
        
        elif 'store' in i:
            inc.store(i, cd)
            print('store', cd)

        elif 'load' in i:
            inc.load(i, cd)
            print('load', cd)


if __name__ == "__main__":
    srcsnkanalysis("ex3.ll")