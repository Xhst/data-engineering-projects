package it.uniroma3.idd.project_3.table;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.StoredFields;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class TableSearchService {

    private final IndexSearcher indexSearcher;
    private final MultiFieldQueryParser queryParser;
    private final RestTemplate restTemplate;

    public TableSearchService(@Qualifier("tableIndexSearcher") IndexSearcher indexSearcher,
                              @Qualifier("tableQueryParser") MultiFieldQueryParser queryParser,
                              RestTemplate restTemplate) {
        this.indexSearcher = indexSearcher;
        this.queryParser = queryParser;
        this.restTemplate = restTemplate;
    }


    public TableSearchDto search(String queryString, int numberOfResults) throws IOException, ParseException {
        long startTime = System.currentTimeMillis();
        List<TableDto> tables = new ArrayList<>();

        List<String> paperIds = List.of("a", "b", "c");

        // Construct the query string manually
        String paperIdsQuery = String.join(",", paperIds);

        ResponseEntity<TableSearchDto> response = restTemplate.getForEntity(
                "http://127.0.0.1:8000/api/table/search?query={query}&paper_ids={paper_ids}",
                TableSearchDto.class,
                queryString, paperIdsQuery
        );

        return response.getBody();
        /*
        Query query = queryParser.parse(queryString);

        TopDocs topDocs = indexSearcher.search(query, numberOfResults);

        StoredFields storedFields = indexSearcher.storedFields();
        for (int i = 0; i < topDocs.scoreDocs.length; i++) {
            ScoreDoc scoreDoc = topDocs.scoreDocs[i];
            Document doc = storedFields.document(scoreDoc.doc);

            tables.add(new TableDto(
                    doc.get("paper_id"),
                    doc.get("table_id"),
                    scoreDoc.score
            ));

        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;

        return new TableSearchDto(tables, "", elapsedTime);*/
    }

}
