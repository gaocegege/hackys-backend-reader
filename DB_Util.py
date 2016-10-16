MOOD_FN = "beiling.data"
TAG_FN = "tag.data"
SEPARATOR = " "


def get_tag_map():
    tag_file = open(TAG_FN)
    tag_map = {}
    for tag in tag_file:
        tag = tag.replace("\n", "")
        info = tag.split(SEPARATOR)
        tag_map[info[0]] = info[1]
    return tag_map


def rewrite(fn):
    mood_file = open(MOOD_FN)
    op = open(fn, "w")
    rs = []
    for line in mood_file:
        rs.append(line)
    # rs.sort()
    for i in rs:
        op.write(i)
    op.flush()
    op.close()


def get_data_inbound(x_min, x_max, y_min, y_max, current_ts, delta_t):
    mood_file = open(MOOD_FN, "r")
    rs = []
    used_tags = set()

    for line in mood_file.readlines():
        line = line.replace("\n", "")
        info = line.split(SEPARATOR)
        x = float(info[0])
        y = float(info[1])
        ts = int(info[3])

        if x_min < x < x_max and y_min < y < y_max and current_ts - delta_t <= ts <= current_ts:
            rs.append([x, y, info[2], info[3]])
            used_tags.add(info[2])

    return rs, used_tags
