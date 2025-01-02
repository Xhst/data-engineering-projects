from enum import Enum

RAW = '../../project-1/extraction/forward_extractor'
PROFILING = '../profiling'
CLAIMS = '../claims'
ALIGNMENT = '../alignment'
LLM_RESPONSE = '../llm_response'

class GROUND_TRUTH(Enum):
    PAPERS = '../ground_truth/papers'
    CLAIMS = '../ground_truth/claims'