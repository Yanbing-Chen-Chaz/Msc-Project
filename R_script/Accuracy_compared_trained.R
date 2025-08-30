library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)
library(RColorBrewer)


# 读取两个 sheet（默认是第一个和第二个）
df1 <- read.csv("C:\\Users\\75695\\Desktop\\results\\cho2\\mean segmentation accuracy_t.csv", check.names = FALSE)
df2 <- read.csv("C:\\Users\\75695\\Desktop\\results\\cho2\\segmentation accuracy (t=0.5)_t.csv", check.names = FALSE)

# 将表格转换为长格式（算法名 + 值）
df1_long <- pivot_longer(df1, cols = everything(), names_to = "Method", values_to = "Accuracy")
df2_long <- pivot_longer(df2, cols = everything(), names_to = "Method", values_to = "Accuracy")

# 给类别生成数字索引
df1_long <- df1_long %>%
  mutate(Method_num = as.numeric(factor(Method))* 1.5)

# 给散点位置加偏移+抖动
set.seed(123)  # 固定随机数种子，方便复现
df1_long <- df1_long %>%
  mutate(
    jitter_x = Method_num + 0.5 + runif(n(), min = -0.1, max = 0.1)  # 右偏0.3，抖动±0.1
  )

df2_long <- df2_long %>%
  mutate(Method_num = as.numeric(factor(Method)) * 1.5) %>%
  mutate(jitter_x = Method_num + 0.5 + runif(n(), min = -0.1, max = 0.1))

# 颜色调色板
color_palette <- brewer.pal(n = length(unique(df1_long$Method)), name = "Set2")

# 主题风格
my_theme <- theme_bw(base_size = 14) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, color = "black", size = 12),
    axis.text.y = element_text(color = "black", size = 12),
    axis.title = element_text(size = 14, face = "plain"),
    plot.title = element_text(hjust = 0.5, size = 16, face = "plain"),
    legend.position = "none",
    
    # 去掉右侧边框，保留左侧和底部边框
    panel.border = element_blank(),
    
    # 横向网格线只保留y方向虚线
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "gray80", linetype = "dashed"),
    panel.grid.minor = element_blank(),
    
    # 左侧和底部实线边框（刻度线）
    axis.line.y = element_line(color = "black", size = 0.8),
    axis.ticks.y = element_line(color = "black", size = 0.8),
    axis.line.x = element_line(color = "black", size = 0.8),
    axis.ticks.x = element_line(color = "black", size = 0.8),
    
    axis.ticks.length = unit(0.25, "cm")
  )

# 画图
p1 <- ggplot(df1_long, aes(x = Method_num, y = Accuracy, fill = Method)) +
  geom_violin(trim = TRUE, alpha = 0.3, color = NA, adjust = 2, width = 0.4) +
  geom_boxplot(
    aes(color = Method, fill = Method),
    width = 0.12,
    outlier.size = 0.7,
    alpha = 0.5,
    size = 0.8
  ) +
  geom_point(
    data = df1_long,
    aes(x = jitter_x, y = Accuracy, color = Method),
    size = 1.8,
    alpha = 0.7,
    shape = 16,
    inherit.aes = FALSE
  ) +
  scale_x_continuous(
    breaks = unique(df1_long$Method_num),
    labels = unique(df1_long$Method),
    expand = expansion(add = c(0.5, 0.3))
  ) +
  scale_y_continuous(
    breaks = seq(0, 1, by = 0.2),  # y轴刻度 0.1 单位
    limits = c(0, 1.115)               # 这里可根据实际数据调整
  ) +
  scale_fill_manual(values = color_palette) +
  scale_color_manual(values = color_palette) +
  labs(
    title = "cho2\nn=72",
    x = " ",
    y = "Mean Segmentation Accuracy"
  ) +
  my_theme +
  theme(plot.margin = margin(10, 40, 10, 10)) +
  
  # 顶部虚线
  geom_hline(yintercept = 1, color = "gray80", linetype = "dashed", size = 0.8)

