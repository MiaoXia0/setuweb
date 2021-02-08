from nonebot import get_bot
from hoshino import Service
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
        进入http://{ip}/setu/开始使用本插件
        '''
else:
    help_str = f'''本插件为在线setu插件
        进入http://{ip}:{port}/setu/开始使用本插件
        '''


@sv.on_fullmatch('setuhelp')
async def setuhelp(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_str)


async def send_to_group(group_id: int, url: str):
    msg = f'[CQ:image,file={url}]'
    await bot.send_group_msg(group_id=group_id, message=msg)


def get_groups():
    return bot.get_group_list()
