import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import numpy as np
import random


# 初始位置生成
def initial_room():
    '''
    生成初始人员并进行随机分配
    '''
    coordinates = []  # 室内人员坐标
    for i in range(N):
        generated_data = [random.randint(1, row), random.randint(1, column)]
        if not generated_data in coordinates:  # 去掉重复数据
            coordinates.append(generated_data)
    for i in range(len(coordinates)):
        room[coordinates[i][0]][coordinates[i][1]] = 1
    # 创建围墙、创建出口
    for i in range(len(room)):
        for j in range(len(room)):
            if i == 0 or i == len(room) - 1 or j == 0 or j == len(room[i]) - 1:
                room[i][j] = 9
    for i in range(len(export)):
        room[export[i][1]][export[i][0]] = 8
    return


# 创建平台
def create_flat():
    # fig, ax = plt.subplots()
    plt.xticks(np.arange(0, column + 3, 1.0))
    plt.yticks(np.arange(0, row + 3, 1.0))
    plt.grid(linestyle='--')
    wall_botton = mpathes.Rectangle((0, 0), column + 2, 1, color='grey')
    wall_left = mpathes.Rectangle((0, 0), 1, row + 2, color='grey')
    wall_top = mpathes.Rectangle((0, row + 1), column + 2, 1, color='grey')
    wall_right = mpathes.Rectangle((column + 1, 0), 1, row + 2, color='grey')
    ax.add_patch(wall_botton)
    ax.add_patch(wall_top)
    ax.add_patch(wall_left)
    ax.add_patch(wall_right)
    for i in range(len(export)):
        ax.add_patch(mpathes.Rectangle((export[i][0], export[i][1]), 1, 1, color='green'))


