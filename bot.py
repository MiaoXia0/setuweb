from nonebot import get_bot
from hoshino import Service, R
from hoshino.typing import HoshinoBot, CQEvent
from hoshino.priv import ADMIN, check_priv
import requests
import os
import aiohttp

try:
    import ujson as json
except ImportError:
    import json

allow_path = os.path.dirname(__file__) + '/allowed_groups.json'
if not os.path.exists(allow_path):
    allowed_groups = {}
    json.dump(allowed_groups, open(allow_path, 'w'))
else:
    allowed_groups = json.load(open(allow_path, 'r'))
    print(allowed_groups)

r18_path = os.path.dirname(__file__) + '/r18_groups.json'
if not os.path.exists(r18_path):
    r18_groups = {}
    json.dump(r18_groups, open(r18_path, 'w'))
else:
    r18_groups = json.load(open(r18_path, 'r'))
    print(r18_groups)


sv = Service('setuweb')
ip = json.loads(requests.get('https://jsonip.com/').text)['ip']
bot = get_bot()
port = bot.config.PORT
curr_dir = os.path.dirname(__file__)
config = json.load(open(f'{curr_dir}/config.json'))

if port == 80:
    setu_url = f'http://{ip}/setu/'
else:
    setu_url = f'http://{ip}:{port}/setu/'

help_str = f'''本插件为在线setu插件
进入{setu_url}开始使用本插件
输入setu/r18allow允许本群发送色图/r18色图
输入setu/r18forbid禁止本群发送色图/r18色图
输入来\\发\\给(数量)份\\点\\张\\幅(R\\r18)(关键字)\\涩\\瑟\\色图 在群内获取色图'''


@sv.on_fullmatch('setuhelp')
async def setuhelp(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_str)


@sv.on_fullmatch('setuallow')
async def setuallow(bot: HoshinoBot, ev: CQEvent):
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    allowed_groups[str(group_id)] = True
    json.dump(allowed_groups, open(allow_path, 'w'))
    await bot.send(ev, f'已允许{group_id}')


@sv.on_fullmatch('setuforbid')
async def setuforbid(bot: HoshinoBot, ev: CQEvent):
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    allowed_groups[str(group_id)] = False
    json.dump(allowed_groups, open(allow_path, 'w'))
    await bot.send(ev, f'已禁止{group_id}')


@sv.on_fullmatch('r18allow')
async def setuallow(bot: HoshinoBot, ev: CQEvent):
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    r18_groups[str(group_id)] = True
    json.dump(r18_groups, open(r18_path, 'w'))
    await bot.send(ev, f'已允许{group_id}r18')


@sv.on_fullmatch('r18forbid')
async def setuforbid(bot: HoshinoBot, ev: CQEvent):
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    r18_groups[str(group_id)] = False
    json.dump(r18_groups, open(r18_path, 'w'))
    await bot.send(ev, f'已禁止{group_id}r18')


