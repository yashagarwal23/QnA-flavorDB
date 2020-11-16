from rules import templates, token_rules, import_rules
import requests
import urllib

requests.adapters.DEFAULT_RETRIES = 3

sparql_url = "http://139.59.7.50:7200/repositories/c2c2f5c2a0c2h7h7i8b1"

start_token = "start"

# add optional EOS at the end of sentences
sentence_names = [template["type"] + " EOS?" for template in templates]

def get_grammar():
    token_rules.extend([
        'EOS: "." | "?" '
    ])

    grammar_rules = []
    grammar_rules.extend(token_rules)
    
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
                grammar_rules.append(template["type"] + f": {rule}")
            else:
                grammar_rules.append(" "*len(template["type"]) + f"| {rule}")

    grammar_rules.append("\n")
    grammar_rules.extend(import_rules)
    

    return "\n".join(grammar_rules)


def query_map():
    query_dict = dict()
    for template in templates:
        if "query" in template:
            query_dict[template["type"]] = template["query"]
    return query_dict


def get_query_result(query):
    params = {"query": query}
    sparql_query_url = sparql_url + "?" + urllib.parse.urlencode(params)
    response = requests.get(url = sparql_query_url)
    return response.content

def parse_query_result(raw_query_result):
    rows = raw_query_result.decode("utf-8").split("\n")
    result = []
    for row in rows[:-1]:
        row_elements = []
        prev_str = ""
        inside_quotes = False
        for i in range(len(row)):
            if row[i] == '\r':
                row_elements.append(prev_str)
                break
            if row[i] == ',':
                if inside_quotes:
                    prev_str += ','
                else:
                    row_elements.append(prev_str)
                    prev_str = ""
            elif row[i] == '"':
                inside_quotes = not inside_quotes
            else:
                prev_str += row[i]
        result.append(row_elements)
    return result
