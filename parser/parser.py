from lark import Lark
from make_grammar import get_grammar, start_token

grammar = """
    ENTITY_1: WORD
    ENTITY_2: WORD

    start: sentence_1
    sentence_1: "find"i "the"i "molecules"i "present"i? "in"i ENTITY_1 "and"i ENTITY_2

    %import common.ESCAPED_STRING -> STRING
    %import common.WORD
    %import common.WS
    %ignore WS
"""

grammar = get_grammar()

parser = Lark(grammar, start=start_token, ambiguity='explicit')

sentence = "find the molecules in milk and apple"

def parse_tree(tree):
    details = dict();
    for node in tree.iter_subtrees():
        if node.data != start_token:
            details["type"] = node.data
            for child in node.children:
                details[child.type] = child.value
    return details

if __name__ == '__main__':
    tree = parser.parse(sentence)
    print(parse_tree(tree))