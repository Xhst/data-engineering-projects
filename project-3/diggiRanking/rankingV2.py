import json
import paths
import embedding
import table_processor


from typing import Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity

json_folder = paths.JSON_FOLDER

def rank(papers, query):
    
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
            filtered_table = table_processor.table_filter(table_name,html_content)
            
            # All fields embedding for keep the contest 
            to_embed = " ".join([filtered_table, ref_to_embed, table_caption])
            embedding = embedding.get_sentence_embedding(to_embed)
            
           
            # Cosine similarity
            similarity = cosine_similarity([embedded_query], [embedding])[0][0]
            
            
            #print(table_name)
            #print(table_similarity)
            #print('\n')
            
            table_rank_dict[paper, table_name] = similarity
            
    return table_rank_dict
        
#if __name__ == "__main__":{
#    rank(["2102.09694"], "sigmoid")
#}