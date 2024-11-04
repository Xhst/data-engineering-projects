package it.uniroma3.idd.project_2;

import org.apache.lucene.analysis.Analyzer;

import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.springframework.stereotype.Service;

import java.nio.file.*;
import java.io.IOException;
import java.nio.file.Path;

@Service
public class SearchService {

    private final Directory index;
    private final IndexWriterConfig config;
    private final Path sourcesPath;

    public SearchService(SearchConfig searchConfig) throws IOException {
        this.index = searchConfig.indexDirectory();
        this.config = searchConfig.indexWriterConfig();
        this.sourcesPath = searchConfig.getSourcesPath();

        this.indexDocuments();
    }

    private void indexDocuments() throws IOException {
        IndexWriter writer = new IndexWriter(index, config);
        writer.deleteAll();

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(sourcesPath)) {
            for (Path path : stream) {
                if (Files.isDirectory(path)) continue;

                DocumentParser parser = new DocumentParser(path);
                Document document = new Document();

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

}
