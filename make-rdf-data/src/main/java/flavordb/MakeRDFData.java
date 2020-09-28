package flavordb;

import org.apache.jena.ontology.OntClass;
import org.apache.jena.ontology.OntModel;
import org.apache.jena.rdf.model.*;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStream;

public class MakeRDFData {
    public static String flavor_db_prefix = "http://cosylab.iiitd.edu.in/flavordb/";
    public static String flavor_db_prop_prefix = flavor_db_prefix + "property#";



    public static void main(String[] args) {
        OntModel model = ModelFactory.createOntologyModel();
        model.setNsPrefix("flavordb", flavor_db_prefix);
        model.setNsPrefix("prop", flavor_db_prop_prefix);

        model.createOntology(flavor_db_prefix);

        // add molecule properties from fdb_molecules.csv
        OntClass moleculeClass = model.createClass(flavor_db_prefix + "Molecule");
        AddMoleculeToRDFData.getMoleculeModel("data/fdb_molecules.csv", model, moleculeClass);

        // add entity properties from fdb_entities.csv
        OntClass entityClass = model.createClass(flavor_db_prefix + "Entity");
        AddEntitiesToRDFData.getEntityData("data/fdb_entities.csv", model);

        // add entity to model relations
        AddEntityToMoleculesRDFData.getEntityToMoleculeData("data/fdb_molecules_entities.csv", model, moleculeClass, entityClass);

        try {
            OutputStream os1 = new FileOutputStream("flavor-db-rdf-data-ont.rdf");
            model.write(os1);
            OutputStream os2 = new FileOutputStream("flavor-db-rdf-data-ont-triple-format.rdf");
            model.write(os2, "N-TRIPLE");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
