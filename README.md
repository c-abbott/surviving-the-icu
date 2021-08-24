# To Drain or Not to Drain? A Causal Investigation into the Efficacy of Subdural Drains in Preventing CSDH Recurrence?
# Introduction
This Master's project has been conducted as part of the MSc in Statistics with Data Science at the University of Edinburgh under the supervision of Dr. Jacques Fleuriot. For medical expertise, Dr. Paul Brennan, a Professor and Honorary Consultant Neurosurgeon at the University of Edinburgh, along with Mr. Michael Poon, a neurosurgical trainee also at the University of Edinburgh, were regularly consulted throughout this project and were integral to its materialization.

# Project File Structure
This project consists of three main folders: `datasets`, `literature`, and `src`. 

## `literature`
This folder contains all the initial literature which inspired my Master's thesis to go down the route of causal inference. It is unlikely that anything here will be of interest when it comes to marking.
## `datasets`
This folder contains all iterations of the `csdh` dataset that was used for this causal investigation. There are multiple versions of this same dataset since the data had to be repeatedly updated following consultation with our medical expert collabortors. 

**The final and most important versions** are **`csdh_final`**, which was used for the minimum and data-driven causal models, and **`csdh_burr`** which was used for the expert causal model.
## `src`
The `src` folder contains all the source code used to conduct throughout this project and is stuctured as follows:
```
└── src
    ├── R
    │   ├── ate_viz.R
    │   ├── mean_deviation.R
    │   ├── missing_data_viz.R
    │   ├── refuters_viz.R
    │   ├── ridges.R
    │   └── tmle.R
    ├── causal_graphs
    │   ├── cate_dag.dot
    │   ├── data_dag.dot
    │   ├── doctor_dag.dot
    │   ├── min_dag.dot
    │   ├── mp_dag.dot
    │   ├── small_data_dag.dot
    │   └── treatment_dag.dot
    ├── helpers
    │   ├── __init__.py
    │   ├── dowhy_helpers.py
    │   └── meta_model_helpers.py
    ├── notebooks
    │   ├── associations.ipynb
    │   ├── cate_dml_estimators.ipynb
    │   ├── cate_estimation.ipynb
    │   ├── csdh.mplstyle
    │   ├── csdh_eda.ipynb
    │   ├── csdh_instrument_estimation.ipynb
    │   ├── csdh_propensity_estimation.ipynb
    │   ├── csdh_regression_estimation.ipynb
    │   ├── data_dag_meta_model_selection.ipynb
    │   ├── doc_dag_meta_model_selection.ipynb
    │   ├── html_notebooks
    │   │   ├── associations.html
    │   │   ├── cate_estimation.html
    │   │   ├── csdh_eda.html
    │   │   ├── csdh_propensity_estimation.html
    │   │   ├── csdh_regression_estimation.html
    │   │   └── doc_dag_meta_model_selection.html
    │   └── min_dag_meta_model_selection.ipynb
    └── output
        ├── figs
        │   ├── ate_ests.pdf
        │   ├── ate_ests.png
        │   ├── bootstrap_refuter.png
        │   ├── cate_dag.png
        │   ├── cate_tree.png
        │   ├── categorical_summary.png
        │   ├── csdh_dag.png
        │   ├── csdh_dag_indep_mediators.png
        │   ├── csdh_dag_no_mediators.png
        │   ├── days_burr.png
        │   ├── drain_ridges.png
        │   ├── dummy_refuter.png
        │   ├── missing_data.png
        │   ├── optype_ridges.png
        │   ├── patient_cate_tree.png
        │   ├── placebo_refuter.png
        │   ├── rcc_refuter.png
        │   ├── rec_burr.png
        │   ├── rec_drain.png
        │   ├── rec_duration.png
        │   ├── rec_mrs.png
        │   ├── rec_plate.png
        │   ├── recurrence_ridges.png
        │   ├── shunt.png
        │   ├── subset_refuter.png
        │   ├── summary_stats.png
        │   ├── surgeon_drain.png
        │   ├── thickness_no_0s.png
        │   ├── thickness_w_0s.png
        │   ├── tmle_ests.png
        │   └── treatment_cate_tree.png
        └── tables
            ├── ate_ests.csv
            ├── ate_ests.xlsx
            ├── bin_bin.csv
            ├── bin_cat.csv
            ├── bin_cont.csv
            ├── cat_cont.csv
            ├── cont_cont.csv
            ├── md_df.csv
            ├── refuters.csv
            └── refuters.xlsx
```

## `R`
This folder contains all `R` scripts which were used towards the back-end of the project primarily for producing figures i.e. `ate_viz`, `missing_data_viz`, `refuters_viz`, and `ridges`, but also conducting the targeted maximum likelihood estimation of the ATE (`tmle`), as well as for model robustness analysis (`mean_deviation`).

## `causal_graphs`
This folder contains all the plain text causal graph files which were necessary for specifying you causal model in a form that was understandable to the DoWhy causal inference framework.

## `helpers`
This folder contains two Python scripts, `dowhy_helpers.py` and `meta_model_helpers.py`, which provide a handful of helper functions which aided in tidying up the appearance of the Jupyter Notebooks used throughout this project by reducing the amount of repeated code. The `dowhy_helpers.py` script was used for the `csdh_propensity_estimation.ipynb` and `csdh_regression_estimation.ipynb` notebooks, meanwhile `meta_model_helpers.py` was used for `doc_dag_meta_model_selection.ipynb` and `cate_estimation.ipynb`.

## `notebooks`
This folder contains all the Jupyter Notebooks that were created throughout this project. For the ease of marking, the notebooks relevant to the final report produced have been rendered in `html` format and included in the `html_notebooks` folder. The details of each notebook are as follows:

- `associations` - contains all the associational calculations used to create the data-driven and expert causal models.
- `cate_estimation` - contains the pipeline which produced the double machine learning CATE trees specified in §5.4.2 of the final report using DoWhy and EconML.
- `csdh_eda` - contains the initial, unrefined EDA conducted on the `csdh` dataset. The final figures produced for the EDA section of the report were created using `ridges.R` in the `R` folder.
- `csdh_propensity_estimation` - contains all results produced for the propensity based estimators using DoWhy; from modelling to refutation.
- `csdh_regression_estimation` - contains all results produced for the regression based estimators using DoWhy; from modelling to refutation.
- `doc_meta_model_selection` - contains the model selection pipeline for the double machine learning CATE estimator used under the expert causal model. This is where you will find why the XGBClassifier was used.

The other notebooks which remain in `ipynb` format have been left as part of the submission as evidence of what else was investigated during the time of this project.

## `output`
This folder contains all the outputs produced throughout the project.