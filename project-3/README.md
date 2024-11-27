# Data Engineering - Project 3

### Assignment
- Write a program that rank tables of scientific papers (such as those extracted from project 1) using lucene indexing (optional: and LM like BERT).
- Write a program that reads the query from console, queries the index (or LM), and prints the result or a small web application where queries can be written through a form.
- Test the system with a dozen different queries

### Valutazione (to translate)

1. Creare tot sistemi diversi (per esempio, lucene, bert, scibert, tabert (con e senza contesto))
2. Creare un sottoinsieme dei paper (tipo 20) da usare come ground truth (o a caso oppure con lucene i più rilevanti per argomento che abbiano tabelle interessanti) - cerchiamo di limitare il numero di tabelle a ca. 50
3. Per ogni query $q \in Q$ (min 5):
    1. Fare il ranking a mano delle tabelle
        - Salviamo i ranking per ogni query in un json, con le informazioni rilevanti, tipo il ranking, il valore di rilevanza per ogni elemento etc.
    2. Interrogare ogni sistema sulla query
    3. Calcolare le metriche: 
        - Reciprocal Rank: $\text{RR}_q = \frac{1}{rank_i}$ dove $i$ è l’elemento più rilevante.
            - nella pratica possiamo controllare se l’elemento scelto dal motore ha almeno lo score massimo (potrebbero esserci dei parimerito)
        - Normalized Discounted Cumulative Gain con taglio $\text{K} = \set{5,15}$:
            
            $
            \text{NDCG@K}_q = \frac{\text{DCG@K}_q}{\text{IDCG@K}_q}
            $
            
            - dove dividiamo il $\text{DCG@K}_q = rel_1 + \sum_{i=2}^K \frac{rel_i}{\log_2 (i + 1)}$ con quello ideale, cioè dove il ranking è il migliore possibile
4. Calcolare la media delle metriche:
    - Mean Reciprocal Rank: $\text{MRR} = \frac{1}{|Q|} \sum_{q \in Q} \text{RR}_q$
    - Media dei NDCG: $\frac{1}{|Q|} \sum_{q \in Q} \text{NDCG@K}_q$

### Query (in verde stesso ranking ma proviamo sinonimi)

1. NDCG su dataset movielens ✅
2. Recommender systems Recall su dataset goodbook ✅
3. Recommender systems MRR ✅
4. Deep Learning dataset Apple Flower ✅
5. Deep Learning GPT3 precision f1 ✅
6. Deep Learning GPT3 precision f-measure ✅

