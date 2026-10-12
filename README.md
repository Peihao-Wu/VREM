# VREM — Virtual Rat Experimental Model

**Research code, data-processing workflows, model simulations, benchmarking, and analysis documentation**

VREM (Virtual Rat Experimental Model) is a computational research workflow for generating and evaluating virtual rat experimental measurements under drug exposure conditions. The supplied documentation describes multimodal compound representations, preparation of experimental datasets, a conditional generative architecture, checkpoint-based simulation, QSAR baseline comparisons, and downstream interpretation of drug-induced liver injury (DILI)-related results.

> **Scope:** This README documents the HTML reports and notebooks supplied with the project. The HTML files are **static, offline-readable research archives**, not executable training environments. They preserve code and saved outputs, but opening an HTML report does not rerun an experiment or independently validate the reported results.

## Documentation map

| Document                                                     | Contents                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`FeatureComput.html`](FeatureComput.html) | Nine feature engineering modules: QSAR, QSIIR, drugs/pathways, KEGG, GO biological process, GO cellular component, GO molecular function, data cleaning and export. |
| [`data_inspect_clean_split.html`](data_inspect_clean_split.html) | Nine notebooks (01–09): variable processing, dataset assembly, compound clustering, experimental analysis, heatmaps, key genes/enrichment, networks, and training-data splitting. |
| [`VREM.html`](VREM.html)                             | PyTorch model architecture and separate checkpoint-based drug simulation/testing source reference. |
| [`VREM_QSAR(basline models)_Training&Testing.html`](VREM_QSAR%28basline%20models%29_Training%26Testing.html) | Integrated VREM architecture/simulation and ten QSAR baseline / generated-data testing and evaluation notebooks (10–19). The filename retains the original spelling `basline` for compatibility. |
| [`Visualization.html`](Visualization.html)                   | Nine visualization and interpretation notebooks (22–30): survival/time-to-event analysis, model correlation, boxed-warning drugs, feature interpretation, tolcapone and nefazodone, MoME weights, DILI classification, and the 27-drug analysis. |
| [`extra.html`](Extra.html)                           | FDA reporting, drug safety labeling, and evidence-source visualizations from `26 FDA data.ipynb`. |

The `01 VREM.html` content is also represented within the integrated baseline report; these are alternative entry points rather than distinct model-training implementations. Numbered notebook identifiers reflect the source archive and are not a guarantee that every intermediate numbered notebook is included.

## Research workflow

```text
Compound-level inputs
  ├── QSAR chemical descriptors and fingerprints
  ├── QSIIR bioactivity-related representations
  └── PSMD / drug–pathway representations
                 │
                 ▼
Data inspection, cleaning, assembly and splitting
                 │
                 ▼
VREM multimodal model architecture
  └── Encoders → modality-aware mixture-of-experts → conditional generator
                 │
                 ▼
Checkpoint-based simulation by drug, time and dose
                 │
                 ├── QSAR baseline and generated-data evaluations
                 ├── DrugMatrix testing
                 ├── DILI classification and boxed-warning analyses
                 └── Feature, pathway and case-study interpretation
```

This diagram is a **documentation-level synthesis** of the supplied modules; it is not a claim that every step is connected by a single executable end-to-end script.

## Model and simulation details

The supplied architecture reference includes `RMSNorm`, `DiffSoftmax`, `RoutingNetwork`, `Discriminator`, `GeneratorNet`, `MoME_ModalRobust`, and `MBMMLAS`. The simulation reference uses PSMD, QSAR, and QSIIR feature matrices and loads saved model weights and training-derived scalers to generate 14 measurement endpoints:

`Neu`, `Eos`, `Bas`, `Mono`, `Lym`, `ALP`, `TBIL`, `RALB`, `A_G`, `AST`, `ALT`, `LDH`, `DBIL`, and `GTP`.

