# 加载必要的包
library(ggplot2)
library(tidyr)
library(readr)

# 读取长格式的 CSV 文件，已经包含 Dataset, Time, Model, Value 四列
data_long <- read_csv("C:\\Users\\75695\\Desktop\\results\\time_series\\ROI.csv")

# 如果有空列，去除它们（保险起见）
data_long <- data_long[, colSums(is.na(data_long) | data_long == "") < nrow(data_long)]


p1 <- ggplot(data_long, aes(x = ROI, y = Value, color = Metric, group = Metric)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  labs(title = "cho2\nn=72",
       x = "Training ROIs",
       y = "Accuracy") +
  scale_y_continuous(limits = c(0.5, 1), breaks = seq(0.5, 1, by = 0.1)) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(hjust = 0.5)  # 标题居中
  )
  

ggsave("plot1.png", plot = p1, width = 6, height = 5, dpi = 300)