import_rules = [
        "%import common.ESCAPED_STRING -> STRING",
        "%import common.WORD",
        "%import common.WS",
        "%ignore WS",
        "%import .tokens.property.PROPERTY",
        "%import .tokens.entity.ENTITY",
]

token_rules = [
    # MOLECULE WORD
    'LCASE_LETTER: "a".."z"',
    'UCASE_LETTER: "A".."Z"',
    'DIGIT: "0".."9"',
    'INT: DIGIT+',
    'MOLECULE_LETTER: UCASE_LETTER | LCASE_LETTER | INT | "(" | ")" | "-" | "]" | "[" | ","',
    'MOLECULE_WORD: MOLECULE_LETTER+',
    'molecule: MOLECULE_WORD+',
    
    # Property
    'property: PROPERTY',

    'entity: WORD+',
    'entity_1: WORD+', 
    'entity_2: WORD+', 
    'category: WORD+', 
    'flavor_profile: WORD+',

    'GET: "get"i',
    'THE: "the"i',
    'MOLECULE: "molecule"i',
    'MOLECULES: "molecules"i',
    'PRESENT: "present"i',
    'IN: "in"i',
    'BOTH: "both"i',
    'AND: "and"i',
    'COMMON: "common"i',
    'WHAT: "what"i',
    'ARE: "are"i',
    'FLAVOR: "flavor"i',
    'FLAVORS: "flavors"i',
    'OF: "of"i',
    'HOW: "how"i',
    'DOES: "does"i',
    'TASTE: "taste"',
    'LIKE: "like"i',
    'DO: "do"i',
    'IS: "is"i',
    'NATURAL: "natural"i',
    'SOURCE: "source"i',
    'SOURCES: "sources"i',
    'FIND: "find"i',
    'ALL: "all"i',
    'ENTITIES: "entities"i',
    'CATEGORY: "category"i',
    'WITH: "with"i',
    'THAT: "that"i',
    'HAVE: "have"i',
    'HAVING: "having"i',
    'WHICH: "which"i',
    'SHOW: "show"i',
    'CONTAIN: "contain"i',
    'CONTAINING: "containing"i',
    ]

