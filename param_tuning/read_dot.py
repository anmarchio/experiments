import re


class Node:
    def __init__(self, id, label, params):
        self.id = id
        self.label = label
        self.params = params

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label}, params={self.params})"


def parse_dot(dot_content):
    # Split the input string based on ';' and strip whitespace
    segments = [segment.strip() for segment in dot_content.split(';') if segment.strip()]
    segments.reverse()

    result_dict = {
        'path': '',
        'datetime': '',
        'pipeline': {}
    }

    for segment in segments:
        match = re.match(r'(\S+)\s+\[label="(.+?)"\]', segment)
        if match:
            node_id, label = match.groups()
            if 'HalconInputNode' in label:
                # result_dict['ignore'] = label
                pass
            else:
                parts = label.split('\\n')
                key = parts[0]
                values = {}
                for part in parts[1:]:
                    param, value = part.split('=')
                    values[param.strip()] = value.strip()
                result_dict['pipeline'][key] = values

    return result_dict
