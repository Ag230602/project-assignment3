# Summary of Reproducibility Process

This assignment focused on converting an existing machine learning project into a reproducible research artifact and attempting to reproduce a related research repository. The goal was to ensure that the experiment pipeline can be executed reliably and that the engineering practices necessary for reproducible AI research are clearly documented.

## Reproducibility of Our Project

To make our project reproducible, we reorganized the repository structure and implemented several engineering practices. The project was configured so that the entire experiment pipeline can be executed using a single command through a reproducibility script (`reproduce.sh`). This script installs the required dependencies and runs a smoke test to verify that the environment and pipeline initialize correctly.

We created a pinned environment using a `requirements.txt` file to ensure consistent package versions across different systems. Controlling the software environment is essential because machine learning experiments are often sensitive to library versions and dependency conflicts.

We also implemented logging and artifact generation. All experiment outputs and logs are written to structured directories (`logs/` and `artifacts/`). This allows users to inspect experiment results and verify that the pipeline executed successfully.

A smoke test was added to confirm that the system can initialize the environment, load the dataset, and start the model execution without errors. The smoke test provides a lightweight validation of the pipeline before running full experiments.

## Reproduction of Related Work

For the related work reproduction task, we selected the RD-GCN repository available on GitHub. The goal was to reproduce the core execution pipeline of the repository.

During the reproduction process, several engineering challenges were encountered. The repository contained missing modules and incomplete dependency documentation. Several required modules such as `utils.timefeatures`, `utils.metrics`, `utils.tools`, and `utils.llm_explain` were referenced in the code but not included in the repository. These missing components prevented the pipeline from executing successfully.

To continue the reproduction attempt, placeholder implementations were created for these missing modules. These minimal implementations allowed the pipeline to progress further and enabled smoke-test level execution. In addition, several import issues were identified within the model package, where classes referenced in the experiment scripts were not properly exported. These issues required adjustments to the repository structure to allow the code to run.

This process demonstrated that reproducing research code often requires significant debugging and environment reconstruction due to missing dependencies or incomplete documentation.

## Lessons Learned

This reproduction exercise highlighted several key lessons about reproducible machine learning systems:

1. Research repositories often lack complete documentation and environment specifications, which can make reproduction difficult.
2. Missing dependencies and inconsistent module structures are common barriers to reproducibility.
3. Clear repository organization, dependency pinning, and deterministic execution practices are critical for reliable experiment replication.
4. Implementing smoke tests and structured logging significantly improves the robustness and usability of machine learning pipelines.

Overall, this assignment reinforced the importance of disciplined engineering practices when publishing machine learning research code. By organizing the repository, controlling the environment, and documenting the execution process, the project was transformed into a reproducible research artifact that can be executed and evaluated by other researchers.









## RD-GCN: Reaction–Diffusion Graph Neural Networks for Long-Horizon Multivariate Forecasting


##  Acknowledgment

We appreciate the following work for their valuable code and data for time-series forecasting:

- **[DFGCN](https://github.com/junjieyePhD/DFGCN/tree/main)** — Dynamic Fusion Graph Convolutional Network
- **[RevIN](https://github.com/ts-kim/RevIN)** - REVERSIBLE INSTANCE NORMALIZATION FOR ACCURATE TIME-SERIES FORECASTING AGAINST DISTRIBUTION SHIFT
