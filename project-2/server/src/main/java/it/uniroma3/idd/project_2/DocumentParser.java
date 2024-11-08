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
        // Split the path by backslashes to get the file name with extension
        String[] split = document.location().split("\\\\");
        String fileNameWithExtension = split[split.length - 1];

        // Remove the file extension
        String[] extensionSplit = fileNameWithExtension.split("\\.");
        String baseFileName = fileNameWithExtension.replace("." + extensionSplit[extensionSplit.length - 1], "");

        // Check if the base name contains "arXiv" pattern and extract accordingly
        if (baseFileName.contains("arXiv")) {
            int arXivIndex = baseFileName.indexOf("arXiv");
            // Return only the portion after "arXiv"
            return baseFileName.substring(arXivIndex + "arXiv".length());
        }

        return baseFileName;
    }

    public String getTitle() {
        String idTag = "[" + getFileName() + "]";
        String title = document.title();

        if (title.isEmpty()) {
            Element el = document.selectFirst("h1, .ltx_title");
            if (el == null) return "";

            title = el.ownText();
        }

        return title.replace(idTag, "").trim();
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

        String text = el.text();

        // Check if the text starts with "Abstract" and remove it
        if (text.startsWith("Abstract")) {
            text = text.substring("Abstract".length()).trim();
        }

        return text;
    }

    public String getContent() {
        return document.body().text();
    }

}
