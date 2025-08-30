# 加载必要的包
library(ggplot2)
library(tidyr)
library(readr)

# 读取长格式的 CSV 文件，已经包含 Dataset, Time, Model, Value 四列
data_long <- read_csv("C:\\Users\\75695\\Desktop\\results\\time_series\\0.5.csv")

# 如果有空列，去除它们（保险起见）
data_long <- data_long[, colSums(is.na(data_long) | data_long == "") < nrow(data_long)]

# 画图：使用 facet_wrap 分出 4 个子图（按 Dataset）
p <- ggplot(data_long, aes(x = Time, y = Value, color = Model, group = Model)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  facet_wrap(~ Dataset, nrow = 1) +  # 每个 Dataset 一个子图，排成两行
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, by = 0.2)) +
  labs(title = "Segmentation Accuracy (t=0.5)",
       x = "Time Interval",
       y = "Segmentation Accuracy (t=0.5)") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "bottom",
    strip.text = element_text(face = "bold"),
    plot.title = element_text(hjust = 0.5)# 子图标题加粗
  )

# 保存图像
ggsave("plot1.png", plot = p, width = 12, height = 3, dpi = 300)