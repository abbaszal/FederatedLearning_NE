import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

dataset_names = {
    "adult": "Adult",
    "huga": "HuGaDB",
    "kdd": "KDD99",
    "spambase": "Spambase",
}

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["lodo", "split"])
args = parser.parse_args()

results = []

for model in ("fedlr", "fedfor"):
    for n_clients in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
        dfs = {}
        for dataset in dataset_names.keys():
            dft = pd.read_csv(f"history/{n_clients}_clients_{dataset}_{model}.csv")
            df = dft[[f"Client {i+1} Accuracy" for i in range(n_clients)]].T.describe(
                percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]
            ).loc[["min", "10%", "25%", "50%", "75%", "90%", "max"]].T
            df["n_clients"] = n_clients
            df["global"] = dft["Global Accuracy"]
            dfs[dataset] = df

        for comm_cost in (0.0, 0.0125, 0.025, 0.05, 0.1):
            for target_dataset in dataset_names.keys():
                for dataset in dataset_names.keys():
                    dfs[dataset]["ground_truth"] = dfs[dataset].apply(
                        lambda row: 1 * (row["global"] > row["max"] + comm_cost), axis=1
                    )

                if args.mode == "lodo":
                    X_train = pd.DataFrame()
                    y_train = pd.Series(dtype=int)
                    for dataset in dataset_names.keys():
                        if dataset != target_dataset:
                            X_train = pd.concat(
                                [X_train, dfs[dataset].drop(columns=["ground_truth", "global"])],
                                ignore_index=True,
                            )
                            y_train = pd.concat(
                                [y_train, dfs[dataset]["ground_truth"]], ignore_index=True
                            )
                        else:
                            X_test = dfs[dataset].drop(columns=["ground_truth", "global"])
                            y_test = dfs[dataset]["ground_truth"]

                if args.mode == "split":
                    X = dfs[target_dataset].drop(columns=["ground_truth", "global"])
                    y = dfs[target_dataset]["ground_truth"]
                    nsplit = int(len(X) / 2)
                    X_train = X.iloc[:nsplit, :].reset_index(drop=True)
                    y_train = y.iloc[:nsplit].reset_index(drop=True)
                    X_test = X.iloc[nsplit:, :].reset_index(drop=True)
                    y_test = y.iloc[nsplit:].reset_index(drop=True)

                if len(y_train.unique()) < 2:
                    if y_train.unique()[0] == 0:
                        y_pred = np.zeros_like(y_test)
                    else:
                        y_pred = np.ones_like(y_test)
                else:
                    est = RandomForestClassifier(n_estimators=100, random_state=42)
                    est.fit(X_train, y_train)
                    y_pred = est.predict(X_test)

                results.append({
                    "model": model,
                    "n_clients": n_clients,
                    "comm_cost": comm_cost,
                    "target_dataset": target_dataset,
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, zero_division=0),
                    "recall": recall_score(y_test, y_pred, zero_division=0),
                    "f1_score": f1_score(y_test, y_pred, zero_division=0),
                    "frequency_true": np.mean(y_test),
                    "frequency_pred": np.mean(y_pred),
                })



                #print(f"Completed: model={model}, n_clients={n_clients}, comm_cost={comm_cost}, target_dataset={target_dataset}")
                #print(f"  Accuracy: {results[-1]['accuracy']:.4f}, Precision: {results[-1]['precision']:.4f}, Recall: {results[-1]['recall']:.4f}, F1-score: {results[-1]['f1_score']:.4f}")
                #print(f"Frequency True: {results[-1]['frequency_true']:.4f}, Frequency Pred: {results[-1]['frequency_pred']:.4f}")

                out = "results/lodo_estimator_results.csv" if args.mode == "lodo" else "results/split_estimator_results.csv"
                pd.DataFrame(results).to_csv(out, index=False)
