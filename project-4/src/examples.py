from dataclasses import dataclass

@dataclass
class ExtractionExample:
    table: str
    caption: str
    references: list[str]
    result: str

    def __str__(self):
        return f"""
        [Table]: 
        {self.table}
        [Caption]: 
        {self.caption}
        [References]: 
        {self.references}
        [Response]: 
        {self.result}
        """
# 1911.07164.S3.T1
example1 = ExtractionExample(
    table="""
|:---------------------|-------------------:|----------------------:|---------------------:|
| Original             |               69.6 |                  75   |                 74.1 |
| Original + Generated |               70.1 |                  74.6 |                 73.8 |
    """,
    caption="Table 1: CUB 5-way-1-shot classification accuracy (%)\nusing ImageNet features. Simply adding generated images to the training\nset does not help, but adding hybrid imageson CUB/NAB dataset.",
    references=[
        """
        Our goal is not to generate images, but to augment the training data\nfor few shot learning. A naive way to do this is to apply the above generation\ntechnique for 
        each training image, in order to double the training set. We\ntested this idea on a validation set (split the same as [4]) from\nthe Caltech-UCSD bird dataset\u00a0[32] 
        and computed average accuracy on 100 episodes of\n5-way-1-shot classification. We used pre-trained ImageNet features from\nResNet18\u00a0[16]
        with nearest neighbor, one-vs-all logistic\nregression, and softmax regression (or multi-class logistic regression).\nAs shown in Table\u00a01, 
        the accuracy actually drops for two of the three classifiers when we double\nthe size of our training set by generating synthetic training images, 
        suggesting\nthat the\ngenerated images are harmful for training classifiers.
        """
    ],
    result="""
        |{|dataset, CUB/NAB|, |Training Data, Original|, |classifier, Nearest Neighbor|}, CUB 5-way-1-shot classification accuracy, 69.6|
        |{|dataset, CUB/NAB|, |Training Data, Original|, |classifier,Logistic Regression|}, CUB 5-way-1-shot classification accuracy, 75|
        |{|dataset, CUB/NAB|, |Training Data, Original|, |classifier Softmax Regression|}, CUB 5-way-1-shot classification accuracy, 74.1|
        |{|dataset, CUB/NAB|, |Training Data, Original + Generated|, |classifier, Nearest Neighbor|}, CUB 5-way-1-shot classification accuracy, 70.1|
        |{|dataset, CUB/NAB|, |Training Data, Original + Generated|, |classifier, Logistic Regression|}, CUB 5-way-1-shot classification accuracy, 74.6|
    """
)

