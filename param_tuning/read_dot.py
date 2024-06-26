import re

class Node:
    def __init__(self, id, label, params):
        self.id = id
        self.label = label
        self.params = params

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label}, params={self.params})"

def parse_dot(dot_content):
    node_pattern = re.compile(r'(\w+) \[label="([\w]+)(?:\\n([\w]+=([\w\d]+))\\n([\w]+=([\w\d]+))\\n([\w]+=([\w\d]+)))?"\];')
    edge_pattern = re.compile(r'(\w+) -> (\w+) \[\];')

    nodes = {}
    edges = []

    for line in dot_content.splitlines():
        node_match = node_pattern.match(line)
        if node_match:
            node_id = node_match.group(1)
            label = node_match.group(2)
            params = {
                node_match.group(3): node_match.group(4),
                node_match.group(5): node_match.group(6),
                node_match.group(7): node_match.group(8)
            } if node_match.group(3) else {}
            nodes[node_id] = Node(node_id, label, params)
        else:
            edge_match = edge_pattern.match(line)
            if edge_match:
                source = edge_match.group(1)
                target = edge_match.group(2)
                edges.append((source, target))

    return nodes, edges

def read_dot_file(file_path):
    with open(file_path, 'r') as file:
        dot_content = file.read()
    return dot_content