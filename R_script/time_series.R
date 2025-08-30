# 加载必要的包
library(ggplot2)
library(tidyr)
library(readxl)

# 读取 CSV 文件
data <- read_csv("C:\\Users\\75695\\Desktop\\results\\time_series\\cho1_5.csv")

data <- data[, colSums(is.na(data) | data == "") < nrow(data)]

# 将数据从宽格式转为长格式
data_long <- pivot_longer(data, 
                          cols = -Time, 
                          names_to = "Model", 
                          values_to = "Value")

# 画折线图
p1 <- ggplot(data_long, aes(x = Time, y = Value, color = Model, group = Model)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  labs(title = "cho1",
       x = "Time Interval",
       y = "Mean Segmentation Accuracy") +
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, by = 0.2)) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("cho1_plot.png", plot = p1, width = 8, height = 5, dpi = 300)