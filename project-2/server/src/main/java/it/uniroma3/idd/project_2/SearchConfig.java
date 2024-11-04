package it.uniroma3.idd.project_2;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

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
    public Map<String, Analyzer> perFieldAnalyzer() {
        return Map.of(
                "title", new StandardAnalyzer(),
                "authors", new StandardAnalyzer(),
                "keywords", new StandardAnalyzer(),
                "abstract", new StandardAnalyzer(),
                "content", new StandardAnalyzer()
        );
    }

    @Bean
    public Directory indexDirectory() throws IOException {
        Path indexDirPath = Paths.get(indexPath);
        return FSDirectory.open(indexDirPath);
    }

    public Path getSourcesPath() {
        return Paths.get(sourcesPath);
    }
}
