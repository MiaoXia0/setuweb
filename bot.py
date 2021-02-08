from nonebot import get_bot
from hoshino import Service, R
from hoshino.typing import HoshinoBot, CQEvent
from .__init__ import allowed_groups, allow_path
import requests
try:
    import ujson as json
except ImportError:
    import json

allowed = allowed_groups
sv = Service('setuweb')
ip = json.loads(requests.get('https://jsonip.com/').text)['ip']
bot = get_bot()
port = bot.config.PORT
if port == 80:
    help_str = f'''本插件为在线setu插件
进入http://{ip}/setu/开始使用本插件
输入setuallow允许本群发送色图
输入setuforbid禁止本群发送色图'''
else:
    help_str = f'''本插件为在线setu插件
进入http://{ip}:{port}/setu/开始使用本插件
输入setuallow允许本群发送色图
输入setuforbid禁止本群发送色图'''


@sv.on_fullmatch('setuhelp')
async def setuhelp(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_str)


@sv.on_fullmatch('setuallow')
async def setuallow(bot: HoshinoBot, ev: CQEvent):
    group_id = ev.group_id
    allowed[group_id] = True
    json.dump(allowed, open(allow_path, 'w'))
    await bot.send(ev, f'已允许{group_id}')


@sv.on_fullmatch('setuforbid')
async def setuforbid(bot: HoshinoBot, ev: CQEvent):
    group_id = ev.group_id
    allowed[group_id] = False
    json.dump(allowed, open(allow_path, 'w'))
    await bot.send(ev, f'已禁止{group_id}')


async def down_img(url: str):
    print(f'downloading from {url}')
    img = requests.get(url)
    filename = url.split('/')[-1]
    path = R.img('setuweb/').path
    f = open(f'{path}/{filename}', 'wb')
    f.write(img.content)
    print(f'downloaded {filename}')


async def send_to_group(group_id: int, url: str):
    if not allowed_groups[group_id]:
        return '此群不允许发送！'
    else:
        await down_img(url)
        filename = url.split('/')[-1]
        print(f'sending {filename}')
        msg = R.img(f'setuweb/{filename}').cqcode
        await bot.send_group_msg(group_id=group_id, message=msg)
        print(f'sended {filename}')
        return f'已发送到群{group_id}！'


def get_groups():
    groups = bot.get_group_list()
    return groups
