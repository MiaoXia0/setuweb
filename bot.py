from nonebot import get_bot
from hoshino import Service, R
from hoshino.typing import HoshinoBot, CQEvent
import requests

try:
    import ujson as json
except ImportError:
    import json
sv = Service('setuweb')
ip = json.loads(requests.get('https://jsonip.com/').text)['ip']
bot = get_bot()
port = bot.config.PORT
if port == 80:
    help_str = f'''本插件为在线setu插件
进入http://{ip}/setu/开始使用本插件'''
else:
    help_str = f'''本插件为在线setu插件
进入http://{ip}:{port}/setu/开始使用本插件'''


@sv.on_fullmatch('setuhelp')
async def setuhelp(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_str)


async def down_img(url: str):
    print(f'downloading from {url}')
    img = requests.get(url)
    filename = url.split('/')[-1]
    path = R.img('setuweb/').path
    f = open(f'{path}/{filename}', 'wb')
    f.write(img.content)
    print(f'downloaded {filename}')


async def send_to_group(group_id: int, url: str):
    await down_img(url)
    filename = url.split('/')[-1]
    print(f'sending {filename}')
    msg = R.img(f'setuweb/{filename}').cqcode
    await bot.send_group_msg(group_id=group_id, message=msg)
    print(f'sended {filename}')


def get_groups():
    groups = bot.get_group_list()
    return groups
