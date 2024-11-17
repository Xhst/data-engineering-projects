package it.uniroma3.idd.project_3;

import it.uniroma3.idd.project_3.paper.PaperSearchService;
import it.uniroma3.idd.project_3.table.TableSearchService;
import lombok.AllArgsConstructor;
import org.apache.lucene.queryparser.classic.ParseException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/search")
@AllArgsConstructor
public class SearchController {

    private final PaperSearchService paperSearchService;
    private final TableSearchService tableSearchService;

    @GetMapping("/papers")
    public ResponseEntity<?> searchPapers(@RequestParam String query, @RequestParam(defaultValue = "50") int numberOfResults) {
        try {
            return ResponseEntity.ok(paperSearchService.search(query, numberOfResults));
        } catch (ParseException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @GetMapping("/tables")
    public ResponseEntity<?> searchTables(@RequestParam String query, @RequestParam(defaultValue = "50") int numberOfResults) {
        try {
            return ResponseEntity.ok(tableSearchService.search(query, numberOfResults));
        } catch (ParseException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }
}
