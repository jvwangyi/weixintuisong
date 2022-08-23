from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = today = datetime.now().date()
# start_date = os.environ['START_DATE']
city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]#微信推送账户

user_id = os.environ["USER_ID"]#目标id
template_id = os.environ["TEMPLATE_ID"]#接口模板


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])
# 获取地区天气信息
# def get_count():
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days
# #获取认识到现在的时间
# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days
# # 获取生日时间
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']
# 获取鼓励文字

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
# 彩色字体


client = WeChatClient(app_id, app_secret)#测试账号
wm = WeChatMessage(client)

wea, temperature, highest, lowest = get_weather()
data = {"date":{"value":json.dumps(today,default=str).split("\"")[1],"color":get_random_color()},
"weather":{"value":wea,"color":get_random_color()},
"temperature":{"value":temperature,"color":get_random_color()},
"words":{"value":get_words(),"color":get_random_color()},
"highest": {"value":highest,"color":get_random_color()},
"lowest":{"value":lowest, "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)