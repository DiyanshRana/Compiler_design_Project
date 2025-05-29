import ast
import json

def classname(cls):
    return cls.__class__.__name__

def jsonify_ast(node, level=0):
    fields = {}
    for k in node._fields:
        v = getattr(node, k, None)
        if isinstance(v, ast.AST):
            fields[k] = jsonify_ast(v)
        elif isinstance(v, list):
            fields[k] = [jsonify_ast(i) if isinstance(i, ast.AST) else str(i) for i in v]
        else:
            fields[k] = v if isinstance(v, (str, int, float, type(None))) else 'unrecognized'
    return {classname(node): fields}

def make_ast(code):
    tree = ast.parse(code)
    return jsonify_ast(tree)
