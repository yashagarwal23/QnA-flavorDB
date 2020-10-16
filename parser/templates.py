tokens = ['MOLECULE', 'PROPERTY', 'ENTITY', 'ENTITY_1', 'ENTITY_2']

templates = [
    {
        "name": "common_molecule_sentence",
        "rules":[
            '"get"i "the"i? "molecules"i "present"i? "in"i "both" ENTITY_1 "and"i ENTITY_2',
            '"get"i "the"? "common"i "molecules"i "in"i ENTITY_1 "and"i ENTITY_2', 
            '"common"i "molecules"i "in"i ENTITY_1 "and"i ENTITY_2',
            '"what"i "are"i "the"i "molecules"i "present"i "in"i "both"i ENTITY_1 "and"i ENTITY_2',
            '"find"i "the"i "molecules"i "present"i? "in"i ENTITY_1 "and"i ENTITY_2'
        ]
    },
    {
        "name": "flavor_profile_entity_sentence",
        "rules":[
            '"get"i "the"i? "flavors"i "of"i ENTITY'
        ]
    },
    {
        "name": "molecules_in_entity_sentence",
        "rules": [
            '"what"i "are"i "the"i "molecules"i "present"i? "in"i ENTITY',
            '"get"i "the"i? "molecules"i "present"i? "in"i ENTITY'
        ]
    },
    {
        "name": "property_of_molecule_sentence",
        "rules": [
            '"get"i "the"i PROPERTY "of"i MOLECULE',
            '"what"i "is"i "the"i PROPERTY "of"i MOLECULE'
        ]
    },
    {
        "name": "property_of_entity_sentence",
        "rules": [
            '"get"i "the"i PROPERTY "of"i ENTITY',
            '"what"i "is"i "the"i PROPERTY "of"i ENTITY'
        ]
    }
]