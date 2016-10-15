import psycopg2

class PointDB():
    """database to link with postgreSQL DB"""
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='writer' user='postgres' host='postgres' password='password'")
        except:
            print "I am unable to connect to the database"
    def __exit__(self, type, value, traceback):
        self.conn.close()

    #fixme: check type in case of inject attack
    def selectPoints(self, xmin, xmax, ymin, ymax, cur_ts, delta_ts):
        prev_ts = cur_ts - delta_ts
        query = "SELECT x,y,tag_id,time_stamp FROM point WHERE x >= {} AND x < {} AND y >= {} AND y < {} AND time_stamp >= {} AND time_stamp < {}".format(xmin, xmax, ymin, ymax, prev_ts, cur_ts)
        
        cur = self.conn.cursor()
        try:
            cur.execute(query)
        except:
            print "I can't select points! query" + query
        rows = cur.fetchall()
        appeared_tagids = list(set(map(lambda r:r[2],rows)))
        return rows, appeared_tagids

    def tagidToTag(self):
        query = "SELECT * FROM tag"
        cur = self.conn.cursor()
        try:
            cur.execute(query)
        except:
            print "I can't select points! query" + query
        rows = cur.fetchall()
        return rows
    def close(self):
        self.conn.close()
