import os
import pickle
import sys

import lark
import requests
from flask import Flask, flash, redirect, request, url_for
from flask.templating import render_template
from lark import Lark
from wtforms import Form, TextField, validators
from wtforms.fields.simple import SubmitField

from utils import get_grammar, get_query_result, query_map, start_token, parse_query_result


sys.setrecursionlimit(100000)

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
app.config['SECRET_KEY'] = '684035ef8a43449f96f53def992fb08529667031ffbd4ada74f804b7ef0e9428'

grammar = get_grammar()
type_to_query = query_map()

entity_set = set(pickle.load(open(os.path.join("tokens", "entity.pkl"), "rb")))
molecule_set = set(pickle.load(open(os.path.join("tokens", "molecule.pkl"), "rb")))

parser = Lark(grammar, start=start_token, ambiguity='explicit')
# parser = Lark(grammar, start=start_token)

def check_tree(tree_details):
    for key, value in tree_details.items():
        if key == "molecule" and value not in molecule_set:
            return False
        elif (key == "entity" or key == "entity_1" or key == "entity_2") and value not in entity_set:
            return False
    return True

def get_correct_tree(tree):
    subtrees = [child for child in tree.children]
    for subtree in subtrees:
        tree_details = parse_tree(subtree)
        if check_tree(tree_details):
            return subtree
    return None

def parse_tree(tree):
    if tree.data == "_ambig":
        tree = get_correct_tree(tree)
    if tree is None:
        return dict()
    subtrees = [child for child in tree.iter_subtrees()]
    details = dict()
    for subtree in subtrees[:-2]:
        token_words = []
        for child in subtree.children:
            token_words.append(child.value)
        details[subtree.data] = " ".join(token_words)
    details["type"] = subtrees[-2].data
    return details

class QueryForm(Form):
    nl_query = TextField("Query", validators=[validators.DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = QueryForm()
        return render_template("index.html", form=QueryForm(), results=None)
    else:
        form = QueryForm(request.form)
        if form.validate():
            nl_query = request.form["nl_query"]

            try:
                # parse query
                tree = parser.parse(nl_query)
                # print("-"*80)
                # print(tree)
                # print(tree.pretty())

                # parse AST
                details = parse_tree(tree)
                # print("-"*80)
                # print(details)
                # print("-"*80)

                # pre process property
                if "property" in details:
                    details["property"] = details["property"].replace(' ', '_')

                # get corresponding sparql query
                query = type_to_query[details["type"]].format(**details)
                # get sparql query result
                raw_query_result = get_query_result(query)
                # process raw query
                results = parse_query_result(raw_query_result)
                
                return render_template("index.html", form=QueryForm(), results = results)

            except requests.exceptions.ConnectionError:
                flash('Sparql server down, try again later')
                return redirect(url_for("index"))
            
            except lark.exceptions.UnexpectedCharacters:
                flash("Sorry!!! Query not supported yet")
                return redirect(url_for("index"))
                
        else:
            flash('Query is required')

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')