import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
})

plt.style.use(["seaborn-v0_8-colorblind"])

model_names = {
    "fedlr": "FedLR",
    "fedfor": "FedFor",
}

dataset_names = {
    "adult": "Adult",
    "huga": "HuGaDB",
    "kdd": "KDD99",
    "spambase": "Spambase",
}

parser = argparse.ArgumentParser()
parser.add_argument("--cc", type=float, required=True)
parser.add_argument("--nc", type=int, required=True)
args = parser.parse_args()

comm_cost = args.cc
n_clients = args.nc

df = pd.read_csv("results/lodo_estimator_results.csv")
df = df.rename(columns={"target_dataset": "dataset", "frequency_pred": "frequency_lodo"})
dfa = pd.read_csv("results/split_estimator_results.csv")
df["frequency_split"] = dfa["frequency_pred"]
df["dataset"] = df["dataset"].map(dataset_names)

df_ = df[(df["comm_cost"] == comm_cost) & (df["n_clients"] == n_clients)].reset_index(drop=True)

for model in df_["model"].unique():
    plt.figure(figsize=(4.5, 2))

    dfx = (
        df_[df_["model"] == model]
        .groupby("dataset")[["frequency_true", "frequency_split", "frequency_lodo"]]
        .mean()
        .reset_index()
    )

    ax = dfx.plot(
        x="dataset",
        y=["frequency_true", "frequency_split", "frequency_lodo"],
        kind="bar",
        ax=plt.gca(),
        rot=0,
        label=[r"${\Psi}^{*}$", r"$\hat{\Psi}_{SD}$", r"$\hat{\Psi}_{CD}$"],
        color=["C0", "C1", "C4"],
        alpha=0.7,
        edgecolor="black",
    )

    bars = ax.patches
    hatches = "".join(h * len(dfx) for h in "*xo")

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    plt.title(r"\tt{" + f"{model_names[model]}" + r"}" + f" $(N={n_clients}$, $C={comm_cost})$")
    plt.xlabel("")
    plt.ylim(0, 1.2)
    plt.legend(fontsize=8)
    plt.ylabel("Grand coalition frequency")
    plt.grid(axis="y", linestyle=":", alpha=0.7)
    plt.tight_layout()

    pretty_comm_cost = f"{comm_cost:.4f}".replace(".", "_")
    plt.savefig(f"fig/{model}_frequency_barplot_{pretty_comm_cost}.pdf")
    plt.show()
