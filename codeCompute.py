import re
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pypinyin import lazy_pinyin
from pyheatmap.heatmap import HeatMap


def apply_heatmap(image, data):
    # image: 原图  data: 识别得到的坐标结果.
    # 创建一个新的与原图大小一致的图像，背景(255, 255, 255)表示白色
    background = Image.new("RGB", (image.shape[1], image.shape[0]), (255, 255, 255))

    # 开始绘制热度图
    hm = HeatMap(data)
    # hm.heatmap(save_as="2.png")  # 热图
    # background：背景图片，r表示半径
    # 可以用于调节可视化效果，调节r即可调节热力点的半径大小
    hit_img = hm.heatmap(base=background, r=40)
    # hit_img 为 PIL Image格式
    # 将背景的Image格式转换成cv2格式
    hit_img = cv2.cvtColor(np.asarray(hit_img), cv2.COLOR_RGB2BGR)
    # print(image.shape)
    # print(hit_img.shape)
    overlay = image.copy()
    alpha = 0.5  # 设置覆盖图片的透明度
    # 设置红色为热度图基本色
    cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), (255, 0, 0), -1)
    # 将背景热度图覆盖到原图
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    # 将热度图覆盖到原图
    image = cv2.addWeighted(hit_img, alpha, image, 1 - alpha, 0)
    return image


my_file_path = '共产党宣言.txt'
save_file_path = '纯文本.txt'
_save_file_path = '拼音.txt'
# 预处理：只保留文本中的汉字
fd = open(my_file_path, 'r', encoding='utf-8')
cop = re.compile("[^\u4e00-\u9fa5^\n]")
for line in fd.readlines():
    string = cop.sub("", line)
    save_file = open(save_file_path, 'a', encoding='utf-8')
    save_file.write(string)
    save_file.flush()
    save_file.close()
fd.close()

# 将文本中的汉字转换为拼音
with open(save_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    string_list = lazy_pinyin(content)
    save_file = open(_save_file_path, 'a', encoding='utf-8')
    for index in range(len(string_list)):
        save_file.write(string_list[index])
        save_file.flush()
save_file.close()

# 计算文本中各字母出现频率
fr = open(_save_file_path, 'r', encoding='UTF-8')
# 读取文件所有行
content = fr.readlines()
letters = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'z', 'x', 'c', 'v', 'b', 'n', 'm']
rates = [0 for x in range(26)]
rate = dict(zip(letters, rates))  # 存放每个字出现的频率
print(rate)
# 依次迭代所有行
for line in content:
    # 统计每一字母出现的个数
    for x in range(0, len(line)):
        if line[x] not in rate and line[x] != '\n':
            rate[line[x]] = 0
        # 出现次数加一
        if line[x] != '\n':
            rate[line[x]] += 1

# print(rate)
# 将字典转换为列表
rate = sorted(rate.items(), key=lambda e: len(e), reverse=False)
print(rate)
sum = 0
for i in rate:
    sum += i[1]
'''
for i in rate:
    print("[", i[0], "] 出现频率 ", round(1000*i[1]/sum), "次")
'''
print('全文共有%d个字母' % sum)
print(rate[1][1])
fr.close()

# 绘制热力图
im = cv2.imread('alphabet.jpg', cv2.IMREAD_UNCHANGED)  # （高度，宽度，通道数）
print(im.shape)
# 输入的数据为形如 [[123, 234], [429, 82], [220, 535], ...]
# 这样的列表或元组，可以把它理解为一组平面坐标。
data = []

# 第一行
x1 = [49+64*xi for xi in range(10)]
y1 = [45 for yi in range(10)]
for i in range(0, 10):  # 第一行
    tmp = [int(x1[i]), int(y1[i])]
    for j in range(0, rate[i][1]):  # 第一行第i个j个
        data.append(tmp)
# print(data)
# 第二行
x2 = [80+64*xi for xi in range(9)]
y2 = [110 for yi in range(9)]
for i in range(0, 9):
    tmp = [int(x2[i]), int(y2[i])]
    for j in range(0, rate[i+10][1]):  # 第二行第i个j个
        data.append(tmp)

# 第三行
x3 = [110+64*xi for xi in range(7)]
y3 = [175 for yi in range(7)]
for i in range(0, 7):
    tmp = [int(x3[i]), int(y3[i])]
    for j in range(0, rate[i+19][1]):  # 第三行第i个j个
        data.append(tmp)

# print(data)
plt.imshow(apply_heatmap(im, data))
plt.show()
