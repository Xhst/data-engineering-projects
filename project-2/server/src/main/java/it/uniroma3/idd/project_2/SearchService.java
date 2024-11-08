package it.uniroma3.idd.project_2;

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

import java.nio.file.*;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class SearchService {

    private final Path sourcePath;
    private final IndexWriter indexWriter;
    private final IndexSearcher indexSearcher;
    private final MultiFieldQueryParser queryParser;

    public SearchService(
            Path sourcePath,
            IndexWriter indexWriter,
            IndexSearcher indexSearcher,
            MultiFieldQueryParser queryParser) throws IOException {
        this.sourcePath = sourcePath;
        this.indexWriter = indexWriter;
        this.indexSearcher = indexSearcher;
        this.queryParser = queryParser;

        this.indexDocuments();
    }

    private static void printLoadingBar(int indexedFiles, int totalFiles) {
        int barLength = 100; // Total length of the loading bar
        int progress = (int) ((double) indexedFiles / totalFiles * barLength);

        StringBuilder bar = new StringBuilder();
        bar.append("\r Indexing - [");
        for (int i = 0; i < barLength; i++) {
            if (i < progress) {
                bar.append("#");
            } else {
                bar.append("-");
            }
        }
        bar.append("] ");
        bar.append(indexedFiles).append("/").append(totalFiles);
        bar.append(" files.");

        // Print the progress bar
        System.out.print(bar);

        // Print a new line when indexing is complete
        if (indexedFiles == totalFiles) {
            System.out.println();
        }
    }

    private void indexDocuments() throws IOException {
        indexWriter.deleteAll();

        log.info("Start Indexing");

        long startTime = System.currentTimeMillis();

        int totalFiles = 9235; //9372;
        int indexedFiles = 0;

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(sourcePath)) {
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

                indexWriter.addDocument(document);
                indexedFiles++;

                printLoadingBar(indexedFiles, totalFiles);
            }
        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;

        log.info("Indexing completed. Files: {}. Elapsed time: {} seconds", indexedFiles, elapsedTime / 1000);

        indexWriter.commit();
        indexWriter.close();
    }

    public List<DocumentDto> search(String queryString) throws IOException, ParseException {
        List<DocumentDto> documents = new ArrayList<>();

        Query query = queryParser.parse(queryString);

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

        return documents;
    }

}
