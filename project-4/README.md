# Data Engineering - Project 4

### Assignment
#### Task 1
From the collection of scientific papers (extracted in project 1), randomly select about 10 papers, each containing around 3 tables each.
The final dataset for this experiments should be composed by more than 30 tables
Extract the claims presented in the tables and in their associated context (references, caption, footnotes). 

Claims must be extracted according to the following format: |{Specification, Specification, …}, Measure, Outcome|
  - Specification: |name, value| pair describing the details of an experiment E.g.: |dataset, Spider|; |LLM, Llama27b|
  - Measure: metric or measure used to evaluate the experiment E.g.: F1-measure
  - Outcome: outcome value related to metric E.g.: 0.89
Extract also a specification called |Task, ...|, which represent the target task (e.g.: |task, record linkage|).
Produce the ground truth for each table.

For each pair (paper, table) you need to produce a json file named `paperID_tableID_claims.json` containing the set of the extracted claims.
Json file should be written following this format:
```json
"Claim 0": "|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.760|"
"Claim 1": ..
```
Json format containing claims: 
```json
[
"0": {
  "specifications": {
    "0": {"name": "Model type", "value": "General LLM"},
    "1": {..}
  },
  "Measure": "Execution Match",
  "Outcome": "0.760"
},
"1": {..},
]
```
(Notice that specifications are numbered)

#### Task 2

Produce a profiling of the extracted claims.
- Distributions of “name” in specification.
- Distributions of “values” for each name of each specification.
- Distributions of “ metrics”.

Produce a spreadsheet with ColumnA key and ColumnB number of items.

Filename should be `NAME_PROFILING.csv` (or xlsx)

#### Task 3
Align specifications names, values and metrics. 

Example:
In some experiments, “dataset” might be mentioned as dataset or benchmarks. Or “model” as model or algorithm.

JSON file for the terms aligned and reproduce the profiling based on these new information. 

Json File: 
```json
{
    "aligned_names": {
        "model type": ["1234.567_2_0_0"],
        "model name": ["1234.567_2_0_1", "6767.9898_4_0_0", "3859.9017_1_0_0"],
..
}
 "aligned_values": {
}
```
In “aligned_names” and “aligned_values”, for each aligned names and values you have to report as paperID_tableID_claimID_specificationID

You can choose the name you prefer for the aligned value or name.

Filename for the alignment is `YOUR_NAME_ALIGNMENT.json`


# Note
### 
- 1812.05040 completed successfully (92.64s)
- 1911.07164 completed successfully (51.82s)
- 2001.11091 completed successfully (130.07s)
- 2011.00695 completed successfully (49.57s)
- 2206.10526 completed successfully (68.41s)
- 2211.16066 completed successfully (3.70s)
- 2401.13405 completed successfully (20.30s)
- 2406.02100 completed successfully (43.42s)
- 2406.20094 completed successfully (44.93s)
- 2407.05174 completed successfully (75.94s)


# Man hours spent

- Ground truth: ∼5 hours
- Alignment: ∼30 mins for ∼30 names, ∼300 values, ∼30 metrics

# chatgpt prompt

I will give you a paper code taken from ar5iv. You must return to me the main data approach that you find in the abstract (only one) of the paper provided. (example: Record Linkage, Synthetic Data, Machine Learning, Data Structures and Algorithms, Operating Systems, Artificial Intelligence, Other Computer Science...)

- 1812.05040 ->  Synthetic Data
- 1911.07164 ->  Synthetic Data
- 2001.11091 ->  Synthetic Data
- 2011.00695 ->  Metric Learning
- 2206.10526 ->  Synthetic Data
- 2211.16066 ->  Synthetic Data
- 2401.13405 ->  Synthetic Data
- 2406.02100 ->  Synthetic Data
- 2406.20094 ->  Synthetic Data
- 2407.05174 ->  Synthetic Data



