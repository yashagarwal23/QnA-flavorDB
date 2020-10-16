from templates import tokens, templates

start_token = "start"
sentence_names = [template["name"] for template in templates]

import_rules = [
    "%import common.ESCAPED_STRING -> STRING",
    "%import common.WORD",
    "%import common.WS",
    "%ignore WS"
]

def get_grammar():
    grammar_rules = []
    grammar_rules.append("\n")
    for token in tokens:
        grammar_rules.append(f"{token}: WORD")
    
    if len(sentence_names) > 0:
        sentence_names_string = " | ".join(sentence_names)
        start_rule = f"{start_token}: {sentence_names_string}"
        grammar_rules.append("\n")
        grammar_rules.append(start_rule)

    for template in templates:
        sentence_rules = template["rules"]
        grammar_rules.append("\n")
        for i, rule in enumerate(sentence_rules):
            if i == 0:
                grammar_rules.append(template["name"] + f": {rule}")
            else:
                grammar_rules.append(" "*len(template["name"]) + f"| {rule}")

    grammar_rules.append("\n")
    grammar_rules.extend(import_rules)

    return "\n".join(grammar_rules)