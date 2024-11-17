package it.uniroma3.idd.project_3.table;

import org.jsoup.Jsoup;
import com.google.gson.*;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Getter
public class TableParser {

    private final List<TableData> tables;

    public TableParser(Path filePath) throws IOException, JsonSyntaxException {
        tables = new ArrayList<>();

        String fileNameWithExtension = filePath.getFileName().toString();
        // Remove the file extension
        String[] extensionSplit = fileNameWithExtension.split("\\.");
        String paperId = fileNameWithExtension.replace("." + extensionSplit[extensionSplit.length - 1], "");

        try (FileReader reader = new FileReader(filePath.toFile())) {
            JsonElement jsonElement = JsonParser.parseReader(reader);

            if (jsonElement.isJsonObject()) {
                JsonObject jsonObject = jsonElement.getAsJsonObject();

                for (String tableId : jsonObject.keySet()) {
                    if (!jsonObject.get(tableId).isJsonObject()) continue;

                    JsonObject table = jsonObject.getAsJsonObject(tableId);

                    if (!table.has("caption") || !table.has("table")) continue;

                    String strTable = Jsoup.parse(parseElement(table.get("table"))).text();

                    tables.add(new TableData(
                            paperId,
                            tableId,
                            parseElement(table.get("caption")),
                            strTable,
                            parseElement(table.get("footnotes")),
                            parseElement(table.get("references"))
                    ));
                }
            }
        }
    }

    private String parseElement(JsonElement element) {
        if (element == null) return "";

        if (!element.isJsonArray() && !element.isJsonObject()) {
            return element.toString();
        }

        JsonArray array = element.getAsJsonArray();

        if (array.isEmpty()) return "";

        StringBuilder concatenated = new StringBuilder();
        for (Object item : array) {
            concatenated.append(item.toString()).append(" ");
        }
        return concatenated.toString().trim();
    }

}
