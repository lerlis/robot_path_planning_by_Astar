import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

robot_map = []


class Block:
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.status = status
        self.bl_g = -1
        self.bl_h = -1
        self.bl_f = -1
        self.is_path = 0
        self.parent_block = None


BLOCK_STATE_NORMAL = 0
BLOCK_STATE_OBSTACLE = 1
BLOCK_STATE_START = 2
BLOCK_STATE_END = 3


def init_map(length, width, opoint):
    global map_length, map_width, start_point, end_point
    if (width == -1) and (length == -1):
        map_length = 10
        map_width = 10
        for i in range(map_width):
            for j in range(map_length):
                robot_map.append(Block(j, i, BLOCK_STATE_NORMAL))
        obstacle = [10, 13, 18, 25, 32, 36, 38, 54, 72, 76, 90, 92, 98]
        for i in range(map_width * map_length):
            if i in obstacle:
                robot_map[i].status = BLOCK_STATE_OBSTACLE
            elif robot_map[i].x == 2 and robot_map[i].y == 2:
                robot_map[i].status = BLOCK_STATE_START
                start_point = i
            elif robot_map[i].x == 8 and robot_map[i].y == 8:
                robot_map[i].status = BLOCK_STATE_END
                end_point = i
    else:
        for i in range(map_width):
            for j in range(map_length):
                robot_map.append(Block(j, i, BLOCK_STATE_NORMAL))
        count = 0
        while True:
            ob = random.randint(0, map_width * map_length - 1)
            if robot_map[ob].status == BLOCK_STATE_NORMAL:
                count = count + 1
                robot_map[ob].status = BLOCK_STATE_OBSTACLE
            if count == opoint:
                break
        while True:
            spoint = random.randint(0, map_width * map_length - 1)
            if robot_map[spoint].status == BLOCK_STATE_NORMAL:
                robot_map[spoint].status = BLOCK_STATE_START
                start_point = spoint
                break
        while True:
            epoint = random.randint(0, map_width * map_length - 1)
            if robot_map[epoint].status == BLOCK_STATE_NORMAL:
                robot_map[epoint].status = BLOCK_STATE_END
                end_point = epoint
                break


def print_map():
    len_map = len(robot_map)
    map_array = []
    map_line = []
    for i in range(len_map):
        if robot_map[i].status == BLOCK_STATE_NORMAL:
            if robot_map[i].is_path == 1:
                map_line.append('P')
            else:
                map_line.append(0)
        elif robot_map[i].status == BLOCK_STATE_OBSTACLE:
            map_line.append(1)
        elif robot_map[i].status == BLOCK_STATE_START:
            map_line.append('s')
        else:
            map_line.append('e')
        if (i + 1) % map_length == 0:
            map_array.append(map_line)
            map_line = []
    np_map = np.array(map_array)
    print(np_map)


def find_path():
    global map_length, map_width, start_point, end_point
    count = 0
    # Open and Close 表
    open_list = []
    close_list = []

    open_list.append(robot_map[start_point])
    cal_function_F(robot_map[start_point], robot_map[end_point])

    while len(open_list) > 0:
        minFpoint = find_minF_point(open_list)
        open_list.remove(minFpoint)
        close_list.append(minFpoint)

        display(open_list, close_list, count)
        count = count + 1

        expand_list = find_surround_way(minFpoint, close_list)
        if robot_map[end_point] in expand_list:
            robot_map[end_point].parent_block = minFpoint
            print('yes!')
            break
        for expoint in expand_list:

            if expoint in open_list:
                new_gain = cal_alter_g(expoint, minFpoint)
                if new_gain < expoint.bl_g:
                    expoint.parent_block = minFpoint
                    expoint.bl_g = new_gain
            elif expoint in close_list:
                new_gain = cal_alter_g(expoint, minFpoint)
                if new_gain < expoint.bl_g:
                    expoint.parent_block = minFpoint
                    expoint.bl_g = new_gain
                    close_list.remove(expoint)
                    open_list.append(expoint)
            else:
                expoint.parent_block = minFpoint
                cal_function_F(expoint, robot_map[end_point])
                open_list.append(expoint)
    End_game = robot_map[end_point]
    while True:
        End_game.is_path = 1
        End_game = End_game.parent_block
        if End_game is None:
            break
    print('结果：')
    print_map()
    display(open_list, close_list, count)


def cal_alter_g(point, minpoint):
    new_g = np.sqrt((point.x - minpoint.x) ** 2 + (
            point.y - minpoint.y) ** 2) + minpoint.bl_g
    return new_g


