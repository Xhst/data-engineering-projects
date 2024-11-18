package it.uniroma3.idd.project_3.table;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.KeywordTokenizerFactory;
import org.apache.lucene.analysis.core.LowerCaseFilterFactory;
import org.apache.lucene.analysis.core.StopFilterFactory;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.en.PorterStemFilterFactory;
import org.apache.lucene.analysis.miscellaneous.ASCIIFoldingFilterFactory;
import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.analysis.miscellaneous.RemoveDuplicatesTokenFilterFactory;
import org.apache.lucene.analysis.miscellaneous.TrimFilterFactory;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizerFactory;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;

@Configuration("tableConfig")
public class TableSearchConfig {

    @Value("${search.index.table.path}")
    private String indexPath;

    @Value("${search.sources.table.path}")
    private String sourcesPath;

    @Value("${search.index.ram_buffer_size_mb}")
    private double ramBufferSizeMb;

    @Value("${search.index.use_debug_codec}")
    private boolean useDebugCodec;

    public Directory indexDirectory() throws IOException {
        Path indexDirPath = Paths.get(indexPath);
        return FSDirectory.open(indexDirPath);
    }

    @Bean(name = "tableSourcesPath")
    public Path sourcesPath() {
        return Paths.get(sourcesPath);
    }


    public Analyzer analyzer() {
        return new PerFieldAnalyzerWrapper(new StandardAnalyzer(), getPerFieldAnalyzers());
    }

    public IndexWriterConfig indexWriterConfig() {
        Analyzer analyzer = analyzer();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);

        if (useDebugCodec) {
            config.setCodec(new SimpleTextCodec());
        }

        config.setRAMBufferSizeMB(ramBufferSizeMb);

        return config;
    }

    @Bean(name = "tableIndexWriter")
    public IndexWriter indexWriter() throws IOException {
        return new IndexWriter(indexDirectory(), indexWriterConfig());
    }

    @Bean(name = "tableIndexSearcher")
    public IndexSearcher indexSearcher() throws IOException {
        IndexReader indexReader = DirectoryReader.open(indexDirectory());
        return new IndexSearcher(indexReader);
    }

    @Bean(name = "tableQueryParser")
    public MultiFieldQueryParser queryParser() {
        return new MultiFieldQueryParser(
                getPerFieldAnalyzers().keySet().toArray(new String[0]),
                analyzer()
        );
    }


    public Map<String, Analyzer> getPerFieldAnalyzers(){

       try {
           CustomAnalyzer.Builder idAnalyzer = CustomAnalyzer.builder()
                   // All content as a single token
                   .withTokenizer(KeywordTokenizerFactory.class)
                   // Removes whitespace at the beginning and end of tokens
                   .addTokenFilter(TrimFilterFactory.class);

           CustomAnalyzer.Builder textAnalyzer = CustomAnalyzer.builder()
                   .withTokenizer(StandardTokenizerFactory.class)
                   .addTokenFilter(LowerCaseFilterFactory.class)
                   .addTokenFilter(TrimFilterFactory.class)
                   // Apply a stemming algorithm to reduce words to their root
                   .addTokenFilter(PorterStemFilterFactory.class)
                   // Remove stop-words
                   .addTokenFilter(StopFilterFactory.class)
                   // Removes consecutive duplicate tokens
                   .addTokenFilter(RemoveDuplicatesTokenFilterFactory.class)
                   // Converts accented characters to plain ASCII characters
                   .addTokenFilter(ASCIIFoldingFilterFactory.class);

           CustomAnalyzer.Builder tableAnalyzer = CustomAnalyzer.builder()
                   .withTokenizer(StandardTokenizerFactory.class)
                   .addTokenFilter(LowerCaseFilterFactory.class)
                   .addTokenFilter(TrimFilterFactory.class)
                   // Converts accented characters to plain ASCII characters
                   .addTokenFilter(ASCIIFoldingFilterFactory.class);


        return Map.of(
                "paper_id", idAnalyzer.build(),
                "table_id", idAnalyzer.build(),
                "caption", textAnalyzer.build(),
                "table", tableAnalyzer.build(),
                "footnotes", textAnalyzer.build(),
                "references", textAnalyzer.build()
        );


       } catch (IOException e) {
           throw new RuntimeException(e);
       }
    }
}
