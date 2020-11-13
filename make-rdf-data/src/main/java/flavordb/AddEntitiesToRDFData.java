package flavordb;

import org.apache.jena.ontology.Individual;
import org.apache.jena.ontology.OntModel;
import org.apache.jena.rdf.model.*;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import static flavordb.MakeRDFData.flavor_db_prefix;
import static flavordb.MakeRDFData.flavor_db_prop_prefix;

public class AddEntitiesToRDFData {

    public static String entity_prefix = flavor_db_prefix + "entity#";

    // column idx of properties to be added
    static List<String> props_taken = new ArrayList<>(Arrays.asList("entity_id", "category", "natural_source_name", "entity_alias_readable"));
    static List<String> props_name = new ArrayList<>(Arrays.asList("entity_id", "category", "natural_source", "entity_name"));

    public static void getEntityData(String filepath, OntModel model) {
        List<String[]> entities = Utils.readCSV(filepath);
        if(entities == null)
            return;

        List<String> entity_heads = Arrays.asList(entities.get(0));
        HashMap<String, Property> props_map = new HashMap<>();
        HashMap<String, Integer> props_taken_idx = new HashMap<>();

        for(int i = 0; i < props_taken.size(); i++) {
            props_map.put(props_taken.get(i), model.createDatatypeProperty(flavor_db_prop_prefix + props_name.get(i)));
            props_taken_idx.put(props_taken.get(i), entity_heads.indexOf(props_taken.get(i)));
        }

        model.setNsPrefix("entity", entity_prefix);

        for (int i = 1; i < entities.size(); ++i) {
            try {
                AddEntity(entities.get(i), props_map, props_taken_idx, model);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
    }

    private static void AddEntity(String[] entity, HashMap<String, Property> props_map, HashMap<String, Integer> props_taken_idx, OntModel model) throws UnsupportedEncodingException {
        String entity_id =  entity[0];
        Individual entity_individual = model.createIndividual(entity_prefix + entity_id, model.createResource(flavor_db_prefix + "Entity"));

        // add entity id
        if(props_map.containsKey("entity_id")) {
            entity_individual.addProperty(props_map.get("entity_id"), entity[props_taken_idx.get("entity_id")]);
        }

        // add category
        if (props_map.containsKey("category")) {
            entity_individual.addProperty(props_map.get("category"), entity[props_taken_idx.get("category")]);
        }

        // add natural source
        if(props_map.containsKey("natural_source_name")) {
            String natural_source = entity[props_taken_idx.get("natural_source_name")].toLowerCase();
            if(natural_source.length() > 0) {
                entity_individual.addProperty(props_map.get("natural_source_name"), natural_source);
            }
        }

        // add entity alias
        if(props_map.containsKey("entity_alias_readable")) {
            String entity_name = entity[props_taken_idx.get("entity_alias_readable")].toLowerCase();
            entity_individual.addProperty(props_map.get("entity_alias_readable"), entity_name);
        }
    }
}
