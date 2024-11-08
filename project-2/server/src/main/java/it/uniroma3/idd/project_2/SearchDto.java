package it.uniroma3.idd.project_2;

import java.util.List;

public record SearchDto(
        List<DocumentDto> documents,
        String suggestion,
        long queryTimeMs
) {

}
