package it.uniroma3.idd.project_3.table;


import java.util.List;

public record TableSearchDto(
        List<TableDto> tables,
        String suggestion,
        long queryTimeMs
) {
}
