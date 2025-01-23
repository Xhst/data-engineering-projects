from enum import Enum

GROUND_TRUTH = '../ground_truth'
DATASET = '../dataset'

class MODELS(Enum):
    DATA_SPLITS = '../models/data_splits'
    DEEP_MATCHER = '../models/deep_matcher'

class BLOCKING(Enum): 
    RESULTS = '../blocking/results/'

class PAIRWISE_MATCHING(Enum):  
    RESULTS_DM = '../pairwise_matching/results/deep_matcher'
    RESULTS_DM_UNLABELED = '../pairwise_matching/results/deep_matcher/unlabeled_pairs'
    RESULTS_DM_PREDICTED = '../pairwise_matching/results/deep_matcher/pairs_prediction'
    RESULTS_JAROWINKLER = '../pairwise_matching/results/jarowinkler'