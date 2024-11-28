package it.uniroma3.idd.project_3;

import it.uniroma3.idd.project_3.paper.PaperSearchService;
import it.uniroma3.idd.project_3.table.TableSearchService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.lucene.queryparser.classic.ParseException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
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
    public ResponseEntity<?> searchTables(
            @RequestParam String queryArgument,
            @RequestParam String queryTable,
            @RequestParam(defaultValue = "distilbert-base-uncased") String modelName,
            @RequestParam(defaultValue = "tab_cap_embedding") String methodName,
            @RequestParam(defaultValue = "10000") int numberOfResults,
            @RequestParam(defaultValue = "true") boolean useHybrid,
            @RequestParam(defaultValue = "false") boolean useGroundTruth) {
        try {
            return ResponseEntity.ok(
                    tableSearchService.search(queryArgument, queryTable, modelName, methodName, numberOfResults, useHybrid, useGroundTruth)
            );
        } catch (ParseException e) {
            log.error(e.getMessage());
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            log.error(e.getMessage());
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }
}
