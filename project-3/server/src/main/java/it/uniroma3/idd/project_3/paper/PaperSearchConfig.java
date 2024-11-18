package it.uniroma3.idd.project_3.paper;

import org.apache.lucene.analysis.core.KeywordTokenizerFactory;
import org.apache.lucene.analysis.core.LowerCaseFilterFactory;
import org.apache.lucene.analysis.core.StopFilterFactory;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.en.PorterStemFilterFactory;
import org.apache.lucene.analysis.miscellaneous.ASCIIFoldingFilterFactory;
import org.apache.lucene.analysis.miscellaneous.RemoveDuplicatesTokenFilterFactory;
import org.apache.lucene.analysis.miscellaneous.TrimFilterFactory;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizerFactory;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.springframework.context.annotation.DependsOn;
import org.springframework.core.annotation.Order;


import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;

@Configuration("paperConfig")
public class PaperSearchConfig {

    @Value("${search.index.paper.path}")
    private String indexPath;

    @Value("${search.sources.paper.path}")
    private String sourcesPath;

    @Value("${search.index.ram_buffer_size_mb}")
    private double ramBufferSizeMb;

    @Value("${search.index.use_debug_codec}")
    private boolean useDebugCodec;

    public Directory indexDirectory() throws IOException {
        Path indexDirPath = Paths.get(indexPath);
        return FSDirectory.open(indexDirPath);
    }

    @Bean(name = "paperSourcesPath")
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

    @Bean(name = "paperIndexWriter")
    public IndexWriter indexWriter() throws IOException {
        return new IndexWriter(indexDirectory(), indexWriterConfig());
    }

    @Bean(name = "paperIndexSearcher")
    @DependsOn("paperIndexDocuments")
    public IndexSearcher indexSearcher() throws IOException {
        IndexReader indexReader = DirectoryReader.open(indexDirectory());
        return new IndexSearcher(indexReader);
    }

    @Bean(name = "paperQueryParser")
    public MultiFieldQueryParser queryParser() {
        return new MultiFieldQueryParser(
                getPerFieldAnalyzers().keySet().toArray(new String[0]),
                analyzer()
        );
    }


    public Map<String, Analyzer> getPerFieldAnalyzers(){

       try {
           CustomAnalyzer.Builder filenameanalyzerBuilder = CustomAnalyzer.builder()
                   // All content as a single token
                   .withTokenizer(KeywordTokenizerFactory.class)
                   // Removes whitespace at the beginning and end of tokens
                   .addTokenFilter(TrimFilterFactory.class);

           CustomAnalyzer.Builder titleAnalyzerBuilder = CustomAnalyzer.builder()
                   // Filter that remove whitespace and punctuation
                   .withTokenizer(StandardTokenizerFactory.class)
                   // Converts all tokens to lowercase
                   .addTokenFilter(LowerCaseFilterFactory.class)
                   .addTokenFilter(TrimFilterFactory.class);

           CustomAnalyzer.Builder authorsAnalyzerBuilder = CustomAnalyzer.builder()
                   .withTokenizer(StandardTokenizerFactory.class)
                   .addTokenFilter(LowerCaseFilterFactory.class)
                   .addTokenFilter(TrimFilterFactory.class);

           CustomAnalyzer.Builder keywordAnalyzerBuilder = CustomAnalyzer.builder()
                   .withTokenizer(StandardTokenizerFactory.class)
                   .addTokenFilter(LowerCaseFilterFactory.class)
                   .addTokenFilter(TrimFilterFactory.class);

           CustomAnalyzer.Builder abstractAnalyzerBuilder = CustomAnalyzer.builder()
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
                    // Handles synonyms, allowing you to map similar or alternative words to a common token
//                   .addTokenFilter(SynonymGraphFilterFactory.class,
//                           "synonyms", synonymsFilePath,  // Pass the path to the synonyms file
//                           "expand", "true");  // Expand synonyms

           CustomAnalyzer.Builder contentAnalyzerBuilder = CustomAnalyzer.builder()
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
                   // Handles synonyms, allowing you to map similar or alternative words to a common token
//                   .addTokenFilter(SynonymGraphFilterFactory.class,
//                           "synonyms", synonymsFilePath,  // Pass the path to the synonyms file
//                           "expand", "true");  // Expand synonyms


        return Map.of(
                "filename", filenameanalyzerBuilder.build(),
                "title", titleAnalyzerBuilder.build(),
                "authors", authorsAnalyzerBuilder.build(),
                "keywords", keywordAnalyzerBuilder.build(),
                "abstract", abstractAnalyzerBuilder.build(),
                "content", contentAnalyzerBuilder.build()
        );


       } catch (IOException e) {
           throw new RuntimeException(e);
       }
    }
}
