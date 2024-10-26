from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

# Node class definition for AST
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

# Helper function to convert Node to a JSON-serializable dictionary
def node_to_dict(node):
    if node is None:
        return None
    return {
        "type": node.type,
        "value": node.value,
        "left": node_to_dict(node.left),
        "right": node_to_dict(node.right)
    }

# Function to create an AST from a rule string (Placeholder - implement logic here)
def create_rule(rule_string):
    # Example AST structure for testing
    # Replace this with the logic to parse the rule string and create the AST
    root = Node("operator", value="AND")
    root.left = Node("operand", value="age > 30")
    root.right = Node("operator", value="OR")
    root.right.left = Node("operand", value="salary > 20000")
    root.right.right = Node("operand", value="experience > 5")
    return root

# Function to save rule to database and return the rule ID
def save_rule(rule_string, rule_ast):
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Rules 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, rule_string TEXT, rule_ast TEXT)''')
    
    # Store the rule AST as a JSON string
    c.execute("INSERT INTO Rules (rule_string, rule_ast) VALUES (?, ?)", (rule_string, json.dumps(rule_ast)))
    rule_id = c.lastrowid  # Get the ID of the newly inserted row
    
    conn.commit()
    conn.close()
    
    print(f"Debug: Rule saved with ID = {rule_id}")  # Debug output to confirm rule_id is set
    return rule_id

# Function to evaluate a rule against provided data
def evaluate_rule(ast, data):
    if ast.type == "operand":
        # Evaluate comparison
        print(f"Evaluating operand: {ast.value} with data: {data}")
        return eval(ast.value, {}, data)
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        print(f"Evaluating operator: {ast.value}, left result: {left_result}, right result: {right_result}")
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result

# Function to convert dictionary back to Node structure
def dict_to_node(node_dict):
    if node_dict is None:
        return None
    left_node = dict_to_node(node_dict['left'])
    right_node = dict_to_node(node_dict['right'])
    return Node(node_dict['type'], node_dict.get('value'), left_node, right_node)

# Endpoint to create a new rule
@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule_string')
    ast = create_rule(rule_string)
    
    # Convert the AST Node to a serializable dictionary
    ast_dict = node_to_dict(ast)
    
    # Save the rule and get the rule ID
    rule_id = save_rule(rule_string, ast_dict)
    
    print(f"Debug: Responding with rule_id = {rule_id}")  # Debug output to confirm response
    
    return jsonify({"message": "Rule created", "rule_id": rule_id, "rule_ast": ast_dict})

# Endpoint to evaluate a rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')
    
    # Fetch the rule from the database using rule_id
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute("SELECT rule_ast FROM Rules WHERE id = ?", (rule_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        rule_ast = json.loads(result[0])  # Load the AST from JSON
        ast = dict_to_node(rule_ast)  # Convert back to Node structure
        
        # Evaluate the rule
        evaluation_result = evaluate_rule(ast, data)
        return jsonify({"rule_id": rule_id, "result": evaluation_result})
    
    return jsonify({"error": "Rule not found"}), 404

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
