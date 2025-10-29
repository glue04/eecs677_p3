import graph_real_real as grr

class Node:
    def __init__(self, label, nexts):
        self.label = label
        self.next = nexts
    
    def __str__(self):
        return f"label: {self.label} | next: {self.next}"
    
    def __repr__(self):
        return f"label: {self.label} | next: {self.next}"


def _locate_source_label(lines): # returns index of the line with the source
    src_line = -1
    for i in range(0, len(lines)):
        if "@SOURCE(" in lines[i] and "declare" not in lines[i]:
            src_line = i
    
    for i in reversed(range(0, src_line + 1)):
        for j in lines[i]:
            if ":" in j:
                label = lines[i][0]
                return i, label[:len(lines[i][0]) - 1]
        
    else:
        return -1, ""


def _locate_sink_label(lines): # returns index of the line with the source
    snk_line = -1
    for i in range(0, len(lines)):
        if "@SINK(i32" in lines[i] and "declare" not in lines[i]:
            snk_line = i
    
    for i in reversed(range(0, snk_line + 1)):
        for j in lines[i]:
            if ":" in j:
                label = lines[i][0]
                return i, label[:len(lines[i][0]) - 1]
    else:
        return -1, ""


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

def _index_label(lines, label):
    label = label + ':'
    for i in range(0, len(lines)):
        if label in lines[i]:
            return i


def path(lines): # return path from start of code, to the source, to the sink. returns a list of lines in path order
    
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

        if "@SINK(i32" in lines[c]:
            return new_lines

        if "br" in lines[c]:
            label_counter += 1
            c = _index_label(lines, node_path[label_counter].label)

        c = c + 1

    return new_lines



            



if __name__ == "__main__":
    lines, src_line, snk_line = grr.profile("ex3.ll")
    print(path(lines))

