package it.uniroma3.idd.project_3.table;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class ClientRank {
    public static void main(String[] args) {
        try {
            // URL of python server
            URL url = new URL("http://localhost:5000/process_data");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Configura la richiesta
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            // Make json file to send
            String query = ""; // ---> PASSARE QUERY ================================================================================================
            String[] papers = {}; // ---> PASSARE LISTA DI PAPER CANDIDATI ==========================================================================
            StringBuilder jsonBuilder = new StringBuilder();
            jsonBuilder.append("{");
            jsonBuilder.append("\"query\":\"").append(query).append("\",");
            jsonBuilder.append("\"papers\":[");
            for (int i = 0; i < papers.length; i++) {
                jsonBuilder.append("\"").append(papers[i]).append("\"");
                if (i < papers.length - 1) {
                    jsonBuilder.append(",");
                }
            }
            jsonBuilder.append("]");
            jsonBuilder.append("}");

            String jsonInputString = jsonBuilder.toString();

            // Write the JSON data in the request body
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonInputString.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }

            // Read response
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);
            try (var reader = new java.io.BufferedReader(new java.io.InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = reader.readLine()) != null) {
                    response.append(responseLine.trim());
                }                                                       //===================================================================================================
                System.out.println("Response: " + response.toString()); // ----> BISOGNA SOLO COLLEGARE LA RISPOSTA ALLA LOGICA DELL'APPLICAZIONE AL FINE DI
                                                                        // INVIARLA AL CLIENT (si spera) (ritorna codice paper, codice tabella e rank tabella in formato json)
            }                                                           //===================================================================================================

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
