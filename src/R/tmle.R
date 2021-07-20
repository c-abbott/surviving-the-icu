library(tidyverse) # for data manipulation
library(kableExtra) # for table printing
library(SuperLearner) # for ensemble learning
library(tmle) # for ate estimation
set.seed(100)

### Read in data
csdh <- read_csv('../../datasets/drain_data/csdh_final.csv')
csdh_burr <- read_csv('../../datasets/drain_data/csdh_burr.csv')

### Obtain naive estimate of ATE
bias_psi <- lm(data=csdh, recurrence ~ drain + thickness_sum + antiplatelet
               + drain*antiplatelet)
cat("\n")
cat("\n Naive_Biased_Psi:",summary(bias_psi)$coef[2, 1])

### Global vars
# data DAG confounders
data_confounders <- c('age', 'stroke', 'ihd', 'thickness_sum', 'hospital', 'platelet',
                     'antiplatelet', 'metalvalve', 'inr')
# doctor DAG confounders
doc_confounders <- c('age', 'stroke', 'ihd', 'metalvalve', 'antiplatelet', 'warfarin',
                    'thickness_sum', 'density', 'optype', 'hospital', 'membranes',
                    'bedrest', 'burrhole_num')
# confounders
W_min <- subset(csdh, select=c(age, thickness_sum, antiplatelet)) 
W_data <- subset(csdh, select=data_confounders)
W_doc <- subset(csdh_burr, select=doc_confounders)

# treatment and outcome
Y <- csdh$recurrence
Y_doc <- csdh_burr$recurrence
A <- csdh$drain 
A_doc <- csdh_burr$drain

# SuperLearner models
"SL.hal9001" <- hal9001::SL.hal9001 # scalable highly adaptive lasso (HAL)
sl_libs <- c("SL.glm", "SL.step", "SL.glm.interaction", "SL.earth", 
             "SL.ranger", "SL.xgboost", "SL.hal9001")

### Parametric ATE estimation with TMLE (min DAG)
tmle_min <- tmle(Y=Y, A=A, W=W_min)
cat("tmle_min_psi:", tmle_min$estimates[[2]][[1]],";", "95%CI(", tmle_min$estimates[[2]][[3]],")")

### Non-parametric ATE estimation with TMLE (min DAG)
sl_tmle_min <- tmle(Y=Y, A=A, W=W_min, family="binomial", V=5,
                    Q.SL.library = sl_libs,
                    g.SL.library = sl_libs)
cat("sl_tmle_min:", sl_tmle_min$estimates[[2]][[1]],";", "95%CI(", sl_tmle_min$estimates[[2]][[3]],")")

### Non-parametric ATE estimation (data DAG)
sl_tmle_data <- tmle(Y=Y, A=A, W=W_data, family="binomial", V=5,
                     Q.SL.library = sl_libs,
                     g.SL.library = sl_libs)
cat("sl_tmle_data:", sl_tmle_data$estimates[[2]][[1]],";", "95%CI(", sl_tmle_data$estimates[[2]][[3]],")")


### Non-parametric ATE estimation (doctor DAG)
sl_tmle_doc <- tmle(Y=Y_doc, A=A_doc, W=W_doc, family="binomial", V=5,
                    Q.SL.library = sl_libs,
                    g.SL.library = sl_libs)
cat("sl_tmle_doc:", sl_tmle_doc$estimates[[2]][[1]],";", "95%CI(", sl_tmle_doc$estimates[[2]][[3]],")")
