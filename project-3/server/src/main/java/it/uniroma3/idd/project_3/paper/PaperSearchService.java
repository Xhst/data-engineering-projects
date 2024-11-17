package it.uniroma3.idd.project_3.paper;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class PaperSearchService {

    private final IndexSearcher indexSearcher;
    private final MultiFieldQueryParser queryParser;

    public PaperSearchService(@Qualifier("paperIndexSearcher") IndexSearcher indexSearcher,
                              @Qualifier("paperQueryParser") MultiFieldQueryParser queryParser) {
        this.indexSearcher = indexSearcher;
        this.queryParser = queryParser;
    }

    /**
     * Search for documents in the index based on the query string and the number of results.
     * 
     * @param queryString The query string
     * @param numberOfResults The max number of results that can be returned
     *
     * @return A SearchDto object containing the list of documents found, suggestions and the elapsed times
     *
     * @see PaperSearchDto
     */
    public PaperSearchDto search(String queryString, int numberOfResults) throws IOException, ParseException {
        long startTime = System.currentTimeMillis();
        List<PaperDto> documents = new ArrayList<>();

        Query query = queryParser.parse(queryString);

        TopDocs topDocs = indexSearcher.search(query, numberOfResults);

        StoredFields storedFields = indexSearcher.storedFields();
        for (int i = 0; i < topDocs.scoreDocs.length; i++) {
            ScoreDoc scoreDoc = topDocs.scoreDocs[i];
            Document doc = storedFields.document(scoreDoc.doc);

            documents.add(new PaperDto(
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

        return new PaperSearchDto(documents, "", elapsedTime);
    }

}
