import json
from lib.util import indent
from typing import Optional, Dict


class AcfFile:
    def __init__(self, file_name: str):
        self.file_name: str = file_name
        self.root: Optional[AcfNode] = None
        self.load()

    def load(self):
        # tokenize
        tokens = []
        single_chars = {'{', '}'}
        with open(self.file_name, 'rb') as f:
            while True:
                c = f.read(1).decode()
                if c == '':
                    break  # EOF
                elif c == '"':  # string
                    current_token = c
                    while True:
                        old_c = c
                        c = f.read(1).decode()
                        if c == '':
                            tokens.append(current_token)
                            break  # EOF
                        elif c == '"' and not old_c == '\\':
                            current_token += c
                            tokens.append(current_token)
                            break
                        current_token += c
                elif c in single_chars:
                    tokens.append(c)
                else:
                    pass  # ignore
        # parse
        token = tokens.pop(0)
        self.root = AcfNode(json.loads(token))
        tokens.pop(0)  # {
        stack = []
        current_node = self.root
        while len(tokens) > 0:
            token = tokens.pop(0)
            if token == '}':
                if len(stack) == 0:
                    break
                current_node = stack.pop()
                continue
            next_token = tokens.pop(0)
            if next_token == '{':
                stack.append(current_node)
                node_name = json.loads(token)
                new_node = AcfNode(node_name)
                current_node.nodes[node_name] = new_node
                current_node = new_node
            else:
                current_node.values[json.loads(token)] = json.loads(next_token)

    def save(self):
        with open(self.file_name, 'wb') as f:
            f.write(str(self.root).encode())


class AcfNode:
    def __init__(self, name: str):
        self.name: str = name
        self.nodes: Dict[str, AcfNode] = dict()
        self.values: Dict[str, str] = dict()

    def __str__(self):
        value = f'{json.dumps(str(self.name))}\n{{\n'
        for k, v in self.values.items():
            value += '\t' + json.dumps(str(k)) + "\t\t" + json.dumps(str(v)) + "\n"
        for k, n in self.nodes.items():
            value += indent(str(n), '\t')
        value += "}\n"
        return value
