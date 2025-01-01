# Data Engineering - Project 5

### Assignment
The goal is to integrate data [sources](./sources) of companies.

Analyze all data sources and identify major heterogeneities.

Define an appropriate mediated schema that has at least 20 attributes. Align the source schemas with the mediated schema.

Populate the mediated schema with the aligned data sources.

Create a ground-truth with at least 100 matching pairs. Make sure that the ground-truth also contains “difficult” cases.

Define at least two different blocking strategies.

Calculate pairwise matchting with the Python Record [Linkage Toolkit library](https://recordlinkage.readthedocs.io/en/latest/) (also offers blocking solutions) from the different blocking strategies chosen and accurately compare the results.

Compute pairwise matching with an alternative tool from the following:
  - [DeepMatcher](https://github.com/anhaidgroup/deepmatcher) (neural network solution) 
  - [Ditto](https://github.com/megagonlabs/ditto) (neural network solution)  
  - [EMT](https://github.com/brunnurs/entity-matching-transformer) (neural network solution very similar to Ditto)
    
Compare the results that are obtained using different combinations of blocking and pairwise matching.
