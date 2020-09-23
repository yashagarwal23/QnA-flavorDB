package flavordb;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;

import java.io.File;
import java.io.FileReader;
import java.util.List;

public class Utils {
    public static List<String[]> readCSV(String filepath) {
        try {
            ClassLoader classLoader = MakeRDFData.class.getClassLoader();
            File file = new File(classLoader.getResource(filepath).getFile());
            FileReader filereader = new FileReader(file);
            CSVReader csvReader = new CSVReaderBuilder(filereader)
                    .build();
            List<String[]> allData = csvReader.readAll();
            return allData;
        } catch (Exception e) {
            System.out.println(e.getClass());
            return null;
        }
    }
}
