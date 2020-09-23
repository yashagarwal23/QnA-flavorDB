package flavordb;

import org.apache.jena.rdf.model.*;

import java.util.List;

import static flavordb.AddEntitiesToRDFData.entity_prefix;
import static flavordb.AddMoleculeToRDFData.molecule_prefix;
import static flavordb.MakeRDFData.flavor_db_prop_prefix;

public class AddEntityToMoleculesRDFData {

    public static void getEntityToMoleculeData(String filepath, Model model) {
        List<String[]> entitiesToMolecules = Utils.readCSV(filepath);
        if(entitiesToMolecules == null)
            return;

        Property containsProp = model.createProperty(flavor_db_prop_prefix + "contains");
        for(int i = 1; i < entitiesToMolecules.size(); ++i) {
            String pubchem_id = entitiesToMolecules.get(i)[1];
            String entity_id = entitiesToMolecules.get(i)[2];
            Resource molecule = model.getResource(molecule_prefix + pubchem_id);
            Resource entity = model.getResource(entity_prefix + entity_id);
            model.add(entity, containsProp, molecule);
        }
    }
}