templates = [
    {
        "type": "common_molecule_sentence",
        "rules":[
            'GET THE? MOLECULES PRESENT IN BOTH entity_1 AND entity_2',
            'GET THE? COMMON MOLECULES IN entity_1 AND entity_2',
            'COMMON MOLECULES IN entity_1 AND entity_2',
            'WHAT ARE THE MOLECULES PRESENT IN BOTH entity_1 AND entity_2',
            'FIND THE MOLECULES PRESENT IN BOTH entity_1 AND entity_2',
        ],
        "query":
            """
                PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

                SELECT DISTINCT ?molecule_name
                WHERE {{ 
                    ?entity1 prop:entity_name "{entity_1}" .
                    ?entity2 prop:entity_name "{entity_2}" .
                    ?entity1 prop:contains ?molecule .
                    ?entity2 prop:contains ?molecule .
                    ?molecule prop:iupac_name ?molecule_name .
                }}
            """
    },
    {
        "type": "flavor_profile_entity_sentence",
        "rules":[
            'GET THE? FLAVORS OF entity',
            '(HOW | WHAT) DOES entity TASTE LIKE?',
            '(HOW | WHAT) DO entity TASTE LIKE?',
            'FLAVORS OF entity',
        ],
        "query":
            """
                PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

                SELECT DISTINCT ?flavor
                WHERE {{
                    ?entity prop:entity_name "{entity}" .
                    ?entity prop:contains ?molecule .
                    ?molecule prop:flavor_profile ?flavor .
                }}
            """
    },
    {
        "type": "molecules_in_entity_sentence",
        "rules": [
            'WHAT ARE THE FLAVOR? MOLECULES PRESENT IN entity',
            'GET THE FLAVOR? MOLECULES PRESENT? IN entity',
            'FLAVOR? MOLECULES PRESENT? IN entity',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

            SELECT DISTINCT ?molecule_name
            WHERE {{
                ?entity prop:entity_name "{entity}" .
                ?entity prop:contains ?molecule .
                ?molecule prop:iupac_name ?molecule_name .
            }}
        """
    },
    {
        "type": "entity_that_contain_molecules_sentence",
        "rules": [
            '(GET | FIND | SHOW | WHAT ARE) THE ENTITIES THAT CONTAIN THE? MOLECULE? molecule',
            '(GET | FIND | SHOW | WHAT ARE) THE ENTITIES CONTAINING THE? MOLECULE? molecule',
            'ENTITIES THAT CONTAIN THE? MOLECULE? molecule',
            'ENTITIES CONTAINING THE? MOLECULE? molecule',
        ],
        "query":
        """

        """
    },
    {
        "type": "natural_source_of_entity_sentence",
        "rules": [
            'WHAT IS THE NATURAL SOURCE OF entity',
            'GET THE NATURAL SOURCE OF entity',
            'NATURAL SOURCE OF entity',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>
            SELECT DISTINCT ?natural_source
            WHERE {{
                ?entity prop:entity_name "{entity}" .
                ?entity prop:natural_source ?natural_source .
            }}
        """
    },
    {
        "type": "natural_source_of_molecule_sentence",
        "rules": [
            '(WHAT ARE | FIND | GET | SHOW) THE NATURAL (SOURCES | SOURCE) OF molecule',
            'NATURAL SOURCES OF molecule',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>
            SELECT DISTINCT ?natural_source
            WHERE {{
                    ?molecule prop:iupac_name "{molecule}" .
                    ?entity prop:contains ?molecule .
                    ?entity prop:natural_source ?natural_source .
                }}
        """
    },
    {
        "type": "entities_of_category_sentence",
        "rules": [
            'GET ALL? THE ENTITIES OF CATEGORY? category',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>
            SELECT DISTINCT ?entity
            WHERE {{
                ?entity_id prop:category "{category}" .
                ?entity_id prop:entity_name ?entity .
            }}
        """
    }, 
    {
        "type": "molecules_with_flavor_profile_sentence",
        "rules":[
            'GET THE MOLECULES (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
            'WHAT ARE THE MOLECULES (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>
            SELECT DISTINCT ?molecule_name
            WHERE {{
                ?molecule_id prop:flavor_profile "{flavor_profile}" .
                ?molecule_id prop:iupac_name ?molecule_name .
            }}
        """
    },
    {
        "type": "entities_with_flavor_profile_sentence",
        "rules":[
            'GET THE? ENTITIES (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
            'WHAT ARE THE ENTITIES (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>
            SELECT DISTINCT ?entity_name
            WHERE {{
                ?molecule_id prop:flavor_profile "{flavor_profile}" .
                ?entity_id prop:contains ?molecule_id .
                ?entity_id prop:entity_name ?entity_name .
            }}
        """
    },
    {
        "type": "molecule_in_entity_with_flavor_profile_sentence",
        "rules": [
            'GET THE MOLECULES IN entity (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
            'SHOW THE MOLECULES IN entity (WITH | THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
            'WHICH FLAVOR? MOLECULES IN entity HAVE flavor_profile (FLAVOR | TASTE)',
            'FLAVOR? MOLECULES IN entity (THAT HAVE | HAVING) flavor_profile (FLAVOR | TASTE)',
        ],
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

            SELECT DISTINCT ?molecule_name 
            WHERE {{
                ?entity prop:entity_name "{entity}" .
                ?entity prop:contains ?molecule .
                ?molecule prop:flavor_profile "{flavor_profile}" .
                ?molecule prop:iupac_name ?molecule_name
            }}
        """
    },
    {
        "type": "property_of_entity_sentence",
        "rules": [
            'GET THE? property OF entity',
            'WHAT IS THE? property OF entity',
            'property OF entity',
        ], 
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

            SELECT ?{property}
            WHERE {{
                ?entity prop:entity_name "{entity}" .
                ?entity prop:{property} ?{property} .
            }}
        """
    },
    {
        "type": "property_of_molecule_sentence",
        "rules": [
            'GET THE? property OF molecule',
            'WHAT IS THE? property OF molecule',
            'property OF molecule',
        ], 
        "query":
        """
            PREFIX prop: <http://cosylab.iiitd.edu.in/flavordb/property#>

            SELECT ?{property}
            WHERE {{
                ?molecule prop:iupac_name "{molecule}" .
                ?molecule prop:{property} ?{property} .
            }}
        """
    },
]