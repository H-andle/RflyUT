#!/usr/bin/env python3
# coding=utf-8
#########################################################################
# Author: @maris
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:process_user_job.py
# Description:redis， key/value系统
#########################################################################

import redis
import json


# pub/sub
class redis_db():
    def __init__(self,host,port,db,password) -> None:
        self.rdb = redis.StrictRedis(host=host, port=port, db=db, password=password)

    ################################kv部分########################################

    # 设置数据，key/value均为字符串
    def set_data(self, key, data, ex):
        self.rdb.set(key, json.dumps(data),ex=ex)
        return 0


    # 设置多个数据
    def set_multi_data(self, kv_dict):
        self.rdb.mset(kv_dict)
        return 0


    # 获得数据
    def get_data(self, key):
        data_str = self.rdb.get(key)
        if data_str is None:
            return False
        data = json.loads(data_str)
        return data


    # 获得多个
    def get_mulit_data(self, key_list):
        str_data_list = self.rdb.mget(key_list)  # 字符串形式
        data_list = []
        for data_str in str_data_list:
            data = json.loads(data_str)
            data_list.append(data)
        return data_list


    # 获得所有数据
    def get_data_list(self):
        data_list = []
        for key in self.rdb.keys():
            data = self.get_data(key)
            data_list.append(data)
        return data_list


    # 删除数据
    def del_data(self, key):
        self.rdb.delete(key)
        return 0


    # 获得key的个数
    def key_count(self):
        count = len(self.rdb.keys())
        return count


    # 清空表
    def clear_db(self):
        # self.rdb0.flushdb(target_nodes=RedisCluster.ALL_NODES)
        self.rdb.flushdb()

        return 0


    # 发布消息
    def pub_data(self, key, data):
        self.rdb.publish(key, json.dumps(data))
        return 0


    ################################queue部分########################################

    # 插入数据,默认插入json字符串格式
    def insert_data(self, db, data):
        self.rdb.lpush(db, json.dumps(data))
        return 0


    # 插入多个数据
    def insert_data_list(self, db, data_list):
        for data in data_list:
            self.insert_data(db, data)


    # 获得队列一个数据(同时删除)
    def get_one_data(self, db):
        data = self.rdb.rpop(db)
        if data:
            return json.loads(data)
        else:
            return -1


    # 获得队列所有值，不删除
    def get_all_data(self, db):
        return self.rdb.lrange(db, 0, -1)


    # 获得队列长度
    def queue_count(self, db):
        count = self.rdb.llen(db)
        return count


    # 清空队列
    def clear_queue(self, db):
        while True:
            data = self.rdb.rpop(db)
            if data:  # 如果队列不为空
                pass
            else:  # 如果队列为空，sleep
                break


if __name__ == "__main__":
    data = {"account_id": "abcde111"}
    key = "global_param"
    rdb = redis_db()
    rdb.set_data(key, data)

    result = rdb.get_data(key)
    print(result)
