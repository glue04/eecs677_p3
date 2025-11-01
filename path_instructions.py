# this whole file is a mess, i know, but it works and that is what matters

# node class for dfs search
class Node:
    def __init__(self, label, nexts):
        self.label = label
        self.next = nexts
    
    def __str__(self):
        return f"label: {self.label} | next: {self.next}"
    
    def __repr__(self):
        return f"label: {self.label} | next: {self.next}"

# returns index of the line with the source
def _locate_source_label(lines): 
    src_line = -1
    for i in range(0, len(lines)):
        if "@SOURCE" in lines[i] and "declare" not in lines[i]:
            src_line = i
    
    for i in reversed(range(0, src_line + 1)):
        for j in lines[i]:
            if ":" in j:
                label = lines[i][0]
                return i, label[:len(lines[i][0]) - 1]
        
    else:
        return -1, ""


# returns index of the line with the sink (exactly the same as above but its @SINK instead of @SOURCE im so smart)
def _locate_sink_label(lines): 
    snk_line = -1
    for i in range(0, len(lines)):
        if "@SINK" in lines[i] and "declare" not in lines[i]:
            snk_line = i
    
    for i in reversed(range(0, snk_line + 1)):
        for j in lines[i]:
            if ":" in j:
                label = lines[i][0]
                return i, label[:len(lines[i][0]) - 1]
    else:
        return -1, ""


# finds and returns the indices of all br or ret instructions, as well as the names of all of the different labels in the program
def _find_branches(lines):
    br_indices = []
    br_labels = ['initial']
    for i in range(0, len(lines)): # iterates through all lines
        if 'br' in lines[i] or 'ret' in lines[i]: # if br or ret is in line:
            br_indices.append(i)
    

    for line in lines:
        for arg in line:
            if ':' in arg:
                br_labels.append(arg[:len(arg) - 1])

                
    return br_indices, br_labels


# i hate this one
# depth first search takes the nodes, initial node, source node and sink node and finds a path from intial to source to sink
# this gives a normalized path so that the analysis can just iterate through all of the lines along said path
def _find_path_between_nodes(nodes, initial_node, source_node, sink_node):
    label_to_node = {node.label: node for node in nodes}

    def dfs_path(start_label, goal_label, visited=None):
        if visited is None:
            visited = set()
        if start_label == goal_label:
            return [label_to_node[start_label]]
        
        visited.add(start_label)
        node = label_to_node.get(start_label)
        if not node:
            return None

        for nxt_label in node.next:
            if nxt_label not in visited:
                subpath = dfs_path(nxt_label, goal_label, visited)
                if subpath:
                    return [node] + subpath
        return None


    path1 = dfs_path(initial_node.label, source_node.label)

    path2 = dfs_path(source_node.label, sink_node.label)

    if path1 and path2:
        full_path = path1 + path2[1:]
    else:
        full_path = None

    return full_path


# simple helper function that merely returns the index of a given label :3
def _index_label(lines, label):
    label = label + ':'
    for i in range(0, len(lines)):
        if label in lines[i]:
            return i

# return path from start of code, to the source, to the sink. returns a list of lines in path order
# 
# wrote the above comment while coding it instead of the day after like this one, you can tell i was pissed off lol
# basically takes all of the lines in the program, finds all of the branches and labels and what not
# then it nodifys the initial, source, and sink blocks, finds a path between them (starting at the first line in the program and ending at the sink)
# then puts all of the lines in order according to the node path so that the analysis works
# definitely not the intended solution but again, it works
# I realize that im doing a terrible job of explaining so ill put an example here of what it does
# 
# INPUT LINES
'''
define i32 @main() {
  %aVar = alloca i32
  store i32 0, ptr %aVar
  %a1 = load i32, ptr %aVar
  %ifTruth = icmp ne i32 %a1, 0
  br i1 %ifTruth, label %ifBody, label %afterIf

ifBody:
  %secret = call i32 (...) @SOURCE()
  store i32 %secret, ptr %aVar
  br label %afterIf

afterIf:
  %a2 = load i32, ptr %aVar
  call void @SINK(i32 %a2)
  ret i32 0
}

declare i32 @SOURCE(...)
declare void @SINK(i32)
'''
# OUTPUT LINES 
'''
define i32 @main() {
  %aVar = alloca i32
  store i32 0, ptr %aVar
  %a1 = load i32, ptr %aVar
  %ifTruth = icmp ne i32 %a1, 0
  br i1 %ifTruth, label %ifBody, label %afterIf
  %secret = call i32 (...) @SOURCE()
  store i32 %secret, ptr %aVar
  br label %afterIf
  %a2 = load i32, ptr %aVar
  call void @SINK(i32 %a2)
'''
##############################
def path(lines): 
    
    new_lines = []
    source_label_index, source_label = _locate_source_label(lines)
    sink_label_index, sink_label = _locate_sink_label(lines)

    nodes = []
    br_indices, br_labels = _find_branches(lines)

    c = 0
    for i in br_indices:
        nexts = []
        for j in range(0, len(lines[i])):
            if lines[i][j] == 'label':
                nexts.append(lines[i][j + 1][1:len(lines[i][j + 1])])
        
        nodes.append(Node(br_labels[c], nexts))
        c += 1

    if len(nodes) > 1:
        for i in nodes:
            if i.label == 'initial':
                initial_node = i
            
            elif i.label == sink_label:
                sink_node = i
            
            elif i.label == source_label:
                source_node = i
    
        if initial_node != None and sink_node != None and source_node != None:
            node_path = _find_path_between_nodes(nodes, initial_node, source_node, sink_node)

    else:
        node_path = None

    # finally (jesus christ this took too long) iterate through lines in path order

    c = 0
    label_counter = 0

    while True: # this is terrible but hear me out
        new_lines.append(lines[c])

        if "@SINK" in lines[c]:
            return new_lines

        if "br" in lines[c]:
            label_counter += 1
            c = _index_label(lines, node_path[label_counter].label)

        c = c + 1