example2_long = ExtractionExample(
    table="""
| Model Type           | Model Name              | Parameter Size | Level 1   | Level 2   | Level 3   | Level 4   | All     |
|:---------------------|:------------------------|:---------------|----------:|----------:|----------:|----------:|--------:|
| General LLM          | ChatGPT-3.5-turbo       | 175B           |     0.760 |     0.799 |     0.408 |     0.493 |   0.623 |
| General LLM          | DIN-SQL+GPT-4           | 1.76T          |     0.861 |     0.866 |     0.700 |     0.654 |   0.762 |
| General LLM          | CodeX-Davinci-3         | 175B           |     0.730 |     0.799 |     0.392 |     0.382 |   0.570 |
| General LLM          | MPT-7B-instruct         | 7B             |     0.262 |     0.381 |     0.117 |     0.091 |   0.205 |
| General LLM          | ALPACA                  | 7B             |     0.311 |     0.460 |     0.192 |     0.083 |   0.242 |
| General LLM          | KOALA                   | 7B             |     0.195 |     0.218 |     0.017 |     0.071 |   0.131 |
| General LLM          | OpenAssistant-pythia    | 12B            |     0.202 |     0.322 |     0.025 |     0.069 |   0.157 |
| General LLM          | ORCA-mini               | 7B             |     0.243 |     0.280 |     0.101 |     0.076 |   0.169 |
| General LLM          | LLaMA-2                 | 7B             |     0.225 |     0.393 |     0.101 |     0.081 |   0.192 |
| Code Specific LLM    | CodeGen2                | 7B             |     0.375 |     0.498 |     0.167 |     0.066 |   0.257 |
| Code Specific LLM    | Starcoder               | 15.5B          |     0.584 |     0.628 |     0.275 |     0.208 |   0.410 |
| Code Specific LLM    | Vicuna                  | 7B             |     0.060 |     0.134 |     0.008 |     0.042 |   0.064 |
| Code Specific LLM    | nsql                    | 6B             |     0.772 |     0.732 |     0.608 |     0.277 |   0.548 |
| Seq-to-Seq Model     | T5(tscholak/cxmefzzi)   | 3B             |     0.828 |     0.782 |     0.650 |     0.434 |   0.641 |
| Seq-to-Seq Model     | PICARD+T5               | 3B             |     0.790 |     0.799 |     0.558 |     0.502 |   0.652 |
| Seq-to-Seq Model     | RESDSQL                 | 3B             |     0.872 |     0.857 |     0.666 |     0.696 |   0.775 |
""",
    
    caption="Table 1. Benchmark Results of Execution Match of all Models we tested on the 'dev' SPIDER dataset",
    
    references=["""
                In our experimentation, we organized the models into three distinct groups as illustrated in Table 1: general purpose LLMs, Code-Specific LLMs, and Sequence-to-Sequence models. Table 1 further presents the Execution Match score on the SPIDER dataset for each studied LLM and for each of the four difficulty levels.
                """],
    result="""
    |{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.760|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.799|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.408|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.493|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.623|
|{|Model Type, General LLM|, |Model Name, DIN-SQL+GPT-4|, |Parameter Size, 1.76T|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.861|
|{|Model Type, General LLM|, |Model Name, DIN-SQL+GPT-4|, |Parameter Size, 1.76T|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.866|
|{|Model Type, General LLM|, |Model Name, DIN-SQL+GPT-4|, |Parameter Size, 1.76T|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.700|
|{|Model Type, General LLM|, |Model Name, DIN-SQL+GPT-4|, |Parameter Size, 1.76T|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.654|
|{|Model Type, General LLM|, |Model Name, DIN-SQL+GPT-4|, |Parameter Size, 1.76T|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.762|
|{|Model Type, General LLM|, |Model Name, CodeX-Davinci-3|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.730|
|{|Model Type, General LLM|, |Model Name, CodeX-Davinci-3|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.799|
|{|Model Type, General LLM|, |Model Name, CodeX-Davinci-3|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.392|
|{|Model Type, General LLM|, |Model Name, CodeX-Davinci-3|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.382|
|{|Model Type, General LLM|, |Model Name, CodeX-Davinci-3|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.570|
|{|Model Type, General LLM|, |Model Name, MPT-7B-instruct|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.262|
|{|Model Type, General LLM|, |Model Name, MPT-7B-instruct|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.381|
|{|Model Type, General LLM|, |Model Name, MPT-7B-instruct|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.117|
|{|Model Type, General LLM|, |Model Name, MPT-7B-instruct|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.091|
|{|Model Type, General LLM|, |Model Name, MPT-7B-instruct|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.205|
|{|Model Type, General LLM|, |Model Name, ALPACA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.311|
|{|Model Type, General LLM|, |Model Name, ALPACA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.460|
|{|Model Type, General LLM|, |Model Name, ALPACA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.192|
|{|Model Type, General LLM|, |Model Name, ALPACA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.083|
|{|Model Type, General LLM|, |Model Name, ALPACA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.242|
|{|Model Type, General LLM|, |Model Name, KOALA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.195|
|{|Model Type, General LLM|, |Model Name, KOALA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.218|
|{|Model Type, General LLM|, |Model Name, KOALA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.017|
|{|Model Type, General LLM|, |Model Name, KOALA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.071|
|{|Model Type, General LLM|, |Model Name, KOALA|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.131|
|{|Model Type, General LLM|, |Model Name, OpenAssistant-pythia|, |Parameter Size, 12B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.202|
|{|Model Type, General LLM|, |Model Name, OpenAssistant-pythia|, |Parameter Size, 12B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.322|
|{|Model Type, General LLM|, |Model Name, OpenAssistant-pythia|, |Parameter Size, 12B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.025|
|{|Model Type, General LLM|, |Model Name, OpenAssistant-pythia|, |Parameter Size, 12B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.069|
|{|Model Type, General LLM|, |Model Name, OpenAssistant-pythia|, |Parameter Size, 12B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.157|
|{|Model Type, General LLM|, |Model Name, ORCA-mini|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.243|
|{|Model Type, General LLM|, |Model Name, ORCA-mini|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.280|
|{|Model Type, General LLM|, |Model Name, ORCA-mini|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.101|
|{|Model Type, General LLM|, |Model Name, ORCA-mini|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.076|
|{|Model Type, General LLM|, |Model Name, ORCA-mini|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.169|
|{|Model Type, General LLM|, |Model Name, LLaMA-2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.225|
|{|Model Type, General LLM|, |Model Name, LLaMA-2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.393|
|{|Model Type, General LLM|, |Model Name, LLaMA-2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.101|
|{|Model Type, General LLM|, |Model Name, LLaMA-2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.081|
|{|Model Type, General LLM|, |Model Name, LLaMA-2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.192|
|{|Model Type, Code Specific LLM|, |Model Name, CodeGen2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.375|
|{|Model Type, Code Specific LLM|, |Model Name, CodeGen2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.498|
|{|Model Type, Code Specific LLM|, |Model Name, CodeGen2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.167|
|{|Model Type, Code Specific LLM|, |Model Name, CodeGen2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.066|
|{|Model Type, Code Specific LLM|, |Model Name, CodeGen2|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.257|
|{|Model Type, Code Specific LLM|, |Model Name, Starcoder|, |Parameter Size, 15.5B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.584|
|{|Model Type, Code Specific LLM|, |Model Name, Starcoder|, |Parameter Size, 15.5B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.628|
|{|Model Type, Code Specific LLM|, |Model Name, Starcoder|, |Parameter Size, 15.5B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.275|
|{|Model Type, Code Specific LLM|, |Model Name, Starcoder|, |Parameter Size, 15.5B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.208|
|{|Model Type, Code Specific LLM|, |Model Name, Starcoder|, |Parameter Size, 15.5B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.410|
|{|Model Type, Code Specific LLM|, |Model Name, Vicuna|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.060|
|{|Model Type, Code Specific LLM|, |Model Name, Vicuna|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.134|
|{|Model Type, Code Specific LLM|, |Model Name, Vicuna|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.008|
|{|Model Type, Code Specific LLM|, |Model Name, Vicuna|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.042|
|{|Model Type, Code Specific LLM|, |Model Name, Vicuna|, |Parameter Size, 7B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.064|
|{|Model Type, Code Specific LLM|, |Model Name, nsql|, |Parameter Size, 6B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.772|
|{|Model Type, Code Specific LLM|, |Model Name, nsql|, |Parameter Size, 6B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.732|
|{|Model Type, Code Specific LLM|, |Model Name, nsql|, |Parameter Size, 6B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.608|
|{|Model Type, Code Specific LLM|, |Model Name, nsql|, |Parameter Size, 6B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.277|
|{|Model Type, Code Specific LLM|, |Model Name, nsql|, |Parameter Size, 6B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.548|
|{|Model Type, Seq-to-Seq Model|, |Model Name, T5(tscholak/cxmefzzi)|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.828|       
|{|Model Type, Seq-to-Seq Model|, |Model Name, T5(tscholak/cxmefzzi)|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.782|       
|{|Model Type, Seq-to-Seq Model|, |Model Name, T5(tscholak/cxmefzzi)|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.650|       
|{|Model Type, Seq-to-Seq Model|, |Model Name, T5(tscholak/cxmefzzi)|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.434|       
|{|Model Type, Seq-to-Seq Model|, |Model Name, T5(tscholak/cxmefzzi)|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.641|     
|{|Model Type, Seq-to-Seq Model|, |Model Name, PICARD+T5|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.790|
|{|Model Type, Seq-to-Seq Model|, |Model Name, PICARD+T5|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.799|
|{|Model Type, Seq-to-Seq Model|, |Model Name, PICARD+T5|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.558|
|{|Model Type, Seq-to-Seq Model|, |Model Name, PICARD+T5|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.502|
|{|Model Type, Seq-to-Seq Model|, |Model Name, PICARD+T5|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.652|
|{|Model Type, Seq-to-Seq Model|, |Model Name, RESDSQL|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.872|
|{|Model Type, Seq-to-Seq Model|, |Model Name, RESDSQL|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.857|
|{|Model Type, Seq-to-Seq Model|, |Model Name, RESDSQL|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.666|
|{|Model Type, Seq-to-Seq Model|, |Model Name, RESDSQL|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.696|
|{|Model Type, Seq-to-Seq Model|, |Model Name, RESDSQL|, |Parameter Size, 3B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.775|
"""   
)

