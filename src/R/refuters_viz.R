library(tidyverse) # data manipulation
library(ggplot2)   # plotting
library(ggtext)    # improve text in plot
library(patchwork) # stitching plots together
theme_set(theme_gray())

### Read in data
refuters_tbl <- read_csv('../output/refuters.csv')
refuters_tbl <- as_tibble(refuters_tbl)

### Remove IV data
refuters_tbl <- subset(refuters_tbl, method != 'iv')

### Relabel methods
refuters_tbl <- refuters_tbl %>% replace(.=='lin_reg', 'LR') %>%
    replace(.=='glm', 'GLM') %>% replace(.=='ipw', 'IPW') %>%
    replace(.=='ps_match', 'PSM') %>% replace(.=='ps_strat', 'PSS') %>%
    replace(.=='doc', 'exp')


### Create new method column
refuters_tbl <- refuters_tbl %>% mutate(model_method = paste0(dag, '_', method))  %>%
### Round deviation column to 4 decimal places
    mutate(across(7, round, 4))

### Filter by refuter type
rcc_tbl <- refuters_tbl %>% filter(refuter == 'random_common_cause')
placebo_tbl <- refuters_tbl %>% filter(refuter == 'placebo_treatment')
dummy_tbl <- refuters_tbl %>% filter(refuter == 'dummy_outcome')
subset_tbl <- refuters_tbl %>% filter(refuter == 'subset')
bootstrap_tbl <- refuters_tbl %>% filter(refuter == 'bootstrap')



plot_refuter <- function(dataframe, title, filename){
    p <- ggplot(dataframe, aes(x=model_method, y=delta_effect, 
                             label=delta_effect, color=dag)) + 
        geom_point(stat='identity', size=24) + 
        geom_segment(aes(y = 0, 
                         x = model_method, 
                         yend = delta_effect, 
                         xend = model_method),
                     size=2) +
        scale_color_manual(
            name = NULL,
            values = c(min="#0072B2", data="#009E73", exp="#D55E00"),
            labels = c(
                min = "<i style='color:#0072B2'>I. min</i>",
                data = "<i style='color:#009E73'>I. data</i>",
                exp = "<i style='color:#D55E00'>I. exp</i>")
        ) +
        geom_text(color="white", size=5) +
        labs(title=title, 
             y='Deviation') + 
        theme(legend.position='none', 
              plot.title = element_markdown(lineheight = 1.1, size=30),
              strip.text.x = element_blank(),
              axis.title.x = element_text(face="bold", vjust = 0, size = 20),
              axis.title.y = element_blank(),
              axis.text.x = element_text(size=16),
              axis.text.y = element_text(size=16),
              plot.margin = margin(t = 25, r = 35, b = 10, l = 15)) + 
        coord_flip()
    ggsave(paste0('../output/figs/', filename), width=12, height=12)
}

plot_refuter(dataframe=rcc_tbl,
             title = "**Random Common Cause (RCC) Refuter**  
                <span style='font-size:18pt'>RCC deviations for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>",
             filename='rcc_refuter.png')

plot_refuter(dataframe=placebo_tbl,
             title = "**Placebo Treatment (PT) Refuter**  
                <span style='font-size:18pt'>PT deviations for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>",
             filename='placebo_refuter.png')

plot_refuter(dataframe=dummy_tbl,
             title = "**Dummy Outcome Refuter**  
                <span style='font-size:18pt'>Dummy outcome deviations for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>",
             filename='dummy_refuter.png')

plot_refuter(dataframe=subset_tbl,
             title = "**Data Subset (DS) Refuter**  
                <span style='font-size:18pt'>DS deviations for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>",
             filename='subset_refuter.png')

plot_refuter(dataframe=bootstrap_tbl,
             title = "**Bootstrap Refuter**  
                <span style='font-size:18pt'>Bootstrap deviations for the 
                <span style='color:#0072B2;'>**minimum**</span>, 
                <span style='color:#009E73;'>**data-driven**</span>, and
                <span style='color:#D55E00;'>**expert**</span> causal models
                </span>",
             filename='bootstrap_refuter.png')

