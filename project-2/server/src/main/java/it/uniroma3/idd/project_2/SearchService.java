package it.uniroma3.idd.project_2;

import org.apache.lucene.analysis.Analyzer;

import org.apache.lucene.store.Directory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Map;

@Service
public class SearchService {

    private final Directory index;
    private final Map<String, Analyzer> perFieldAnalyzer;
    private final Path sourcesPath;

    public SearchService(SearchConfig searchConfig) throws IOException {
        this.index = searchConfig.indexDirectory();
        this.perFieldAnalyzer = searchConfig.perFieldAnalyzer();
        this.sourcesPath = searchConfig.getSourcesPath();
    }

}
