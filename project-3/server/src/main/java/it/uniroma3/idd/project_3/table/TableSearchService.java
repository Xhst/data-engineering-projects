package it.uniroma3.idd.project_3.table;

import lombok.extern.slf4j.Slf4j;
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

@Slf4j
@Service
public class TableSearchService {

    private final IndexSearcher indexSearcher;
    private final MultiFieldQueryParser queryParser;
    private final RestTemplate restTemplate;

    private final List<String> groundTruthPapers = List.of(
            "2008.03797", "2102.08921", "2301.04366v1", "2404.17723", "2405.02156v1", "2405.17060v1",
            "2406.02638v2", "2407.03440", "2407.09157v1", "2407.13531v1", "2408.04641v1", "2408.09646v1",
            "2409.10272", "2409.10309v2", "2409.17165v1", "2409.17400"
    );

    public TableSearchService(@Qualifier("tableIndexSearcher") IndexSearcher indexSearcher,
                              @Qualifier("tableQueryParser") MultiFieldQueryParser queryParser,
                              RestTemplate restTemplate) {
        this.indexSearcher = indexSearcher;
        this.queryParser = queryParser;
        this.restTemplate = restTemplate;
    }


    public TableSearchDto search(String queryString, String modelName, String methodName, int numberOfResults,
                                 boolean useHybridApproach, boolean useGroundTruth) throws IOException, ParseException {
        long startTime = System.currentTimeMillis();
        List<TableDto> tables = new ArrayList<>();
        List<String> paperIds = new ArrayList<>();

        if (!useHybridApproach) {
            Query query = queryParser.parse(queryString);

            TopDocs topDocs = indexSearcher.search(query, numberOfResults);

            StoredFields storedFields = indexSearcher.storedFields();
            for (int i = 0; i < topDocs.scoreDocs.length; i++) {
                ScoreDoc scoreDoc = topDocs.scoreDocs[i];
                Document doc = storedFields.document(scoreDoc.doc);

                if (useGroundTruth && !groundTruthPapers.contains(doc.get("paper_id"))) continue;

                paperIds.add(doc.get("paper_id"));

                tables.add(new TableDto(
                        doc.get("paper_id"),
                        doc.get("table_id"),
                        scoreDoc.score
                ));
            }

            long endTime = System.currentTimeMillis();
            long elapsedTime = endTime - startTime;

            if (methodName.equals("lucene") || modelName.equals("lucene")) {
                return new TableSearchDto(tables, "", elapsedTime);
            }
        }

        ResponseEntity<TableSearchDto> response = restTemplate.getForEntity(
                "http://127.0.0.1:8000/api/table/search?query={query}&paper_ids={paper_ids}&model_name={model_name}&method_name={method_name}&use_hybrid_approach={use_hybrid_approach}",
                TableSearchDto.class,
                queryString, paperIds, modelName, methodName, useHybridApproach
        );

        return response.getBody();
    }

}
