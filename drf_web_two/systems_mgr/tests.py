import json
import os
import random
import sys
import time

import requests
from django.test import TestCase
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_web_two.settings')
django.setup()
# Create your tests here.
from django.db import connection
from django.core.cache import cache
from systems_mgr.models import AreaCity, Employee
import logging
# Get an instance of a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


def test_log_level():
    # set default logging configuration
    logger = logging.getLogger()  # initialize logging class
    logger.setLevel(logging.INFO)  # default log level
    format = logging.Formatter("%(asctime)s - %(message)s")  # output format
    sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
    sh.setFormatter(format)
    logger.addHandler(sh)

    # use logging to generate log ouput
    logger.debug("this is debug")
    logger.info("this is info")
    logger.warning("this is warning")
    logging.error("this is error")
    logger.critical("this is critical")


test_log_level()
if __name__ == '__main__':
    # cache.set('code', '1234', 3)
    # time.sleep(4)
    # print(cache.get('code'))
    #批量导入城市数据
    # with connection.cursor() as cursor:
    #     sql='select * from travel_area'
    #     cursor.execute(sql)
    #     result=cursor.fetchall()
    #     task_list=[]
    #     for obj in result:
    #         parent_id=None if obj[2]==0 else obj[2]
    #         area=AreaCity(pk=obj[0],
    #                         area_name=obj[1],
    #                         area_parent_id=parent_id,
    #                         area_sort=obj[3],
    #                         area_type=obj[4])
    #         task_list.append(area)
    #     AreaCity.objects.bulk_create(task_list)

    # user=Employee.objects.get(pk=1)
    # print(user.address.area_name)   #区
    # print(user.address.area_parent.area_name)   #市
    # print(user.address.area_parent.area_parent.area_name)   #省
    # logger.info('提示信息！')
    pass