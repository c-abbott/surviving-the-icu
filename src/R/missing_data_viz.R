library(tidyverse) # data manipulation
library(ggplot2)   # plotting
library(ggtext)
library(tidyquant)
library(forcats)

## Read in data
md_df <- as_tibble(read_csv('../output/tables/md_df.csv'))

## Pivot longer
md_df %>%
    ## Drop unnecessary columns
    select(c(2, 3, 4)) %>%
    ## Remove thickness_cleaned (not suitable for our project)
    filter(covariate != 'thickness_cleaned') %>%
    ## Pivot longer for plotting
    pivot_longer(
        cols=c('no_drain', 'drained'),
        names_to=c('treatment')
        ) %>%
    mutate(covariate=fct_reorder(covariate, value)) %>%
    ### Plot stacked bar chart
    ggplot(aes(fill=treatment, y=value, x=covariate)) + 
        geom_bar(position="stack", stat="identity") + 
        ## adjusting theme
        scale_fill_manual(
            name = NULL,
            values = c(drained="#0072B2", no_drain="#D55E00"),
            labels = c(
                drained = "<i style='color:#0072B2'>I. drained</i>",
                no_drain = "<i style='color:#D55E00'>I. no_drain</i>"
            )
        ) +
        theme_tq() + 
        theme(legend.position='none', 
            plot.title = element_markdown(face="bold", lineheight = 1.1, size=20),
            plot.subtitle = element_blank(),
            strip.text.x = element_blank(),
            axis.title.y = element_blank(),
            axis.title.x = element_blank(),
            axis.text.x = element_text(size=14),
            axis.text.y = element_text(size=14)
        ) + 
        labs(
            title = "**CSDH Missing Data**  
                <span style='font-size:16pt'>Missing data counts in the <span style='color:#D55E00;'>**no drain**</span> 
                and <span style='color:#0072B2;'>**drain**</span> treatment groups
                </span>"
        ) + 
        coord_flip() 

ggsave(paste0('../output/figs/', 'missing_data.png'), width=10, height=6)