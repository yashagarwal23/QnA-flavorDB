package flavordb;

import org.apache.jena.rdf.model.*;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStream;

public class MakeRDFData {
    public static String flavor_db_prefix = "http://cosylab.iiitd.edu.in/flavordb/";
    public static String flavor_db_prop_prefix = flavor_db_prefix + "property#";


    public static void main(String[] args) {
        Model model = ModelFactory.createDefaultModel();
        model.setNsPrefix("prop", flavor_db_prop_prefix);

        // add molecule properties from fdb_molecules.csv
        AddMoleculeToRDFData.getMoleculeModel("data/fdb_molecules.csv", model);

        // add entity properties from fdb_entities.csv
        AddEntitiesToRDFData.getEntityData("data/fdb_entities.csv", model);

        // add entity to model relations
        AddEntityToMoleculesRDFData.getEntityToMoleculeData("data/fdb_molecules_entities.csv", model);

        try {
            OutputStream os1 = new FileOutputStream("flavor-db-rdf-data.rdf");
            model.write(os1);
            OutputStream os2 = new FileOutputStream("flavor-db-rdf-data-triple-format.rdf");
            model.write(os2, "N-TRIPLE");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
