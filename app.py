from flask import Flask, request, jsonify
from rule_engine import create_rule, combine_rules, evaluate_rule, Node

app = Flask(__name__)

rules = []


@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get('rule')
    rule = create_rule(rule_string)
    rules.append(rule)
    return jsonify({'message': 'Rule created', 'rule': str(rule)})


@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    combined_rule = combine_rules(rules)
    return jsonify({'message': 'Rules combined', 'combined_rule': str(combined_rule)})


@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    user_data = request.json
    combined_rule = combine_rules(rules)
    result = evaluate_rule(combined_rule, user_data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
