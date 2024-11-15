package it.uniroma3.idd.project_2;

public record DocumentDto(
        String filename,
        String Title,
        String Authors,
        String Keywords,
        String Abstract,
        float score
) {

}
