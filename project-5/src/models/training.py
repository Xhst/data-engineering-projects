import pandas as pd
from sklearn.model_selection import train_test_split
import os
import sys
import deepmatcher as dm
import nltk
import itertools

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###

#FastText Word Vectors (good for our task)
nltk.download('punkt_tab')


def load_and_split_data(dataset: str):
    
    # Load dataset
    file_path = dataset  
    df = pd.read_csv(file_path)

    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Labels -> int
    df['label'] = df['label'].astype(int)
    
    
    train_size = 0.7
    valid_size = 0.15
    test_size = 0.15

    valid_test_ratio = valid_size / (valid_size + test_size)

    
    train, valid_test = train_test_split(df, test_size=(1 - train_size), random_state=42)

    
    validation, test = train_test_split(valid_test, test_size=valid_test_ratio, random_state=42)

    
    print(f"{CYAN}Train size:{RESET} {len(train)}")
    print(f"{CYAN}Validation size:{RESET} {len(validation)}")
    print(f"{CYAN}Test size:{RESET} {len(test)}")

    data_splits_path = paths.MODELS.DATA_SPLITS.value

    if not os.path.exists(data_splits_path):
        os.makedirs(data_splits_path)

   
    train.to_csv(f"{data_splits_path}/train.csv", index=False)
    validation.to_csv(f"{data_splits_path}/validation.csv", index=False)
    test.to_csv(f"{data_splits_path}/test.csv", index=False)

    print(f"train.csv, validation.csv, test.csv {GREEN}Created{RESET}\n")


def train_dm(dataset: str):

    if not os.path.exists(paths.MODELS.DEEP_MATCHER.value):
        os.makedirs(paths.MODELS.DEEP_MATCHER.value)

    load_and_split_data(dataset)

    try:
        train, validation, test = dm.data.process(
            path=paths.MODELS.DATA_SPLITS.value,
            train='train.csv',
            validation='validation.csv',
            test='test.csv'
        )
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Grid search for hyperparameter tuning
    learning_rates = [0.00001, 0.0001, 0.001, 0.01]
    batch_sizes = [8, 16]
    epochs = [5, 10, 15]

    param_grid = list(itertools.product(learning_rates, batch_sizes, epochs))


    best_model = None
    best_f1 = 0
    best_params = None

    for lr, batch_size, num_epochs in param_grid:
        print(f"\n{RED}Testing params: LR={CYAN}{lr}{RED}, Batch Size={CYAN}{batch_size}{RED}, Epochs={CYAN}{num_epochs}{RESET}\n")
        
        # Model init
        model = dm.MatchingModel(attr_summarizer='hybrid') # Uses RNN and attention mechanism
        model.lr = lr

        model.run_train(
            train,
            validation,
            epochs=num_epochs,
            batch_size=batch_size,
            best_save_path=f"{paths.MODELS.DEEP_MATCHER.value}/pw_matching_DM_model_lr{lr}_bs_{batch_size}_epochs_{num_epochs}.pth"
        )
        
        # Best model on F1-score
        validation_f1 = model.run_eval(validation).item()
        print(f"{GREEN}Validation F1:{RESET} {validation_f1}")

        if validation_f1 > best_f1:
            best_f1 = validation_f1
            best_model = model
            best_params = (lr, batch_size, num_epochs)

    print(f"\n{CYAN}Best Model Params: LR={RESET}{best_params[0]}{CYAN}, Batch Size={RESET}{best_params[1]}{CYAN}, Epochs={RESET}{best_params[2]}\n")

    test_results = best_model.run_eval(test)

    f1 = test_results.item()
    with open(f"{paths.MODELS.DEEP_MATCHER.value}/best_model_info.txt", 'w') as file:
        file.write(f"=========Best Model Params:=========\n")
        file.write(f"- Learning rate: {best_params[0]}\n")
        file.write(f"- Batch Size: {best_params[1]}\n")
        file.write(f"- Epochs: {best_params[2]}\n")
        file.write(f"=========Best Model Performance (on test set):=========\n")
        file.write(f"- F1 Score: {f1}\n")
        file.write(f"- Precision:\n") # Taken from the logs
        file.write(f"- Recall:\n") # Taken from the logs

    print(f"{GREEN}Results saved on{RESET} 'best_model_metrics.txt'")


if __name__ == "__main__":

    print("sus")
    #train_dm(f"{paths.DATASET}/company_pairs.csv")
    #load_and_split_data(f"{paths.DATASET}/company_pairs.csv")