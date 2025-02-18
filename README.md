# Data Engineering Projects

Group projects for the course **Data Engineering** held by professor Paolo Merialdo at Roma Tre University. 

#

- ### [Project 1](/project-1/README.md) - Scraping & Data extraction:

  Downloading scientific papers from [Arxiv](https://arxiv.org/) (in html format) and extracting information regarding tables from them using xpaths.

#

- ### [Project 2](/project-2/README.md) - Paper Search Engine:

  Search engine for scientific papers, extracted in the previous project.
  
  Server made with [Apache Lucene](https://lucene.apache.org/) and [SpringBoot](https://spring.io/projects/spring-boot) (Java).
  
  Client made with Typescript and Bootstrap.

#

- ### [Project 3](/project-3/README.md) - Table Search Engine + Semantich Search:

  Continuation of project 2 with the introduction of the table search engine. Semantic search with evaluation of different models (e.g., BERT, All MiniLM v2) and different embedding methods.

#

- ### [Project 4](/project-4/README.md) - Table data extraction and understanding:
Knowledge extraction from html tables (from project 1) using LLMs.
#

- ### [Project 5](/project-5/README.md) - Data Integration of Companies:
Integration of companies data from 16 different sources. The mediated schema is realized with the use of LLMs to generate field descriptions, on which embeddings were subsequently calculated and then used to do clustering (with HDBSCAN). The Blocking is done using Locality Sensitive Hashing (LSH) with words and bi-gram vectors. The final step of pairwise matching is realized with 3 different approaches: DITTO, DeepMatcher and Jaro-Winkler.
#