# 更新状态
def update_state():
    '''
    搜寻距离出口同一层的人，记录坐标
    :return:
    '''
    # 记录坐标
    tem=[]
    for i in range(len(export)):
        tem.append(column-export[i][0])
        tem.append(row-export[i][1])
        tem.append(export[i][0]-1)
        tem.append(export[i][1]-1)
    n = max(tem)
    total_around_people = []
    for i in range(1, n + 1):  # 总循环次数n,从1开始
        around_people = []
        if export[0][1] + i < row + 1:  # 上左(有这一行)在范围内
            if export[0][0] - i > 0:  # 上左(列)在范围内
                if export[0][0] + i < column + 1:  # 上右（列）在范围内
                    for j in range(export[0][0] - i, export[0][0] + i + 1):   #列的变化范围
                        if room[export[0][1]+i][j] == 1:
                            around_people.append((export[0][1]+i, j))
                else:  # 上右(列)不再范围内
                    for j in range(export[0][0] - i, column + 1):
                        if room[export[0][1]+i][j] == 1:
                            around_people.append((export[0][1]+i, j))
            else:  # 上左（列）不在范围内
                if export[0][0] + i < column + 1:  # 上右（列）在范围内
                    for j in range(1, export[0][0]+i+1):
                        if room[export[0][1]+i][j] == 1:
                            around_people.append((export[0][1]+i, j))
                else:  # 上右(列)不再范围内
                    for j in range(1, column + 1):
                        if room[export[0][1]+i][j] == 1:
                            around_people.append((export[0][1], j))
        if export[0][1] - i > 0:  # 下左在范围内（有这一行）
            if export[0][0] - i > 0:  # 下左（列）在范围内
                if export[0][0] + i < column + 1:  # 下右（列）在范围内
                    for j in range(export[0][0] - i, export[0][0] + i + 1):
                        if room[export[0][1]-i][j] == 1:
                            around_people.append((export[0][1]-i, j))
                else:  # 下右（列）不在范围内
                    for j in range(export[0][0] - i, column + 1):
                        if room[export[0][1]-i][j] == 1:
                            around_people.append((export[0][1]-i, j))
            else:  # 下左（列）不在范围内
                if export[0][0] + i < column + 1:  # 下右（列）在范围内
                    for j in range(1, export[0][0] + i + 1):
                        if room[export[0][1]-i][j] == 1:
                            around_people.append((export[0][1]-i, j))
                else:  # 下右（列）不在范围内
                    for j in range(1, column + 1):
                        if room[export[0][1]-i][j] == 1:
                            around_people.append((export[0][1]-i, j))
        if export[0][0] - i > 0:  # 上左（列）存在
            if export[0][1] + i < row + 1:  # 上左（行）存在
                if export[0][1] - i > 0:  # 下左（行）存在
                    for j in range(export[0][1]- i +1, export[0][1] + i):
                        if room[j][export[0][0]-i] == 1:
                            around_people.append((j, export[0][0] - i))
                else:  # 下左（行）不存在
                    for j in range(1, export[0][1] + i):
                        if room[j][export[0][0] - i] == 1:
                            around_people.append((j, export[0][0] - i))
            else:  # 上左（行）不存在
                if export[0][1] - i > 0:  # 下左（行）存在
                    for j in range(export[0][1]+1,len(room)-1):
                        if room[j][export[0][0] - i] == 1:
                            around_people.append((j, export[0][0] - i))
                else:  # 下左（行）不存在
                    for j in range(1, len(room)-1):
                        if room[j][export[0][0] - i] == 1:
                            around_people.append((j, export[0][0] - i))
        if export[0][0] + i < len(room[i])-1:  # 上右（列）存在
            if export[0][1] + i < len(room)-1:  # 上右（行）存在
                if export[0][1] - i > 0:  # 下右（行）存在
                    for j in range(export[0][1] - i + 1, export[0][1] + i):
                        if room[j][export[0][0] + i] == 1:
                            around_people.append((j, export[0][0] + i))
                else:  # 下右（行）不存在
                    for j in range(1, export[0][1] + i):
                        if room[j][export[0][0] + i] == 1:
                            around_people.append((j, export[0][0] + i))
            else:  # 上右（行）不存在
                if export[0][1] - i > 0:  # 下右（行）存在
                    for j in range(export[0][1]-i, len(room)-1):
                        if room[j][export[0][0] + i] == 1:
                            around_people.append((j, export[0][0] + i))
                else:  # 下右（行）不存在
                    for j in range(1, len(room)-1):
                        if room[j][export[0][0] + i] == 1:
                            around_people.append((j, export[0][0] + i))
        total_around_people.append(around_people)

    newlist = [x for x in total_around_people if x]  # 删除空格项
    distance = []
    dic = {}
    for i in range(len(newlist)):
        subdis = []
        for j in range(len(newlist[i])):
            dis = ((newlist[i][j][0] - export[0][1] + 1) ** 2 + (newlist[i][j][1] - export[0][0] + 1) ** 2)
            dic[newlist[i][j]] = dis
            subdis.append(dis)
        distance.append(subdis)
    tourists_move(dic, distance)  # 引用移动函数


