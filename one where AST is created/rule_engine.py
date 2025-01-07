

import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Reference to left child (Node)
        self.right = right     # Reference to right child (Node)
        self.value = value     # Optional value for operand nodes

def create_rule(rule_string):
    pattern = r'(\w+)\s*([<>=!]+)\s*(\d+|\'.*?\')'
    matches = re.findall(pattern, rule_string)

    if not matches:
        raise ValueError("Invalid rule string")

    conditions = []
    for match in matches:
        attribute, operator, value = match
        operand_node = Node("operand", value=value.strip("'"))
        operator_node = Node("operator", left=operand_node, value=operator)
        conditions.append(operator_node)

    root = conditions[0]
    current = root
    for condition in conditions[1:]:
        and_node = Node("operator", left=current, right=condition, value="AND")
        current = and_node

    return current

def evaluate_ast(node, data):
    if node is None:
        return False  # Handle None case

    if node.type == "operand":
        # Return the value of the operand from data
        return int(node.value) if node.value.isdigit() else data[node.value]
    elif node.type == "operator":
        left_value = evaluate_ast(node.left, data)
        right_value = evaluate_ast(node.right, data)

        if node.value == '>':
            return left_value > right_value
        elif node.value == '<':
            return left_value < right_value
        elif node.value == '=':
            return left_value == right_value
        elif node.value == 'AND':
            return left_value and right_value
        # Add more operators as needed

def print_ast(node, level=0):
    if node:
        print(" " * (level * 4) + f"{node.type}: {node.value if node.value else ''}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)

# Test the function with a sample rule string
rule_string = "age > 30 AND salary > 50000"
ast = create_rule(rule_string)
print_ast(ast)

# Sample data for evaluation
sample_data = {
    "age": 35,
    "salary": 60000
}

# Evaluate the rule against the sample data
result = evaluate_ast(ast, sample_data)
print(f"Rule Evaluation Result: {result}")


import unittest

class TestRuleEngine(unittest.TestCase):
    def test_simple_rule(self):
        rule_string = "age > 30"
        sample_data = {"age": 35}
        ast = create_rule(rule_string)
        result = evaluate_ast(ast, sample_data)
        self.assertTrue(result)

    def test_multiple_conditions(self):
        rule_string = "age > 30 AND salary > 50000"
        sample_data = {"age": 35, "salary": 60000}
        ast = create_rule(rule_string)
        result = evaluate_ast(ast, sample_data)
        self.assertTrue(result)

    def test_invalid_rule(self):
        rule_string = "age > thirty"
        sample_data = {"age": 35}
        with self.assertRaises(ValueError):
            create_rule(rule_string)

    def test_empty_rule(self):
        rule_string = ""
        sample_data = {"age": 35}
        with self.assertRaises(ValueError):
            create_rule(rule_string)

if __name__ == "__main__":
    unittest.main()

