# Game Theoretic Analysis of Coalition Stability in Federated Learning

Federated Learning under voluntary participation, unlike settings where client participation is assumed, assumes data owners are rational clients who decide whether to join or remain outside a coalition to maximize their own utility. In this setting, participation is driven by a comparison between local and global accuracy.

In our game theoretic framework, a client’s utility is defined by the accuracy of its model:

- If a client joins a coalition, its utility equals the coalition’s global accuracy.  
- If a client does not join, its utility equals its local accuracy.

And, the stability of a client coalition is characterized as a Nash Equilibrium (NE), meaning that no client can improve its outcome by unilaterally changing its decision. Specifically, a coalition is an NE if:

- Clients outside the coalition have no incentive to join.  
- Clients inside the coalition have no incentive to leave.

This framework is used to analyze the stability of the grand coalition (where all clients participate) under different conditions, such as a complete information scenario, an incomplete information scenario, data heterogeneity among clients , and the inclusion of a communication cost term.

---


This is a living repository. Separate branches are created to maintain permanent code snapshots for each paper associated with this project.


## Associated Publications:

### MeditCom 2025  
**Evaluating Coalition Stability in Federated Learning Under Voluntary Client Participation**  


*[2025 IEEE International Mediterranean Conference on Communications and Networking (MeditCom)](https://ieeexplore.ieee.org/abstract/document/11104301)* 

**Branch**  
- 🔗 **[meditcom2025](https://github.com/abbaszal/FederatedLearning_NE/tree/meditcom2025)**

---

### WCNC 2026  
**Costs and Incentives for Data Owners to Participate in Federated Learning Seen Through Game Theory**  


*2026 IEEE Wireless Communications and Networking Conference (WCNC)*

**Branch**  
- 🔗 **[wcnc2026](https://github.com/abbaszal/FederatedLearning_NE/tree/wcnc2026)**

---

## Citations

To cite the **MeditCom 2025** project, use the following BibTeX entry:

```bibtex
@INPROCEEDINGS{11104301,
  author    = {Zal, Abbas and Marchioro, Thomas and Badia, Leonardo},
  booktitle = {2025 IEEE International Mediterranean Conference on Communications and Networking (MeditCom)},
  title     = {Evaluating Coalition Stability in Federated Learning Under Voluntary Client Participation},
  year      = {2025},
  organization = {IEEE}
}
````

To cite the **WCNC 2026** project , use the following BibTeX entry:


```bibtex
> To be published. will be added once available.
```