def cal_function_F(point, epoint):
    if point.parent_block is None:
        g = 0
    else:
        g = np.sqrt((point.x - point.parent_block.x) ** 2 + (
            point.y - point.parent_block.y) ** 2) + point.parent_block.bl_g
    h = np.sqrt((point.x - epoint.x) ** 2 + (point.y - epoint.y) ** 2)
    point.bl_g = g
    point.bl_h = h
    point.bl_f = g + h


def find_minF_point(op_list):
    min = np.inf
    temp = 0
    for point in op_list:
        if point.bl_f < min:
            min = point.bl_f
            temp = point
    return temp


def find_surround_way(mpoint, exist_list):
    global map_length, map_width, start_point, end_point
    expand_list = []
    # 左边的点
    if mpoint.x > 0:
        left = robot_map[mpoint.y * map_length + mpoint.x - 1]
        if check(left, exist_list):
            expand_list.append(left)
    # 右边的点
    if mpoint.x < map_length - 1:
        right = robot_map[mpoint.y * map_length + mpoint.x + 1]
        if check(right, exist_list):
            expand_list.append(right)
    # 上边的点
    if mpoint.y > 0:
        up = robot_map[(mpoint.y - 1) * map_length + mpoint.x]
        if check(up, exist_list):
            expand_list.append(up)
    # 下边的点
    if mpoint.y < map_width - 1:
        down = robot_map[(mpoint.y + 1) * map_length + mpoint.x]
        if check(down, exist_list):
            expand_list.append(down)
    # 左上方的点
    if mpoint.x > 0 and mpoint.y > 0:
        left_up = robot_map[(mpoint.y - 1) * map_length + mpoint.x - 1]
        if check(left_up, exist_list):
            expand_list.append(left_up)
    # 左下方的点
    if mpoint.x > 0 and mpoint.y < map_width - 1:
        left_down = robot_map[(mpoint.y + 1) * map_length + mpoint.x - 1]
        if check(left_down, exist_list):
            expand_list.append(left_down)
    # 右上方的点
    if mpoint.x < map_length - 1 and mpoint.y > 0:
        right_up = robot_map[(mpoint.y - 1) * map_length + mpoint.x + 1]
        if check(right_up, exist_list):
            expand_list.append(right_up)
    # 右下方的点
    if mpoint.x < map_length - 1 and mpoint.y < map_width - 1:
        right_down = robot_map[(mpoint.y + 1) * map_length + mpoint.x + 1]
        if check(right_down, exist_list):
            expand_list.append(right_down)
    return expand_list


def check(point, exist):
    if point.status == BLOCK_STATE_OBSTACLE:
        return 0
    else:
        return 1


def display(op, cl, count):
    mat = np.zeros([map_length, map_width])
    chang = len(mat)
    kuan = len(mat[1])
    t = 0
    judge = [0, 0, 0]
    c = 0
    for i in range(kuan):
        for j in range(chang):
            if robot_map[t] in op:
                judge[0] = 1
                mat[i][j] = 4
            if robot_map[t] in cl:
                if len(cl) == 1:
                    judge[1] = 0
                else:
                    judge[1] = 1
                mat[i][j] = 5
            if robot_map[t].is_path == 1:
                c = c + 1
                if c == 1:
                    judge[2] = 0
                else:
                    judge[2] = 1
                mat[i][j] = 6
            if robot_map[t].status == BLOCK_STATE_OBSTACLE:
                mat[i][j] = 1
            elif robot_map[t].status == BLOCK_STATE_START:
                mat[i][j] = 2
            elif robot_map[t].status == BLOCK_STATE_END:
                mat[i][j] = 3
            t = t + 1
    cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Red', 'Orange', 'Indigo'])
    if judge == [0, 0, 0]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise'])
    elif judge == [1, 0, 0]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Red'])
    elif judge == [0, 1, 0]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Orange'])
    elif judge == [1, 1, 1]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Red', 'Orange', 'Indigo'])
    elif judge == [1, 1, 0]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Red', 'Orange'])
    elif judge == [0, 1, 1]:
        cmap = ListedColormap(['LightGray', 'Black', 'Lightgreen', 'Turquoise', 'Orange', 'Indigo'])
    plt.figure(count)
    plt.matshow(mat, cmap=cmap)
    plt.savefig('./random/%s.jpg' % count)
    plt.show()


if __name__ == '__main__':
    start_point = -1
    end_point = -1
    map_length = -1
    map_width = -1
    obstacle_point = 2000
    init_map(map_length, map_width, obstacle_point)
    print_map()
    find_path()
