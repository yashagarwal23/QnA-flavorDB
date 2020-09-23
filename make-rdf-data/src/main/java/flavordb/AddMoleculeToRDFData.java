package flavordb;

import org.apache.jena.rdf.model.*;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import static flavordb.MakeRDFData.flavor_db_prefix;
import static flavordb.MakeRDFData.flavor_db_prop_prefix;

public class AddMoleculeToRDFData {

    public static String molecule_prefix = flavor_db_prefix + "molecule#";

    // column idx of properties to be added
    static List<String> props_taken = Arrays.asList("pubchem_id", "iupac_name", "common_name", "odor", "natural", "flavor_profile");
    static List<String> props_name = Arrays.asList("pubchem_id", "iupac_name", "common_name", "odor", "is_natural", "flavor_profile");

    public static void getMoleculeModel(String filepath, Model model) {
        List<String[]> molecules = Utils.readCSV(filepath);
        if(molecules == null)
            return;

        List<String> molecule_heads = Arrays.asList(molecules.get(0));
        HashMap<String, Property> props_map = new HashMap<>();
        HashMap<String, Integer> props_taken_idx = new HashMap<>();

        for(int i = 0; i < props_taken.size(); i++) {
            props_map.put(props_taken.get(i), model.createProperty(flavor_db_prop_prefix + props_name.get(i)));
            props_taken_idx.put(props_taken.get(i), molecule_heads.indexOf(props_taken.get(i)));
        }

        model.setNsPrefix("molecule", molecule_prefix);

        for (int i = 1; i < molecules.size(); ++i) {
            try {
                AddMolecule(molecules.get(i), props_map, props_taken_idx, model);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
    }

    private static void AddMolecule(String[] molecule, HashMap<String, Property> props_map, HashMap<String, Integer> props_taken_idx, Model model) throws UnsupportedEncodingException {
        String pubchem_id =  molecule[0];
        Resource molecule_resource = model.createResource(molecule_prefix + pubchem_id);

        // add pubchem_id
        if(props_map.containsKey("pubchem_id"))
            model.add(molecule_resource, props_map.get("pubchem_id"), molecule[props_taken_idx.get("pubchem_id")]);

        // add iupac name
        if(props_map.containsKey("iupac_name")) {
            String iupac_name = molecule[props_taken_idx.get("iupac_name")];
            if(iupac_name.length() > 0) {
                iupac_name = URLEncoder.encode(iupac_name, "UTF-8");
                model.add(molecule_resource, props_map.get("iupac_name"), iupac_name);
            }
        }

        // add common name
        if(props_map.containsKey("common_name")) {
            String common_name = molecule[props_taken_idx.get("common_name")];
            if(common_name.length() > 0) {
                common_name = URLEncoder.encode(common_name, "UTF-8");
                model.add(molecule_resource, props_map.get("common_name"), common_name);
            }
        }

        // add odor
        if(props_map.containsKey("odor")) {
            String odor = molecule[props_taken_idx.get("odor")].toLowerCase();
            if(odor.length() > 0) {
                String[] odors = odor.split("@");
                for(String o : odors)
                    model.add(molecule_resource, props_map.get("odor"), URLEncoder.encode(o, "UTF-8"));
            }
        }

        // is natural or synthetic
        if(props_map.containsKey("natural")) {
            String nat = molecule[props_taken_idx.get("natural")];
            model.add(molecule_resource, props_map.get("natural"), (nat.equals("1") ? "true" : "false"));
        }

        // add flavor profile
        if(props_map.containsKey("flavor_profile")) {
            String flavor_profile = molecule[props_taken_idx.get("flavor_profile")].toLowerCase();
            if(flavor_profile.length() > 0) {
                String[] flavor_profiles = flavor_profile.split("@");
                for(String profile : flavor_profiles) {
                    model.add(molecule_resource, props_map.get("flavor_profile"), profile);
                }
            }
        }
    }
}
