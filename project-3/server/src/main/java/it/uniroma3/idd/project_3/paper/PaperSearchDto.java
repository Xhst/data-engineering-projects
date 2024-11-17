package it.uniroma3.idd.project_3.paper;

import java.util.List;

public record PaperSearchDto(
        List<PaperDto> documents,
        String suggestion,
        long queryTimeMs
) {

}
