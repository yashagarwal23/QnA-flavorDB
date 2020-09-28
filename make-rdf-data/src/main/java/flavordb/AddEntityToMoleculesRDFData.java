package flavordb;

import org.apache.jena.ontology.ObjectProperty;
import org.apache.jena.ontology.OntClass;
import org.apache.jena.ontology.OntModel;
import org.apache.jena.rdf.model.*;

import java.util.List;

import static flavordb.AddEntitiesToRDFData.entity_prefix;
import static flavordb.AddMoleculeToRDFData.molecule_prefix;
import static flavordb.MakeRDFData.flavor_db_prop_prefix;

public class AddEntityToMoleculesRDFData {

    public static void getEntityToMoleculeData(String filepath, OntModel model, OntClass moleculeClass, OntClass entityClass) {
        List<String[]> entitiesToMolecules = Utils.readCSV(filepath);
        if(entitiesToMolecules == null)
            return;

        ObjectProperty containsProp = model.createObjectProperty(flavor_db_prop_prefix + "contains");
        containsProp.addDomain(entityClass);
        containsProp.addRange(moleculeClass);
        for(int i = 1; i < entitiesToMolecules.size(); ++i) {
            String pubchem_id = entitiesToMolecules.get(i)[1];
            String entity_id = entitiesToMolecules.get(i)[2];
            Resource molecule = model.getIndividual(molecule_prefix + pubchem_id);
            Resource entity = model.getIndividual(entity_prefix + entity_id);
            entity.addProperty(containsProp, molecule);
        }
    }
}
