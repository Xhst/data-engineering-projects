package it.uniroma3.idd.project_2;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;

public class DocumentParser {

    private final Document document;

    public DocumentParser(Path filePath) throws IOException {
        File file = new File(filePath.toString());
        this.document = Jsoup.parse(file, "UTF-8");
    }

    public String getFileName() {
        String[] split = document.location().split("\\\\");
        String fileNameWithExtension = split[split.length - 1];
        String[] extensionSplit = fileNameWithExtension.split("\\.");
        String extension = extensionSplit[extensionSplit.length - 1];
        return fileNameWithExtension.replace("." + extension, "");
    }

    public String getTitle() {
        String idTag = "[" + getFileName() + "]";
        return document.title().replace(idTag, "").trim();
    }

    public String getAuthors() {
        Element el = document.selectFirst(".ltx_authors");

        if (el == null) return "";

        return el.text();
    }

    public String getKeywords() {
        Element el = document.selectFirst("meta[name=keywords]");

        if (el == null) return "";

        return el.attr("content");
    }

    public String getAbstract() {
        Element el = document.selectFirst(".ltx_abstract");

        if (el == null) return "";

        return el.text();
    }

    public String getContent() {
        return document.body().text();
    }

}
