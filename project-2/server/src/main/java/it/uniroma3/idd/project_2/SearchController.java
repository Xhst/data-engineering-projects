package it.uniroma3.idd.project_2;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/search")
@AllArgsConstructor
public class SearchController {

    private final SearchService searchService;
}
