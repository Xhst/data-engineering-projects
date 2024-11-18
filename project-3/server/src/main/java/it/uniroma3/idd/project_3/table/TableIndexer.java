package it.uniroma3.idd.project_3.table;

import com.google.gson.JsonSyntaxException;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;

@Slf4j
@Component
public class TableIndexer {

    private final Path sourcePath;

    private final IndexWriter indexWriter;

    @Value("${search.index.table.recreate:true}")
    private boolean recreateIndex;

    public TableIndexer(@Qualifier("tableSourcesPath") Path sourcePath,
                        @Qualifier("tableIndexWriter") IndexWriter indexWriter) {
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

        log.info("Start Indexing Tables");

        long startTime = System.currentTimeMillis();

        int totalFiles = 9125;
        int indexedFiles = 0;
        int indexedTables = 0;
        int malformedFiles = 0;

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(sourcePath)) {
            for (Path path : stream) {
                if (Files.isDirectory(path)) continue;

                try {
                    TableParser parser = new TableParser(path);

                    for (TableData table : parser.getTables()) {
                        Document document = new Document();

                        document.add(new TextField("paper_id", table.paperId(), Field.Store.YES));
                        document.add(new TextField("table_id", table.tableId(), Field.Store.YES));
                        document.add(new TextField("table", table.htmlTable(), Field.Store.NO));
                        document.add(new TextField("caption", table.caption(), Field.Store.NO));
                        document.add(new TextField("references", table.references(), Field.Store.NO));
                        document.add(new TextField("footnotes", table.footnotes(), Field.Store.NO));

                        indexWriter.addDocument(document);
                        indexedTables++;
                    }

                    indexedFiles++;

                } catch (JsonSyntaxException e) {
                    malformedFiles++;
                }

                printLoadingBar(indexedFiles, totalFiles);
            }
        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;

        log.info("Indexing completed. Files: {}. Tables: {}. {} Malformed files. Elapsed time: {} seconds", indexedFiles, indexedTables, malformedFiles ,elapsedTime / 1000);

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
