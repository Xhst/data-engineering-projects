package it.uniroma3.idd.project_2;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;

@Configuration
public class SearchConfig {

    @Value("${search.index.path}")
    private String indexPath;

    @Value("${search.sources.path}")
    private String sourcesPath;

    @Bean
    public Directory indexDirectory() throws IOException {
        Path indexDirPath = Paths.get(indexPath);
        return FSDirectory.open(indexDirPath);
    }

    public Path getSourcesPath() {
        return Paths.get(sourcesPath);
    }

    @Bean
    public IndexWriterConfig indexWriterConfig() {
        Analyzer analyzer = new PerFieldAnalyzerWrapper(new StandardAnalyzer(), getPerFieldAnalyzers());
        IndexWriterConfig config = new IndexWriterConfig(analyzer);

        config.setCodec(new SimpleTextCodec());

        return config;
    }

    private Map<String, Analyzer> getPerFieldAnalyzers() {
        return Map.of(
                "title", new StandardAnalyzer(),
                "authors", new StandardAnalyzer(),
                "keywords", new StandardAnalyzer(),
                "abstract", new StandardAnalyzer(),
                "content", new StandardAnalyzer()
        );
    }
}