method1 <- "cellpose-SAM"
method2 <- "cellpose-SAM(trained)"
method3 <- "cellpose cyto3"
method4 <- "cellpose cyto3(trained)"

vec1 <- df1[[method1]]
vec2 <- df1[[method2]]
vec3 <- df1[[method3]]
vec4 <- df1[[method4]]

# Wilcoxon signed-rank test
test_result1 <- wilcox.test(vec1, vec2, paired = TRUE)
test_result2 <- wilcox.test(vec3, vec4, paired = TRUE)

p_val1 <- test_result1$p.value
p_val2 <- test_result2$p.value


# 转为星号
get_sig_label <- function(p) {
  if (p <= 0.001) return("***")
  else if (p <= 0.01) return("**")
  else if (p <= 0.05) return("*")
  else return("ns")
}
p_label1 <- get_sig_label(p_val1)
p_label2 <- get_sig_label(p_val2)


# 手动标注线 + 星号
p1 <- p1 +
  annotate("segment", x = 1.5, xend = 3.0, y = 1.06, yend = 1.06, size = 0.8) +
  annotate("text", x = (1.5 + 3.0) / 2, y = 1.09, label = p_label1, size = 5) +
  annotate("segment", x = 4.5, xend = 6.0, y = 1.06, yend = 1.06, size = 0.8) +
  annotate("text", x = (4.5 + 6.0) / 2, y = 1.09, label = p_label2, size = 5) 

print(p1)
ggsave("plot1.png", plot = p1, width = 5, height = 7)

p2 <- ggplot(df2_long, aes(x = Method_num, y = Accuracy, fill = Method)) +
  geom_violin(trim = TRUE, alpha = 0.3, color = NA, adjust = 2, width = 0.4) +
  geom_boxplot(
    aes(color = Method, fill = Method),
    width = 0.12,
    outlier.size = 0.7,
    alpha = 0.5,
    size = 0.8
  ) +
  geom_point(
    aes(x = jitter_x, y = Accuracy, color = Method),
    size = 1.8,
    alpha = 0.7,
    shape = 16,
    inherit.aes = FALSE
  ) +
  scale_x_continuous(
    breaks = unique(df2_long$Method_num),
    labels = unique(df2_long$Method),
    expand = expansion(add = c(0.5, 0.3))
  ) +
  scale_y_continuous(
    breaks = seq(0, 1, by = 0.2),  # y轴刻度0.2单位
    limits = c(0, 1.115)
  ) +
  scale_fill_manual(values = color_palette) +
  scale_color_manual(values = color_palette) +
  labs(
    title = "cho2\nn=72",
    x = " ",
    y = "Segmentation Accuracy (t=0.5)"
  ) +
  my_theme +
  theme(plot.margin = margin(10, 40, 10, 10)) +
  
  # 顶部虚线
  geom_hline(yintercept = 1, color = "gray80", linetype = "dashed", size = 0.8)

vec21 <- df2[[method1]]
vec22 <- df2[[method2]]
vec23 <- df2[[method3]]
vec24 <- df2[[method4]]

# Wilcoxon signed-rank test
test_result21 <- wilcox.test(vec21, vec22, paired = TRUE)
test_result22 <- wilcox.test(vec23, vec24, paired = TRUE)

p_val21 <- test_result21$p.value
p_val22 <- test_result22$p.value


# 转为星号

p_label21 <- get_sig_label(p_val21)
p_label22 <- get_sig_label(p_val22)


# 手动标注线 + 星号
p2 <- p2 +
  annotate("segment", x = 1.5, xend = 3.0, y = 1.06, yend = 1.06, size = 0.8) +
  annotate("text", x = (1.5 + 3.0) / 2, y = 1.09, label = p_label21, size = 5) +
  annotate("segment", x = 4.5, xend = 6.0, y = 1.06, yend = 1.06, size = 0.8) +
  annotate("text", x = (4.5 + 6.0) / 2, y = 1.09, label = p_label22, size = 5) 

print(p2)

ggsave("plot2.png", plot = p2, width = 5, height = 7)
