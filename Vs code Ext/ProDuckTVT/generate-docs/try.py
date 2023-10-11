import ast

def extract_variables(code):
    variables = []
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_name = target.id
                    if hasattr(node, 'value'):
                        variable_value = ast.dump(node.value)
                        variables.append((variable_name, variable_value))
    
    return variables

def extract_functions(code):
    functions = []
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            arguments = [arg.arg for arg in node.args.args]
            functions.append((function_name, arguments))
    
    return functions

def extract_classes(code):
    classes = []
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_members = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append((class_name, class_members))
    
    return classes

def generate_basic_documentation(code):
    variables = extract_variables(code)
    functions = extract_functions(code)
    classes = extract_classes(code)
    
    documentation = []
    
    if variables:
        documentation.append("Variables:")
        for variable, value in variables:
            documentation.append(f"- {variable}: {value}")
    
    if functions:
        documentation.append("Functions:")
        for function, arguments in functions:
            documentation.append(f"- {function}({', '.join(arguments)})")
    
    if classes:
        documentation.append("Classes:")
        for class_name, members in classes:
            documentation.append(f"- {class_name}")
            if members:
                documentation.extend([f"  - {member}" for member in members])
    
    return "\n".join(documentation)

if __name__ == "__main__":
    python_code = """
x = 10
y = 'Hello'

def add(a, b):
    return a + b

class MyClass:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
    """
    
    documentation = generate_basic_documentation(python_code)
    print(documentation)
