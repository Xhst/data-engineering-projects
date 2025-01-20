from enum import Enum

GROUND_TRUTH = '../ground_truth'

class BLOCKING(Enum): 
    RESULTS = '../blocking/results/'

class PAIRWISE_MATCHING(Enum):  
    RESULTS_DM = '../pairwise_matching/results/deep_matcher'
    RESULTS_JAROWINKLER = '../pairwise_matching/results/jarowinkler'