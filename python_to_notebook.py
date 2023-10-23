import jinja2
import nbformat
from nbformat.v4 import new_code_cell

# Create a Jupyter Notebook
notebook = nbformat.v4.new_notebook()

# Load your Jinja2 template
with open("jinja_template.json", "r") as template_file:
    jinja_template = template_file.read()
template = jinja2.Template(jinja_template)

# Read the content of the brain.py file and extract code from train_model()
with open("brain.py", "r") as python_file:
    python_code = ""
    inside_function = False
    function_indent = None

    for line in python_file:
        if inside_function:
            # Check for indentation level
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= function_indent:
                break  # Stop when the indentation level decreases
            python_code += line
        if not inside_function and line.strip().startswith("def"):
            inside_function = True
            function_indent = len(line) - len(line.lstrip())
            python_code = line
            
    # Add a code cell with the extracted Python code
    code_cell = new_code_cell(python_code)
    notebook.cells.append(code_cell)

# Save the notebook to a .ipynb file
with open("output_notebook.ipynb", "w") as f:
    nbformat.write(notebook, f)
