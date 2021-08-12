library(tidyverse) # data manipulation
library(ggplot2)   # plotting
library(ggtext)    # improve text in plot
theme_set(theme_gray())

### Read in data
ests_tbl <- read_csv('../output/ate_ests.csv')
ests_tbl <- as_tibble(ests_tbl)

### Remove NAs for plotting
ests_tbl$p_val <- as.numeric(ests_tbl$p_val)
ests_tbl <- ests_tbl %>% replace(is.na(.), 0)

### Order DAG column
ests_tbl$dag <- factor(ests_tbl$dag, levels=c('min', 'data', 'doc'))

### Define new tibble tfor plotting naive vlin
naive_ests <- tibble(dag=c('min', 'data', 'doc'), 
                     est=c(-0.0936, -0.0936,  -0.0837))
naive_ests$dag <- factor(naive_ests$dag, levels=c('min', 'data', 'doc'))

## PLOTTING PARAMETRIC ATE ESTIMATES
p <- ggplot(ests_tbl, aes(x=method, y=ate, color=dag)) + 
        geom_point(size=4) + 
        geom_errorbar(data=subset(ests_tbl, method!='naive'),
                      aes(ymin=ci_lb, ymax=ci_ub), width=.25, size=1.25) + 
        ## Create facet grid for each DAG
        facet_grid(.~dag) + 
        ## Use font colours as legend
        scale_color_manual(
            name = NULL,
            values = c(min="#0072B2", data="#009E73", doc="#D55E00"),
            labels = c(
                min = "<i style='color:#0072B2'>I. min</i>",
                data = "<i style='color:#009E73'>I. data</i>",
                doc = "<i style='color:#D55E00'>I. doc</i>")
        ) +
        ## Remove IV from plot (ruins scale)
        scale_x_discrete(labels=c('PSS', 'PSM', 'IPW',
                                  'GLM', 'LR', 'Naive'),
                         limits=c('ps_strat', 'ps_match', 'ipw',
                                  'glm', 'lin_reg', 'naive')) + 
        ## Rescaling numerical axis
        scale_y_continuous(limits=c(-0.23, 0.015)) +
        labs(title = "**ATE Estimation**  
                <span style='font-size:18pt'>ATE estimates for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>", 
             x='Estimation Method', y='ATE') + 
        theme(legend.position='none', 
              plot.title = element_markdown(lineheight = 1.1, size=30),
              strip.text.x = element_blank(),
              axis.title.x = element_text(face="bold", vjust = 0, size = 20),
              axis.title.y = element_blank(),
              axis.text.x = element_text(size=16),
              axis.text.y = element_text(size=16),
              plot.margin = margin(t = 25, r = 35, b = 10, l = 15)) + 
        coord_flip()
## Add vline for naive est comparison
p <- p + geom_hline(aes(yintercept=est, color=dag), naive_ests, 
               linetype=5, size=1, alpha=.5)

p
## Saving fig as pdf and png
ggsave("../output/figs/ate_ests.png", width=12, height=8)


## PLOTTING TMLE AETE ESTIMATE
g <- ggplot(ests_tbl, aes(x=method, y=ate, color=dag)) + 
    geom_point(size=4) + 
    geom_errorbar(data=subset(ests_tbl, method!='naive'),
                  aes(ymin=ci_lb, ymax=ci_ub), width=.25, size=1.25) + 
    ## Create facet grid for each DAG
    facet_grid(.~dag) + 
    ## Use font colours as legend
    scale_color_manual(
        name = NULL,
        values = c(min="#0072B2", data="#009E73", doc="#D55E00"),
        labels = c(
            min = "<i style='color:#0072B2'>I. min</i>",
            data = "<i style='color:#009E73'>I. data</i>",
            doc = "<i style='color:#D55E00'>I. doc</i>")
    ) +
    ## Remove IV from plot (ruins scale)
    scale_x_discrete(labels=c('TMLE', 'Naive'),
                     limits=c('tmle', 'naive')) + 
    ## Rescaling numerical axis
    scale_y_continuous(limits=c(-0.23, 0.015)) +
    labs(title = "**TMLE ATE Estimation**  
                <span style='font-size:18pt'>TMLE ATE estimates for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>", 
         x='Estimation Method', y='ATE') + 
    theme(legend.position='none', 
          plot.title = element_markdown(lineheight = 1.1, size=30),
          strip.text.x = element_blank(),
          axis.title.x = element_text(face="bold", vjust = 0, size = 20),
          axis.title.y = element_blank(),
          axis.text.x = element_text(size=16),
          axis.text.y = element_text(size=16),
          plot.margin = margin(t = 25, r = 35, b = 10, l = 15)) + 
    coord_flip()
## Add vline for naive est comparison
g <- g + geom_hline(aes(yintercept=est, color=dag), naive_ests, 
                    linetype=5, size=1, alpha=.5)
g
## Saving fig as pdf and png
ggsave("../output/figs/tmle_ests.png", width=12, height=4)





