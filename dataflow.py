import flow_instructions as finc
import path_instructions as pinc
import sys

# class that has 2 members, one is a list of all registers that contain the source data, and a bool that says if the value has been changed at all
class critical_data:
    def __init__(self):
        self.reg = []
        self.tainted = False

    def regadd(self, new_reg):
        if new_reg not in self.reg:
            self.reg.append(new_reg)
    
    def __str__(self):
        return f"reg: {self.reg}"


# hidden function that takes a string and returns said string without parentheses or commas
def _clean_str(str):
    lststr = list(str)
    new_lst = []
    for i in range(0, len(lststr)):
        if lststr[i] == ',' or lststr[i] == ')':
            new_lst.append('')
            
        
        elif lststr[i] == '(':
            break

        else:
            new_lst.append(lststr[i])

    return ''.join(new_lst)


# just uses _clean_str over a whole line and returns it
def _clean_line(lst):
    for i in range(0, len(lst)):
        lst[i] = _clean_str(lst[i])
    
    return lst


# takes a file name, iterates through and returns all lines after they have been cleaned of punctuation
def profile(fn):
    lines = []
    line_num = -1
    source_line = -1
    sink_line = -1

    inp = open(fn, "r")
    for line in inp:
        line_num += 1
        line = line.split()
        lines.append(_clean_line(line))
        
        for arg in line:
            if "@SOURCE" in arg and "declare" not in line: # detects only the calls, not the declarations
                source_line = line_num

            elif "@SINK" in arg and "declare" not in line: # what he said
                sink_line = line_num

    inp.close()

    return lines, source_line, sink_line


# the actual analysis engine
# initializes a critical_data object and then looks for how the data changes throughout the program
# the lines that get passed in need to be in order such that control passes through the source and sink (obviously)
# for that we use the path() function found in main
# utilizes flow_instructions.py for changing how the data is being interpreted, the final output of "FLOW" or "NO FLOW" actually comes from flow_instructions.py
# not the most intuitive but whatever :)
def dataflowanalysis(lines):
    cd = critical_data()
    for i in lines:
        if '@SOURCE' in i and i[0] != 'declare':
            finc.SOURCE(i, cd)
        
        elif '@SINK' in i and i[0] != 'declare':
            print(finc.SINK(i, cd))
        
        elif 'store' in i:
            finc.store(i, cd)

        elif 'load' in i:
            finc.load(i, cd)


if __name__ == "__main__":
    lines, src_line, snk_line = profile(sys.argv[1]) # gets the lines from the file
    path_lines = pinc.path(lines) # arranges them so that we get a clear line from start of program to source to sink, lines only change if there are branches and what not
    dataflowanalysis(path_lines) # analyzes the lines and gives output