@sv.on_rex(r'^[来发给](\d*)?[份点张幅]([Rr]18)?(.*)?[涩瑟色]图$')
async def group_setu(bot: HoshinoBot, ev: CQEvent):
    group_id = ev.group_id
    try:
        if not allowed_groups[str(group_id)]:
            await bot.send_group_msg(group_id=group_id, message='此群不允许发送Setu！')
            return
    except KeyError:
        await bot.send_group_msg(group_id=group_id, message='此群不允许发送Setu！')
        return
    api = config['group_api']
    if api == 'lolicon':
        num = ev['match'].group(1)
        if num == '':
            num = 1
        else:
            num = int(num)
        r18 = int(ev['match'].group(2) is not None)
        if r18 == 1:
            try:
                if not r18_groups[str(group_id)]:
                    await bot.send_group_msg(group_id=group_id, message='此群不允许发送r18Setu！')
                    return
            except KeyError:
                await bot.send_group_msg(group_id=group_id, message='此群不允许发送r18Setu！')
                return
        await bot.send_group_msg(group_id=group_id, message='获取中')
        keyword = ev['match'].group(3)
        apikeys = config['apikey']
        size1200 = int(config['size1200'])
        result = {}
        code = -1
        for apikey in apikeys:
            if keyword == '':
                params = {
                    'apikey': apikey,
                    'proxy': config['proxy'],
                    'r18': r18,
                    'num': num,
                    'size1200': size1200,
                }
            else:
                params = {
                    'apikey': config['apikey'],
                    'proxy': config['proxy'],
                    'keyword': keyword,
                    'r18': r18,
                    'num': num,
                    'size1200': size1200,
                }
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.lolicon.app/setu/', params=params) as rq:
                    result = await rq.read()
                    result = json.loads(result)
            code = result['code']
            if code == 0 or code == 404:
                break
        if code == 404:
            await bot.send(ev, '找不到此关键字的色图')
        elif code != 0:
            await bot.send(ev, 'setu获取失败')
        else:
            data = result['data']
            for setu in data:
                url = setu['url']
                pid = setu['pid']
                p = setu['p']
                title = setu['title']
                author = setu['author']
                ori_url = f'https://www.pixiv.net/artworks/{pid}'
                await send_to_group(ev.group_id, url, pid, p, title, author, ori_url, r18)
    elif config['group_api'] == 'acgmx':
        await bot.send_group_msg(group_id=group_id, message='获取中')
        headers = {
            'token': config['acgmx_token'],
            'referer': 'https://www.acgmx.com/'
        }
        url = 'https://api.acgmx.com/public/setu'
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as res:
                res = await res.read()
                res = json.loads(res)
        img_url = res['data']['large']
        pid = res['data']['illust']
        restrict = res['data']['restrict']
        title = res['data']['title']
        author = res['data']['user']['name']
        ori_url = f'https://www.pixiv.net/artworks/{pid}'
        await send_to_group_acgmx(ev.group_id, img_url, pid, restrict, title, author, ori_url, config['acgmx_token'])


async def down_img(url: str):
    print(f'downloading from {url}')
    filename = url.split('/')[-1]
    path = R.img('setuweb/').path
    async with aiohttp.ClientSession() as session:
        res = await session.get(url)
        f = open(f'{path}/{filename}', 'wb')
        res = await res.read()
        f.write(res)


async def down_acgmx_img(url: str, token: str):
    headers = {
        'token': token,
        'referer': 'https://www.acgmx.com/'
    }
    print(f'downloading from {url}')
    filename = url.split('/')[-1]
    path = R.img('setuweb/').path
    async with aiohttp.ClientSession(headers=headers) as session:
        res = await session.get(url)
        f = open(f'{path}/{filename}', 'wb')
        res = await res.read()
        f.write(res)


async def send_to_group(group_id: int, url: str, pid: str, p: str, title: str, author: str, ori_url: str, r18: bool):
    try:
        if not allowed_groups[str(group_id)]:
            return '此群不允许发送！'
    except KeyError:
        return '此群不允许发送！'
    if r18:
        try:
            if not r18_groups[str(group_id)]:
                return '此群不允许发送r18Setu！'
        except KeyError:
            return '此群不允许发送r18Setu！'
    filename = url.split('/')[-1]
    if not os.path.exists(R.img(f'setuweb/{filename}').path):
        await down_img(url)
    print(f'sending {filename}')
    img = R.img(f'setuweb/{filename}').cqcode
    msg = f'pid: {pid} p{p}\n标题: {title}\n作者: {author}\n原地址: {ori_url}\n{url}\n{img}'
    await bot.send_group_msg(group_id=group_id, message=msg)
    print(f'sended {filename}')
    return f'已发送到群{group_id}！'


async def send_to_group_acgmx(group_id: int, url: str, pid: str, p: str, title: str, author: str, ori_url: str, token: str):
    try:
        if not allowed_groups[str(group_id)]:
            return '此群不允许发送！'
    except KeyError:
        return '此群不允许发送！'
    else:
        filename = url.split('/')[-1]
        if not os.path.exists(R.img(f'setuweb/{filename}').path):
            await down_acgmx_img(url, token)
        print(f'sending {filename}')
        img = R.img(f'setuweb/{filename}').cqcode
        msg = f'pid: {pid} p{p}\n标题: {title}\n作者: {author}\n原地址: {ori_url}\n{img}'
        await bot.send_group_msg(group_id=group_id, message=msg)
        print(f'sended {filename}')
        return f'已发送到群{group_id}！'


def get_groups():
    groups = bot.get_group_list()
    return groups
