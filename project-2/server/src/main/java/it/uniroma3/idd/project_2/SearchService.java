package it.uniroma3.idd.project_2;

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

import java.nio.file.*;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Service
public class SearchService {

    private final SearchConfig config;

    public SearchService(SearchConfig searchConfig) throws IOException {
        this.config = searchConfig;

        this.indexDocuments();
    }

    private void indexDocuments() throws IOException {
        IndexWriter writer = new IndexWriter(config.indexDirectory(), config.indexWriterConfig());
        writer.deleteAll();

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(config.getSourcesPath())) {
            for (Path path : stream) {
                if (Files.isDirectory(path)) continue;

                DocumentParser parser = new DocumentParser(path);
                Document document = new Document();

                document.add(new TextField("filename", parser.getFileName(), Field.Store.YES));
                document.add(new TextField("title", parser.getTitle(), Field.Store.YES));
                document.add(new TextField("authors", parser.getAuthors(), Field.Store.YES));
                document.add(new TextField("keywords", parser.getKeywords(), Field.Store.YES));
                document.add(new TextField("abstract", parser.getAbstract(), Field.Store.YES));
                document.add(new TextField("content", parser.getContent(), Field.Store.NO));

                writer.addDocument(document);
            }
        }

        writer.commit();
        writer.close();
    }

    public List<DocumentDto> search(String queryString) throws IOException, ParseException {
        List<DocumentDto> documents = new ArrayList<>();

        MultiFieldQueryParser queryParser = new MultiFieldQueryParser(
                config.getPerFieldAnalyzers().keySet().toArray(new String[0]),
                config.analyzer()
        );

        Query query = queryParser.parse(queryString);

        try (IndexReader indexReader = DirectoryReader.open(config.indexDirectory())) {
            IndexSearcher indexSearcher = new IndexSearcher(indexReader);
            TopDocs topDocs = indexSearcher.search(query, 50);

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
        }

        return documents;
    }

}
