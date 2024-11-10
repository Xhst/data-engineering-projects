package it.uniroma3.idd.project_2;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
@AllArgsConstructor
public class SearchService {

    private final IndexSearcher indexSearcher;
    private final MultiFieldQueryParser queryParser;

    public SearchDto search(String queryString, int numberOfResults) throws IOException, ParseException {
        long startTime = System.currentTimeMillis();
        List<DocumentDto> documents = new ArrayList<>();

        Query query = queryParser.parse(queryString);

        TopDocs topDocs = indexSearcher.search(query, numberOfResults);

        StoredFields storedFields = indexSearcher.storedFields();
        for (int i = 0; i < topDocs.scoreDocs.length; i++) {
            ScoreDoc scoreDoc = topDocs.scoreDocs[i];
            Document doc = storedFields.document(scoreDoc.doc);

            documents.add(new DocumentDto(
                    doc.get("filename"),
                    doc.get("title"),
                    doc.get("authors"),
                    doc.get("keywords"),
                    doc.get("abstract"),
                    scoreDoc.score
            ));

        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;

        return new SearchDto(documents, "", elapsedTime);
    }

}
