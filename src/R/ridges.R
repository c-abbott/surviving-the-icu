library(tidyverse) # data manipulation
library(ggplot2)   # plotting
library(ggtext)
library(tidyquant)

### Read in data
csdh <- as_tibble(read_csv('../../datasets/drain_data/csdh_final.csv'))

### Convert numeric vars into to factor variable
csdh$optype <- as.factor(csdh$optype)
csdh$drain <- as.factor(csdh$drain)
csdh$recurrence <- as.factor(csdh$recurrence)


### Create plotting function
plot_dist <- function(data, x, y, fill){
    p <- ggplot(data, aes(x=x, y=y, fill=fill)) +
        ggdist::stat_halfeye(
            adjust = .5, 
            width = .6, 
            .width = 0, 
            justification = -.2, 
            point_colour = NA,
        ) + 
        geom_boxplot(
            width = .15, 
            outlier.shape = NA,
            alpha = .5
        ) +
        ## add justified jitter from the {gghalves} package
        gghalves::geom_half_point(
            aes(color=fill),
            ## draw jitter on the left
            side = "l", 
            ## control range of jitter
            range_scale = .4, 
            ## add some transparency
            alpha = .3
        ) +
        theme_tq() + 
        theme(legend.position='none', 
              plot.title = element_markdown(face="bold", lineheight = 1.1, size=20),
              plot.subtitle = element_markdown(lineheight = 1.1, size=16),
              strip.text.x = element_blank(),
              axis.title.y = element_text(vjust = 0, size = 14),
              axis.title.x = element_blank(),
              axis.text.x = element_text(size=14),
              axis.text.y = element_text(size=12)
        )
    return(p)
}

plot_dist(data=csdh, x=csdh$optype, y=csdh$thickness_sum, fill=csdh$optype) + 
    scale_fill_tq() + 
    scale_color_tq() +
    scale_x_discrete(labels=c('BHC', 'Craniotomy', 'Other'), limits=c(1, 2, 3)) + 
    labs(
        title = 'CSDH Operation Types',
        subtitle = 'Distributions of hematoma thickness by operation type',
        y = 'Hematoma Thickness (mm)'
        ) + 
    coord_cartesian(xlim = c(1.2, 3.1), clip = "off")
ggsave(paste0('../output/figs/', 'optype_ridges.png'), width=8, height=6)

plot_dist(data=csdh, x=csdh$drain, y=csdh$thickness_sum, fill=csdh$drain) + 
    scale_fill_tq() + 
    scale_color_tq() +
    scale_x_discrete(labels=c('No Drain', 'Drain')) + 
    labs(
        title = 'CSDH Treatment Assignment',
        subtitle = 'Distributions of hematoma thickness by treatment assignment',
        y = 'Hematoma Thickness (mm)'
    )
ggsave(paste0('../output/figs/', 'drain_ridges.png'), width=8, height=6)

plot_dist(data=csdh, x=csdh$recurrence, y=csdh$thickness_sum, fill=csdh$recurrence) + 
    scale_fill_tq() + 
    scale_color_tq() +
    scale_x_discrete(labels=c('No Recurrence', 'Recurrence')) + 
    labs(
        title = 'CSDH Recurrence',
        subtitle = 'Distributions of hematoma thickness by recurrence',
        y = 'Hematoma Thickness (mm)'
    )
    
ggsave(paste0('../output/figs/', 'recurrence_ridges.png'), width=8, height=6)