example2_short = ExtractionExample(
    table="""
| Model Type   | Model Name         | Parameter Size   | Level 1   | Level 2   | Level 3   | Level 4   | All   |
|:-------------|:-------------------|:-----------------|----------:|----------:|----------:|----------:|------:|
| General LLM  | ChatGPT-3.5-turbo  | 175B             |     0.760 |     0.799 |     0.408 |     0.493 | 0.623 |
""",
    
    caption="Table 1. Benchmark Results of Execution Match of all Models we tested on the 'dev' SPIDER dataset",
    
    references=["""
                In our experimentation, we organized the models into three distinct groups as illustrated in Table 1: general purpose LLMs, Code-Specific LLMs, and Sequence-to-Sequence models. Table 1 further presents the Execution Match score on the SPIDER dataset for each studied LLM and for each of the four difficulty levels.
                """],
    result="""
    |{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 1|}, Execution Match , 0.760|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 2|}, Execution Match , 0.799|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 3|}, Execution Match , 0.408|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, 4|}, Execution Match , 0.493|
|{|Model Type, General LLM|, |Model Name, ChatGPT-3.5-turbo|, |Parameter Size, 175B|, |Dataset, Spider dev|, |Difficulty Level, All|}, Execution Match , 0.623|
"""   
)

example_data_table = ExtractionExample(
    table="""
| Hyperparameter   | Value   | Hyperparameter   | Value   |
|:-----------------|:--------|:-----------------|:--------|
| Learning Rate    | 1e-4    | Epochs           | 5       |
""",
    caption="Table 3: Hyperparameter Settings",
    
    references=[""],
    result="""
    |{|Hyperparameter, Learning Rate|, |Value, 1e-4|}|
    |{|Hyperparameter, Epochs|, |Value, 5|}|
    ...
"""  
)

