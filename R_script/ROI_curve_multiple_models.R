# load necessary packages
library(ggplot2)
library(tidyr)
library(readr)

# read long format CSV file, already contains Dataset, Time, Model, Value four columns
data_long <- read_csv("C:\\Users\\75695\\Desktop\\results\\Hela\\Hela.csv")

# if there are empty columns, remove them (just in case)
data_long <- data_long[, colSums(is.na(data_long) | data_long == "") < nrow(data_long)]


# draw line chart and add error bars
p1 <- ggplot(data_long, aes(x = ROI, y = Value, color = Training_set, linetype = Metric, group = interaction(Training_set, Metric))) +
  geom_line(size = 1.2) +  # draw line
  geom_point(size = 2) +   # draw data points
  geom_errorbar(aes(ymin = Value - SD, ymax = Value + SD), width = 0.1) +  # add error bars
  labs(title = "Hela\nn=132",
       x = "Training ROIs",
       y = "Accuracy") +
  scale_y_continuous(limits = c(0.5, 1), breaks = seq(0.5, 1, by = 0.1)) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(hjust = 0.5)  # title in the center
  )



ggsave("plot2.png", plot = p1, width = 6, height = 5, dpi = 300)