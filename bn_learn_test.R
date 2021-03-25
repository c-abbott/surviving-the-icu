# Import libs and set working directory
# setwd("/Users/callum/Uni/GitHubRepos/surviving-the-icu")
library(bnlearn)
library(dplyr)
library(Rgraphviz)


# Read in data as dataframe
sepsis = data.frame(read.csv('sepsis.csv'))
# Remove hadm and subject id
sepsis = subset(sepsis, select=c(-hadm_id, -subject_id))
# Convert int --> factor for bnlearn()
sepsis[1:9] = lapply(sepsis[1:9], factor)
# Create DAG using hill climbing search
sepsis_dag = hc(sepsis)
#graphviz.plot(sepsis_dag, shape="ellipse")

# Test strength of connections with bootstrapphing
dag_strength = boot.strength(sepsis, R = 200, algorithm = "hc")

dag_strength
attr(dag_strength, "threshold")

# Plotting averaged network from bootstrap samples
avg_sepsis_dag = averaged.network(dag_strength)
strength.plot(avg_sepsis_dag, dag_strength, shape = "ellipse")

# Obtaining CPT (I'm not sure if hill climbing search and mle are related)
bn.mle = bn.fit(sepsis_dag, data = sepsis, method = "mle")
bn.mle
