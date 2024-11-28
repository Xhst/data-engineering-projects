from embedder import Embedder
from table_preprocess import table_filter
import tokenizer


def tab_embedding(embedder: Embedder, table_data):
    """
    Compute embeddings for table content only.

    Args:
        embedder (Embedder): An instance of the Embedder class to generate sentence embeddings.
        table_data (dict): A dictionary containing the table data. 
                           Must have a key "table" with the table content.

    Returns:
        numpy.ndarray: The embedding for the table content.
    """
    return embedder.get_sentence_embedding(table_data["paperTitle"] + table_filter(table_data["table"]))


def tab_cap_embedding(embedder: Embedder, table_data):
    """
    Compute embeddings for table content combined with its caption.

    Args:
        embedder (Embedder): An instance of the Embedder class to generate sentence embeddings.
        table_data (dict): A dictionary containing table data. 
                           Must have keys "table" for table content and "caption" for the table's caption.

    Returns:
        numpy.ndarray: The embedding for the concatenated table content and caption.
    """
    return embedder.get_sentence_embedding(
        table_filter(table_data["paperTitle"] + table_data["table"]) + table_data["caption"]
    )


def tab_cap_ref_embedding(embedder: Embedder, table_data):
    """
    Compute embeddings for table content, caption, and references.

    Args:
        embedder (Embedder): An instance of the Embedder class to generate sentence embeddings.
        table_data (dict): A dictionary containing table data. 
                           Must have keys "table" for table content, "caption" for the table's caption, 
                           and "references" for a list of references.

    Returns:
        numpy.ndarray: The embedding for the concatenated table content, caption, and references.
    """
    return embedder.get_sentence_embedding(
        table_data["paperTitle"]
        + table_filter(table_data["table"]) 
        + table_data["caption"] 
        + tokenizer.filter(" ".join(table_data["references"]))
    )


def weighted_embedding(embedder: Embedder, table_data):
    """
    Compute a weighted embedding by combining embeddings of table content, caption, and references.

    Args:
        embedder (Embedder): An instance of the Embedder class to generate sentence embeddings.
        table_data (dict): A dictionary containing table data. 
                           Must have keys "table" for table content, "caption" for the table's caption, 
                           and "references" for a list of references.

    Returns:
        numpy.ndarray: The weighted embedding, computed as a weighted sum of embeddings for 
                       table content, caption, and references.
    """
    table_embedding = embedder.get_sentence_embedding(table_filter(table_data["table"]))
    # Caption with paper title
    caption_embedding = embedder.get_sentence_embedding(table_data["paperTitle"] + table_data["caption"])
    references_embedding = embedder.get_sentence_embedding(tokenizer.filter(" ".join(table_data["references"])))

    w_tab = 0.5  # Weight for the table content
    w_cap = 0.35  # Weight for the caption
    w_ref = 0.15  # Weight for the references

    return (w_tab * table_embedding + w_cap * caption_embedding + w_ref * references_embedding).tolist()


def get_function_from_name(function_name: str):
    """
    Retrieve a function object based on its name.

    Args:
        function_name (str): The name of the function to retrieve. 

    Returns:
        function: The function object corresponding to the provided name.

    Raises:
        ValueError: If the provided function name is not recognized.
    """
    if function_name == "tab_embedding":
        return tab_embedding
    elif function_name == "tab_cap_embedding":
        return tab_cap_embedding
    elif function_name == "tab_cap_ref_embedding":
        return tab_cap_ref_embedding
    elif function_name == "weighted_embedding":
        return weighted_embedding
    else:
        raise ValueError("Invalid function name")
