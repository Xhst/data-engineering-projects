package it.uniroma3.idd.project_3.paper;

public record PaperDto(
        String filename,
        String Title,
        String Authors,
        String Keywords,
        String Abstract,
        float score
) {

}
