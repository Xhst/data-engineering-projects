package it.uniroma3.idd.project_2;

import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;

@Slf4j
@Component
public class Indexer {

    private final Path sourcePath;
    private final IndexWriter indexWriter;

    @Value("${search.index.recreate:true}")
    private boolean recreateIndex;

    public Indexer(Path sourcePath, IndexWriter indexWriter) throws IOException {
        this.sourcePath = sourcePath;
        this.indexWriter = indexWriter;
    }

    @PostConstruct
    private void indexDocuments() throws IOException {
        if (!recreateIndex) {
            indexWriter.close();
            return;
        }

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
}