The simulation script specifies four time points (`4`, `8`, `15`, `29`) and three dose levels (`Low`, `Middle`, `High`), yielding **12 experimental conditions per compound**. It saves compound-level TSV predictions and configuration information. Simulation count is configurable: a reference to 100,000 simulations in comments or file naming should not be confused with the script's effective default setting.

**Important implementation distinction:** `mbmmlas_robust.py` is a network-definition file, **not a complete training pipeline**. The accompanying simulation script loads pretrained/finetuned checkpoints. Its default model import points to `models.mbmmlas`, so architectural identity with the separately supplied `mbmmlas_robust.py` cannot be assumed without checking the actual training repository and checkpoint configuration.

## Evaluation and interpretation

The documentation covers QSAR baseline model construction and testing; t-SNE/PCA visualizations; similarity/error comparisons including cosine similarity and RMSE; statistical analyses of baseline and generated results; and DrugMatrix testing. Subsequent visualizations address survival-related analysis, model correlations, boxed-warning drugs, DILI group comparisons, multimodal feature interpretation, routing weights, and case studies involving **tolcapone** and **nefazodone**.

The FDA supplementary report presents saved visualizations of adverse-event reporting, safety-label changes, and evidence-source distributions. These analyses should not be interpreted as proof of drug causality or as independently verified regulatory findings without reviewing their data provenance and methods.

## How to use the HTML reports

1. Download the relevant HTML file and open it in a current desktop browser (Chrome or Edge).
2. Use the sidebar or module tabs to select a notebook or source-code section.
3. Use search, code/output expansion, copy, and dark-mode controls where provided.
4. Inspect saved plots, tables, execution logs, and exceptions in the context of the corresponding code cell.
5. Use the original notebooks and Python scripts—not the static HTML—to reproduce or modify calculations.

The reports are intended to be self-contained for viewing. Data files, model weights, Python/R environments, and external services required for execution are **not** bundled into the HTML exports. Saved output is historical and may reflect environment-specific file paths or failed requests.

## Suggested repository organization

```text
VREM/
├── README.md
├── docs/
│   ├── FeatureComput_Complete_EN_v2.html
│   ├── data_inspect_clean_split.html
│   ├── 01 VREM.html
│   ├── VREM_QSAR(basline models)_Training&Testing.html
│   ├── Visualization.html
│   └── 05 extra.html
├── notebooks/            # Original .ipynb sources
├── models/               # Model definitions and training scripts, if supplied
├── scripts/              # Simulation and processing scripts, if supplied
├── configs/              # Reproducible run configurations, if supplied
└── data/                 # Documented paths or small examples only
```

This is a **proposed** organization, not a verified listing of the existing repository.

## Reproducibility checklist

- Record dataset versions, provenance, inclusion/exclusion criteria, and training/test partition identifiers.
- Pin Python/R and package versions, random seeds, model definitions, and checkpoint hashes.
- Preserve the fitted training scalers used during inference; avoid refitting on held-out or external-test data.
- Document dose and time encodings, simulation counts, batch size, stochastic inference behavior, and output schema.
- Distinguish original measurements, virtual samples, baseline predictions, and external validation sets.
- Report evaluation metrics, uncertainty, and the experimental unit used for train/test separation.
- Review saved notebook errors and incomplete outputs before using figures in publications.

## Data management and limitations

Large intermediate RDS files, raw mass-spectrometry data, and bulk prediction outputs should be kept in managed research storage rather than committed to Git history. A `.gitignore` prevents new untracked matches from being added, but does not remove files already committed.

The supplied documentation alone does not establish a complete executable training environment, current dependencies, source dataset licenses, checkpoint availability, or independent replication of scientific performance claims. Do not infer those details from the existence of saved plots.

## Citation and attribution

If you use this repository in a manuscript, cite the relevant VREM publication or preprint **once a verified bibliographic record is available**. Author list, DOI, license, and repository release/version should be added by project maintainers; they are not established by the supplied HTML reports.

---

*Documentation compiled from the supplied VREM HTML reports and their source notebooks. Last updated: 2026-10-12.*
