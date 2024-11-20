import json
import paths
import embedding
import table_preprocess
import tokenizer


from typing import Dict
from sklearn.metrics.pairwise import cosine_similarity

json_folder = paths.JSON_FOLDER

def rank(papers: str, query: str) -> Dict[Tuple[str, str], float]:

    """All table ranking from list of papers (V2)"""
    
    embedded_query = embedding.get_sentence_embedding(query)
    table_rank_dict: Dict[Tuple[str, str], float] = {}
    
    
    for paper in papers:
        # Load JSON file
        with open(f"{json_folder}/{paper}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            
        # Rank for each table
        for table_name, table_data in data.items():
            
            html_content = table_data.get('table', '')
            table_references = table_data.get('references', '')
            table_caption = table_data.get('caption', '')
            
            #print(table_references)
            #print(table_caption)
            
            ref_to_embed = (" ".join(table_references))
            tokenized_ref_to_embed = tokenizer.tokenize_toString(ref_to_embed)
            filtered_table = table_preprocess.table_filter(table_name,html_content)
            
            # All fields embedding for more the contest (also the query)
            to_embed = " ".join([query,filtered_table, tokenized_ref_to_embed, table_caption])
            embed = embedding.get_sentence_embedding(to_embed)
            
           
            # Cosine similarity
            similarity = cosine_similarity([embedded_query], [embed])[0][0]
            
            
            #print(table_name)
            #print(table_similarity)
            #print('\n')
            
            table_rank_dict[paper][table_name] = similarity
            
    return table_rank_dict
        
#if __name__ == "__main__":{
#    rank(["2102.09694"], "sigmoid")
#}