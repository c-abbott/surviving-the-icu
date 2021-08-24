library(tidyverse) # data manipulation
library(ggplot2)   # plotting
library(ggtext)    # improve text in plot
library(patchwork) # stitching plots together
theme_set(theme_gray())

### Read in data
refuters_tbl <- read_csv('../output/refuters.csv')
refuters_tbl <- as_tibble(refuters_tbl)

refuters_tbl %>% 
    mutate(abs_dev = abs(delta_effect)) %>%
    group_by(dag) %>%
    summarise_at(vars(abs_dev), list(name=mean))