package it.uniroma3.idd.project_2;

import org.apache.lucene.analysis.Analyzer;

import org.apache.lucene.store.Directory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Path;

@Service
public class SearchService {

    private final Directory index;
    private final Analyzer analyzer;
    private final Path sourcesPath;

    public SearchService(SearchConfig searchConfig) throws IOException {
        this.index = searchConfig.indexDirectory();
        this.analyzer = searchConfig.analyzer();
        this.sourcesPath = searchConfig.getSourcesPath();
    }

}
