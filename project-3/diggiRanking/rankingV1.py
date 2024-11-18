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
            
            # Table's references and caption embedding 
            ref_embedding = embedding.get_sentence_embedding(ref_to_embed)
            caption_embedding = embedding.get_sentence_embedding(table_caption)
            
            # Tried to compute similarity for each token in a table and do mean for discover low level patterns
            # but is not a god choise, cause mean does not give relevance to similar terms
            
            # Similarity is calculated on the entire filtered table 
            # to keep track of the general context without going into detail
            table_embedding = embedding.get_sentence_embedding(filtered_table)
            
           
            # Cosine similarity
            table_similarity = cosine_similarity([embedded_query], [table_embedding])[0][0]
            ref_similarity = cosine_similarity([embedded_query], [ref_embedding])[0][0]
            caption_similarity = cosine_similarity([embedded_query], [caption_embedding])[0][0]
            
            
            # Weights
            w_ref = 0.5
            w_table = 0.3
            w_caption = 0.2
            
            # Weighted average
            similarity_wAvg = (
                w_table * table_similarity + w_ref * ref_similarity + w_caption * caption_similarity
                ) / (
                    w_table + w_ref + w_caption
                    )
            
            #similarity_avg = (table_similarity + ref_similarity + caption_similarity) / 3
            
            #print(table_name)
            #print(table_similarity)
            #print('\n')
            
            table_rank_dict[paper, table_name] = similarity_wAvg
            
    return table_rank_dict
        
#if __name__ == "__main__":{
#    rank(["2102.09694"], "sigmoid")
#}