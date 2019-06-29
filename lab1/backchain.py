from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def iterate_node(rules, node, mapping):
    if isinstance(node, str):
        leaf = populate(node, mapping)
        return backchain_to_goal_tree(rules, leaf)
    elif isinstance(node, OR):
        return(OR([iterate_node(rules, exp, mapping) for exp in node]))
    elif isinstance(node, AND):
        return(AND([iterate_node(rules, exp, mapping) for exp in node]))

def backchain_to_goal_tree(rules, hypothesis):
    result = []
    for rule in rules:
        matched = match(rule.consequent()[0], hypothesis)
        if matched != None:
            antecedent = rule.antecedent()
            result.append(iterate_node(rules, antecedent, matched))
    if len(result) > 0:
        return simplify(OR(hypothesis, OR(result)))
    else:
        return hypothesis

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