def tourists_move(dic, distance):
    for k in range(len(distance)):
        order = sorted(distance[k])
        order_dis = []  # 排序存放了周围元素距离坐标
        for i in order:
            for key, val in dic.items():
                if val == i:
                    order_dis.append(key)
                    del dic[key]
                    break
  
        for i in range(len(order_dis)):  # 一次判断每个点
            x, y, xdoor, ydoor = order_dis[i][0], order_dis[i][1], export[0][1], export[0][0]
            if x < xdoor and y > ydoor:  # 右下角
                if room[x+1][y-1] == 8:  #斜角
                    room[x][y] = 0
                elif room[x + 1][y - 1] == 0 and (y-1>ydoor or x+1<xdoor):  # 斜角
                    room[x + 1][y - 1] = 1
                    room[x][y] = 0
                elif room[x][y - 1] == 0:  # 往左
                    room[x][y - 1] = 1
                    room[x][y] = 0
                elif room[x + 1][y] == 0:  # 往下
                    room[x + 1][y] = 1
                    room[x][y] = 0
                else:
                    continue
            elif x > xdoor and y > ydoor:  # 右上角
                if room[x-1][y-1]==8:
                    room[x][y] = 0
                elif room[x - 1][y - 1] == 0 and (y-1>ydoor or x-1>xdoor):  # 斜角
                    room[x - 1][y - 1] = 1
                    room[x][y] = 0
                elif room[x][y - 1] == 0:  # 往左
                    room[x][y - 1] = 1
                    room[x][y] = 0
                elif room[x - 1][y] == 0:  # 往下
                    room[x - 1][y] = 1
                    room[x][y] = 0
                else:
                    continue
            elif x == xdoor and y > ydoor:  #(右)正前面
                if room[x][y - 1] == 8:  #往前8
                    room[x][y] = 0
                elif room[x][y - 1] == 0:  #往前
                    room[x][y - 1] = 1
                    room[x][y] = 0
                else:
                    if room[x+1][y-1]==0:
                        room[x + 1][y - 1] = 1
                        room[x][y]=0
                    elif room[x-1][y-1]==0:
                        room[x-1][y-1]=1
                        room[x][y]=0
                    else:
                         continue
            elif x < xdoor and y <= ydoor:   #左下
                if room[x + 1][y + 1] == 8:
                    room[x][y] = 0
                elif room[x + 1][y + 1] == 0 and (y+1<ydoor or x+1<xdoor):  #斜角
                    room[x + 1][y + 1] = 1
                    room[x][y] = 0
                elif room[x + 1][y] == 0:    #往上
                    room[x + 1][y] = 1
                    room[x][y] = 0
                elif room[x][y + 1] == 0:    #往右
                    room[x][y + 1] = 1
                    room[x][y] = 0
                else:
                    continue
            elif x > xdoor and y <= ydoor:   #左上
                if room[x-1][y+1]==8:
                    room[x][y]=0
                elif room[x - 1][y + 1] == 0 and (y+1<ydoor or x-1>xdoor):  #斜角
                    room[x - 1][y + 1] = 1
                    room[x][y] = 0
                elif room[x][y + 1] == 0:   #往右
                    room[x][y + 1] = 1
                    room[x][y] = 0
                elif room[x - 1][y] == 0:   #往下
                    room[x - 1][y] = 1
                    room[x][y] = 0
                else:
                    continue
                # elif x == xdoor and y <ydoor:
            else: #(左)正对
                if room[x][y+1]==8:
                    room[x][y]=0
                elif room[x][y+1]==0:
                    room[x][y+1]=1
                    room[x][y]=0
                else:
                    if room[x+1][y+1]==0:
                        room[x+1][y+1]=1
                        room[x][y]=0
                    elif room[x-1][y+1]==0:
                        room[x-1][y+1]=1
                        room[x][y]=0
                    else:
                        continue


# 可视化


def visualization():
    for i in range(1, len(room) - 1):
        for j in range(1, len(room[i]) - 1):
            if room[i][j] == 1:
                rect = mpathes.Circle((j + 0.5, i + 0.5), 0.3, color='grey')
                ax.add_patch(rect)
    plt.show()


def main():
    create_flat()
    #visualization()  # 调用可视化函数
    update_state()
    visualization()   #调用可视化函数


if __name__ == '__main__':
    '''
    N：室内游客总数
    column：室内水平方向元胞个数，代表列数量
    row：室内竖直方向元胞个数,代表行数量
    '''
    N, row, column = 20, 20, 20
    room = np.zeros((row + 2, column + 2))  # 创建房间
    export = [(5, 0)]  # 设定出口位置和开门方向,此处为坐标轴坐标

    initial_room()  # 创建人员
    while 1 in room:
        fig, ax = plt.subplots()
        main()
