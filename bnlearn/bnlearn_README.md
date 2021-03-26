# bnlearn README
This README accompanies the `bn_learn_test.R` script and `sepsis.csv` table.

## The Data
The `sepsis.csv` table contains 11 features but 2 of them are `subject_id` and `hadm_id` which are not entirely useful for this initial investigation. The other 9 features are binary variables, taken from [Martin et. al](https://www.nejm.org/doi/full/10.1056/NEJMoa022139), indicating whether a specific subject has been diagnosed with the following sepsis related comorbidites:

**Type of Organ Failure and Code — Description**

**Respiratory**

518.81 — Acute respiratory failure

518.82 — Acute respiratory distress syndrome

518.85 — Acute respiratory distress syndrome after shock or trauma

786.09 — Respiratory insufficiency

799.1 — Respiratory arrest

96.7 — Ventilator management

**Cardiovascular**

458.0 — Hypotension, postural

785.5 — Shock

785.51 — Shock, cardiogenic

785.59 — Shock, circulatory or septic

458.0 — Hypotension, postural

458.8 — Hypotension, specified type, not elsewhere classified

458.9 — Hypotension, arterial, constitutional

796.3 — Hypotension, transient

**Renal**

584 — Acute renal failure

580 — Acute glomerulonephritis

585 — Renal shutdown, unspecified

39.95 — Hemodialysis

**Hepatic**

570 — Acute hepatic failure or necrosis

572.2 — Hepatic encephalopathy

573.3 — Hepatitis, septic or unspecified

**Hematologic**

286.2 — Disseminated intravascular coagulation

286.6 — Purpura fulminans

286.9 — Coagulopathy

287.3-5 — Thrombocytopenia, primary, secondary, or unspecified

**Metabolic**

276.2 — Acidosis, metabolic or lactic

**Neurologic**

293 — Transient organic psychosis

348.1 — Anoxic brain injury

348.3 — Encephalopathy, acute

780.01 — Coma

780.09 — Altered consciousness, unspecified

89.14 — Electroencephalography

---
## The Script
It is likely you will first have to install the required packages to run the `bn_learn_test.R` script. 

This can be done by running the following statments in either the `R` console or in the actual script itself.

```
install.packages(bnlearn)
install.packages(Rgraphviz)
install.packages(dplyr)
```

If you experience problems installing Rgraphviz, try the following script:

```
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("Rgraphviz")
```
Another hiccup which may prevent the script from running is being in the wrong working direction. This can be fixed with the `setwd()` function in R.

Once all packages have been installed, the script can be ran by highlighting all lines you wish to run and hitting `Cmd/Ctrl + Enter`.

