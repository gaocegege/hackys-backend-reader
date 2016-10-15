import sys
from pointdb import PointDB

STEP_CNT = 1000
POS_SEPARATOR = "#"
DISTANCE = 2
LEAST_SIZE = 10


def near_node(pos_tag1, pos_tag2):
    tmp = pos_tag1.split(POS_SEPARATOR)
    x1 = int(tmp[0])
    y1 = int(tmp[1])
    tmp = pos_tag2.split(POS_SEPARATOR)
    x2 = int(tmp[0])
    y2 = int(tmp[1])
    return abs(x1 - x2) < DISTANCE and abs(y1 - y2) < DISTANCE


def calculate_distance(x1, x2, x_step, y1, y2, y_step):
    return pow(pow((x1 - x2) * x_step, 2) + pow((y1 - y2) * y_step, 2), 0.5)


def get_final_info(x_min, x_max, y_min, y_max, current_ts, delta_t, tags_considered):
    conn = PointDB()
    raw_info, used_tags = conn.selectPoints(x_min, x_max, y_min, y_max, current_ts, delta_t)

    x_len = x_max - x_min
    x_step = x_len / STEP_CNT
    y_len = y_max - y_min
    y_step = y_len / STEP_CNT

    mosaic_map = {}
    for info in raw_info:
        # schema: info = {x:int, y:int, tag:str, ts:str}
        x = int(info[0] / x_step)
        y = int(info[1] / y_step)
        tag = info[2]

        if tag not in tags_considered:
            continue

        pos_tag = str(x) + POS_SEPARATOR + str(y)
        if pos_tag in mosaic_map:
            cur_cnt = mosaic_map[pos_tag]
            if tag in cur_cnt:
                cur_cnt[tag] += 1
            else:
                cur_cnt[tag] = 1
        else:
            mosaic_map[pos_tag] = {tag: 1}

    tag2pos = {}
    for item in mosaic_map.items():
        pos_tag = item[0]
        cnt_result = item[1]

        max_cnt = -1
        max_tag = set()
        for i in cnt_result.items():
            tag = i[0]
            cnt = i[1]
            if cnt > max_cnt:
                max_tag = set()
                max_tag.add(tag)
                max_cnt = cnt
            elif cnt == max_cnt:
                max_tag.add(tag)

        for tag in max_tag:
            if tag in tag2pos:
                tag2pos[tag].add(pos_tag)
            else:
                tag2pos[tag] = set()
                tag2pos[tag].add(pos_tag)

    tag2block = {}
    for tag in tag2pos:
        blocks_list = list()
        for insert_pt in tag2pos[tag]:
            belonging_id = []
            for i in range(0, blocks_list.__len__()):
                for ref_pt in blocks_list[i]:
                    if near_node(insert_pt, ref_pt):
                        belonging_id.append(i)
                        break
            belonging_size = belonging_id.__len__()
            if belonging_size > 1:
                # remove from end to head to eliminate strange things
                belonging_id.reverse()
                new_block = set()
                for i in belonging_id:
                    new_block = new_block.union(blocks_list[i])
                    blocks_list.pop(i)
                new_block.add(insert_pt)
                blocks_list.append(new_block)
            elif belonging_size == 1:
                blocks_list[belonging_id[0]].add(insert_pt)
            else:
                block = set()
                block.add(insert_pt)
                blocks_list.append(block)

        # filter blocks whose size is too small
        to_remove = []
        for i in range(blocks_list.__len__()):
            if len(blocks_list[i]) < LEAST_SIZE:
                to_remove.append(i)
        to_remove.reverse()
        for i in to_remove:
            blocks_list.pop(i)

        if blocks_list.__len__() > 0:
            tag2block[tag] = blocks_list

    tag2final = {}
    for tag in tag2block:
        for block in tag2block[tag]:
            t_x_min = sys.maxint
            t_x_max = -1
            t_y_min = sys.maxint
            t_y_max = -1
            for pt in block:
                info = pt.split(POS_SEPARATOR)
                x = int(info[0])
                y = int(info[1])
                t_x_min = min(x, t_x_min)
                t_x_max = max(x, t_x_max)
                t_y_min = min(y, t_y_min)
                t_y_max = max(y, t_y_max)
            diameter = calculate_distance(t_x_min, t_x_max, x_step, t_y_min, t_y_max, y_step)
            r_x = (t_x_min + t_x_max) * x_step / 2
            r_y = (t_y_min + t_y_max) * y_step / 2
            if tag in tag2final:
                tag2final[tag].append([r_x, r_y, diameter / 2])
            else:
                tag2final[tag] = [[r_x, r_y, diameter / 2]]

    # filter final result to eliminate too much overlapped
    pre_list = []
    for tag in tag2final:
        block_list = tag2final[tag]
        for pos in range(len(block_list)):
            insert = [tag + "#" + str(pos)]
            insert.extend(block_list[pos])
            # schema: [tag#pos, x, y, radius]
            pre_list.append(insert)
    to_remove = []
    for pos in range(len(pre_list)):
        for inner in range(pos):
            if inner not in to_remove:
                cur_pt = pre_list[pos]
                ref_pt = pre_list[inner]
                distance = calculate_distance(cur_pt[1], ref_pt[1], 1, cur_pt[2], ref_pt[2], 1)
                if cur_pt[3] > distance or ref_pt[3] > distance:
                    if cur_pt[3] > ref_pt[3]:
                        to_remove.append(inner)
                    else:
                        to_remove.append(pos)
    remove_dict = {}
    for pos in to_remove:
        c_tag = pre_list[pos][0].split("#")
        tag = c_tag[0]
        i = int(c_tag[1])
        if tag in remove_dict:
            remove_dict[tag].append(i)
        else:
            remove_dict[tag] = [i]
    for item in remove_dict.items():
        tag = item[0]
        tmp_list = item[1]
        tmp_list.sort(reverse=True)
        for i in tmp_list:
            tag2final[tag].pop(i)

    return tag2final


def get_all_tags():
    conn = PointDB()
    return conn.tagidToTag()