example_metric_column = ExtractionExample(
    table="""
| ('Dataset', 'Dataset')   | ('Metric (%)', 'Metric (%)')   |   ('Number of images', '50') |   ('Number of images', '100') |   ('Number of images', '150') |   ('Number of images', '200') | ('Number of images', '300')   | ('Number of images', '400')   | ('Number of images', '500')   | ('Number of images', '600')   |
|:-------------------------|:-------------------------------|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|:------------------------------|:------------------------------|:------------------------------|:------------------------------|
| Syn-only                 | AP@0.5                         |                         61.2 |                          69.3 |                          67.8 |                          77.7 | 79.6                          | 80.6                          | 76.5                          | 71.0                          |
| CP-only                  | AR@[0.5:0.95]                  |                         66.2 |                          69.8 |                          69.6 |                          71.4 | 72.9                          | 73.4                          | 71.0                          | 70.5                          |                     81.9 |                          82.9 | -                             | -                             | -                             | -                             |
""",

caption="TABLE II: Average precision and recall of instance segmentation algorithm with the Real-only, Syn-only, and CP-only datasets.",

references=[""],

result="""|{|Dataset, Syn-only|, |Number of images, 50|}, AP@0.5, 61.2|
|{|Dataset, Syn-only|, |Number of images, 100|}, AP@0.5, 69.3|
...
|{|Dataset, CP-only|, |Number of images, 50|}, AR@[0.5:0.95], 66.2|
|{|Dataset, CP-only|, |Number of images, 100|}, AR@[0.5:0.95], 69.8|
...
"""
)