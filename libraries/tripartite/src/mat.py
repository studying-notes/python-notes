'''
Date: 2021-04-04 16:32:10
LastEditors: Rustle Karl
LastEditTime: 2021-04-04 16:32:10
'''
'''
Date: 2021.04.04 15:48
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.04.04 15:48
'''
import tkinter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tkinter.Tk()
root.title('图形')
root.geometry('630x700+100+100')
root.resizable(False, False)
tkinter.Label(root, anchor='w', text='随机游走的布朗运动').place(x=10, y=20, width=300, height=20)

# 第一个动画
# 使用 Label组件显示动画
lbFig1 = tkinter.Label(root)
lbFig1.place(x=10, y=40, width=300, height=300)
# c表示散点的数量
r, c = 2, 88
# 散点初始位置
positions = np.random.randint(-10, 10, (r, c))
# 每个散点的颜色,随机彩色
colors = np.random.random((c, 3))
fig, ax = plt.subplots()
scatters = ax.scatter(positions[0], positions[1], marker='*', s=60, c=colors)
canvas1 = FigureCanvasTkAgg(fig, master=lbFig1)
canvas1.get_tk_widget().pack(fill=tkinter.BOTH, expand=tkinter.YES)

ax.set_xlim(-40, 40)
ax.set_ylim(-40, 40)


def update(i):
    global positions

    # 随机游走,两个方向随机加减1,都限定在[-39,39]区间内
    positions = positions + np.random.choice((1, -1), (r, c))
    positions = np.where((positions > -39) & (positions < 39),
                         positions, np.sign(positions) * 39)

    # 更新散点位置
    scatters.set_offsets(positions.T)

    return scatters,


# 创建动画,100毫秒刷新一次
ani_scatters = FuncAnimation(fig, update, interval=100, blit=True)

# 第二个动画
tkinter.Label(root, anchor='w', text='闪烁的小星星').place(x=320, y=20, width=300, height=20)

lbFig2 = tkinter.Label(root)
lbFig2.place(x=320, y=40, width=300, height=300)

# 散点数量
N = 109
x = np.random.randint(10, 90, N)
y = np.random.randint(20, 90, N)
fig2, ax2 = plt.subplots()
scatters2 = ax2.scatter(x, y, marker='*', s=120)
canvas2 = FigureCanvasTkAgg(fig2, master=lbFig2)
canvas2.get_tk_widget().pack(fill=tkinter.BOTH, expand=tkinter.YES)


def update2(i):
    # 对散点符号的颜色、大小、边线颜色进行调整和变化
    scatters2.set_facecolor(np.random.random((N, 3)))
    scatters2.set_sizes(np.random.randint(50, 200, N))
    scatters.set_edgecolors(np.random.random((N, 3)))
    return scatters,


ani_scatters2 = FuncAnimation(fig2, update2, interval=300, blit=True)

# 第三个动画
tkinter.Label(root, anchor='w', text='随机折线图').place(x=10, y=360, width=300, height=20)
lbFig3 = tkinter.Label(root)
lbFig3.place(x=10, y=380, width=300, height=300)
fig3, ax3 = plt.subplots()
ax3.set_xlim(-10, 110)
ax3.set_ylim(10, 100)
x3, y3 = [], []
line, = ax3.plot(x3, y3)
canvas = FigureCanvasTkAgg(fig3, master=lbFig3)
canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=tkinter.YES)


def init():
    x3.clear()
    y3.clear()
    line.set_data(x3, y3)
    return line,


def update3(i):
    x3.append(i)
    y3.append(np.random.randint(30, 80))
    line.set_data(x3, y3)
    # 更新图形数据
    return line,


ani_line = FuncAnimation(fig=fig3, func=update3, frames=range(0, 100, 5), init_func=init, interval=500, blit=True)

# 第四个动画
tkinter.Label(root, anchor='w', text='动态柱状图').place(x=320, y=360, width=300, height=20)
lbFig4 = tkinter.Label(root)
lbFig4.place(x=320, y=380, width=300, height=300)

# 演示数据
data = {f'20{i:02d}': np.random.randint(30, 80, 12) for i in range(20)}

fig4, ax4 = plt.subplots()
ax4.set_yticks([])
ax4.set_yticklabels([])
canvas4 = FigureCanvasTkAgg(fig4, master=lbFig4)
canvas4.get_tk_widget().pack(fill=tkinter.BOTH, expand=tkinter.YES)


def init4():
    bars = ax4.barh(range(1, 13), data['2000'])
    return bars


def update4(year):
    ax4.cla()
    values = data[year]
    temp = sorted(zip(range(1, 13), values), key=lambda item: item[1])

    x = [item[0] for item in temp]
    y = [item[1] for item in temp]
    title = ax4.text(65, 1, str(year), fontproperties='simhei', fontsize=18)

    ax4.set_xlim(0, 100)
    bars = ax4.barh(range(1, 13), y)

    # 在水平柱状图右侧显示对应的数值,每个柱的左边显示月份
    texts = []
    for xx, yy in zip(range(1, 13), y):
        texts.append(ax4.text(yy + 0.1, xx - 0.1, str(yy)))
        texts.append(ax4.text(3, xx - 0.2, f'{x[xx - 1]}', fontproperties='simhei'))

    return list(bars) + [title] + texts


ani_bars = FuncAnimation(fig=fig4, init_func=init4, func=update4,
                         frames=data.keys(), interval=1000, blit=True)

root.mainloop()
