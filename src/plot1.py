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

df = pd.read_csv("results/lodo_estimator_results.csv")
df = df.rename(columns={"target_dataset": "dataset", "frequency_pred": "frequency_lodo"})
dfa = pd.read_csv("results/split_estimator_results.csv")
df["frequency_split"] = dfa["frequency_pred"]
df["dataset"] = df["dataset"].map(dataset_names)

for model in df["model"].unique():
    df_model = df[df["model"] == model]
    plt.figure(figsize=(4.5, 3))

    for i, n_clients in enumerate((10, 30, 100)):
        df_nc = df_model[df_model["n_clients"] == n_clients].groupby(
            "comm_cost"
        )[["frequency_true"]].mean().reset_index()
        plt.plot(
            df_nc["comm_cost"],
            df_nc["frequency_true"],
            marker="s",
            label=r"${\Psi}^{*}$",
            color=f"C{i}",
            mfc="none",
        )

    for i, n_clients in enumerate((10, 30, 100)):
        df_nc = df_model[df_model["n_clients"] == n_clients].groupby(
            "comm_cost"
        )[["frequency_split"]].mean().reset_index()
        plt.plot(
            df_nc["comm_cost"],
            df_nc["frequency_split"],
            "--",
            marker="^",
            label=r"$\hat{\Psi}_{SD}$",
            color=f"C{i}",
            alpha=0.7,
        )

    for i, n_clients in enumerate((10, 30, 100)):
        df_nc = df_model[df_model["n_clients"] == n_clients].groupby(
            "comm_cost"
        )[["frequency_lodo"]].mean().reset_index()
        plt.plot(
            df_nc["comm_cost"],
            df_nc["frequency_lodo"],
            "-.",
            marker="x",
            label=r"$\hat{\Psi}_{CD}," + f"N={n_clients}" + r"$",
            color=f"C{i}",
            alpha=0.5,
        )

    plt.xlabel(r"Communication cost $C$")
    plt.ylabel("Grand coalition frequency")
    plt.title(r"\tt{" + f"{model_names[model]}" + r"}")
    plt.legend(ncol=3)
    plt.grid(linestyle=":", alpha=0.7)
    if model == "fedfor":
        plt.ylim(-0.05, 1.25)
    elif model == "fedlr":
        plt.ylim(-0.05, 0.65)
    plt.tight_layout()
    plt.savefig(f"fig/{model}_frequency_vs_comm_cost.pdf")
    plt.show()
