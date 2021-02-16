from nonebot import get_bot
from hoshino import Service, R
from hoshino.typing import HoshinoBot, CQEvent
from hoshino.priv import check_priv, ADMIN, SUPERUSER
import requests
import os
import aiohttp
import asyncio

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

r18_path = os.path.dirname(__file__) + '/r18_groups.json'
if not os.path.exists(r18_path):
    r18_groups = {}
    json.dump(r18_groups, open(r18_path, 'w'))
else:
    r18_groups = json.load(open(r18_path, 'r'))

withdraw_path = os.path.dirname(__file__) + '/withdraw_groups.json'
if not os.path.exists(withdraw_path):
    withdraw_groups = {}
    json.dump(withdraw_groups, open(withdraw_path, 'w'))
else:
    withdraw_groups = json.load(open(withdraw_path, 'r'))

sv = Service('setuweb')
ip = json.loads(requests.get('https://jsonip.com/').text)['ip']
bot = get_bot()
port = bot.config.PORT
curr_dir = os.path.dirname(__file__)
config = json.load(open(f'{curr_dir}/config.json', 'r'))

if port == 80:
    setu_url = f'http://{ip}/setu/'
else:
    setu_url = f'http://{ip}:{port}/setu/'

help_str = f'''本插件为在线setu插件
进入{setu_url}开始使用本插件
输入setuallow允许本群发送色图
输入setuforbid禁止本群发送色图
输入r18allow允许本群发送r18色图
输入r18forbid禁止本群发送r18色图
输入withdrawon开启本群撤回
输入withdrawoff关闭本群撤回
输入setwithdraw+时间设置撤回时间(秒) 0为全局关闭撤回
输入来\\发\\给(数量)份\\点\\张\\幅(R\\r18)(关键字)\\涩\\瑟\\色图 在群内获取色图'''


@sv.on_fullmatch('setuhelp')
async def setuhelp(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, help_str)


@sv.on_fullmatch('setuallow')
async def setuallow(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    allowed_groups[str(group_id)] = True
    json.dump(allowed_groups, open(allow_path, 'w'))
    await bot.send(ev, f'已允许{group_id}')


@sv.on_fullmatch('setuforbid')
async def setuforbid(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    allowed_groups[str(group_id)] = False
    json.dump(allowed_groups, open(allow_path, 'w'))
    await bot.send(ev, f'已禁止{group_id}')


@sv.on_fullmatch('r18allow')
async def setuallow(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    r18_groups[str(group_id)] = True
    json.dump(r18_groups, open(r18_path, 'w'))
    await bot.send(ev, f'已允许{group_id}r18')


@sv.on_fullmatch('r18forbid')
async def setuforbid(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    r18_groups[str(group_id)] = False
    json.dump(r18_groups, open(r18_path, 'w'))
    await bot.send(ev, f'已禁止{group_id}r18')


@sv.on_fullmatch('withdrawon')
async def withdrawon(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    withdraw_groups[str(group_id)] = True
    json.dump(withdraw_groups, open(withdraw_path, 'w'))
    await bot.send(ev, f'已开启{group_id}撤回')


@sv.on_fullmatch('withdrawoff')
async def withdrawoff(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] != 'group':
        return
    if not check_priv(ev, ADMIN):
        await bot.send(ev, f'管理员以上才能使用')
        return
    group_id = ev.group_id
    withdraw_groups[str(group_id)] = False
    json.dump(withdraw_groups, open(withdraw_path, 'w'))
    await bot.send(ev, f'已关闭{group_id}撤回')


@sv.on_prefix('setwithdraw')
async def setwithdraw(bot: HoshinoBot, ev: CQEvent):
    if not check_priv(ev, SUPERUSER):
        await bot.send(ev, f'机器人主人才能使用')
        return
    time = ev.message.extract_plain_text()
    try:
        time = int(time)
    except ValueError:
        await bot.send(ev, '请输入setwithdraw+数字')
        return
    if time < 0:
        await bot.send(ev, '请输入setwithdraw+大于0的数字')
        return
    config['withdraw'] = time
    json.dump(config, open(f'{curr_dir}/config.json', 'w'))
    await bot.send(ev, f'已设置撤回时间为{time}秒')


@sv.on_rex(r'^[来发给](\d*)?[份点张幅]([Rr]18)?(.*)?[涩瑟色]图$')
async def group_setu(bot: HoshinoBot, ev: CQEvent):
    if ev['message_type'] == 'group':
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
        try:
            num = int(num)
        except ValueError:
            if num == '':
                num = 1
            else:
                await bot.send(ev, '请输入正确的数字')
                return
        else:
            if num > 10:
                num = 10
            elif num < 1:
                num = 1
        r18 = int(ev['match'].group(2) is not None)
        if ev['message_type'] == 'group':
            if r18 == 1:
                try:
                    if not r18_groups[str(group_id)]:
                        await bot.send_group_msg(group_id=group_id, message='此群不允许发送r18Setu！')
                        return
                except KeyError:
                    await bot.send_group_msg(group_id=group_id, message='此群不允许发送r18Setu！')
                    return
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
            sending = []
            data = result['data']
            for setu in data:
                url = setu['url']
                pid = setu['pid']
                p = setu['p']
                title = setu['title']
                author = setu['author']
                ori_url = f'https://www.pixiv.net/artworks/{pid}'
                if ev['message_type'] == 'group':
                    sending.append(send_to_group(ev.group_id, url, pid, p, title, author, ori_url, bool(r18)))
                else:
                    sending.append(send_to_private(ev.user_id, url, pid, p, title, author, ori_url))
            await asyncio.gather(*sending)


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
        if ev['message_type'] == 'group':
            await send_to_group_acgmx(ev.group_id, img_url, pid, restrict, title, author, ori_url,
                                      config['acgmx_token'])
        else:
            await send_to_private_acgmx(ev.user_id, url, pid, restrict, title, author, ori_url, config['acgmx_token'])


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


async def format_msg(url: str, pid: str, p: str, title: str, author: str, ori_url: str):
    # filename = url.split('/')[-1]
    # img = R.img(f'setuweb/{filename}').cqcode
    msg = f'pid: {pid} p{p}\n标题: {title}\n作者: {author}\n原地址: {ori_url}\n{url}'
    return msg


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
    msg = await format_msg(url, pid, p, title, author, ori_url)
    await bot.send_group_msg(group_id=group_id, message=msg)
    if not os.path.exists(R.img(f'setuweb/{filename}').path):
        await down_img(url)
    # msg = await format_msg(url, pid, p, title, author, ori_url)
    filename = url.split('/')[-1]
    img = R.img(f'setuweb/{filename}').cqcode
    result = await bot.send_group_msg(group_id=group_id, message=img)
    withdraw = int(config['withdraw'])
    ifwithdraw = True
    try:
        if not withdraw_groups[str(group_id)]:
            ifwithdraw = False
    except KeyError:
        ifwithdraw = False
    if ifwithdraw and withdraw and withdraw > 0:
        print(f'{withdraw}秒后撤回')
        await asyncio.sleep(withdraw)
        await bot.delete_msg(message_id=result['message_id'])
        return f'已发送到群{group_id}并撤回！'
    return f'已发送到群{group_id}！'


async def send_to_group_acgmx(group_id: int, url: str, pid: str, p: str, title: str, author: str, ori_url: str,
                              token: str):
    try:
        if not allowed_groups[str(group_id)]:
            return '此群不允许发送！'
    except KeyError:
        return '此群不允许发送！'
    else:
        msg = await format_msg(url, pid, p, title, author, ori_url)
        await bot.send_group_msg(group_id=group_id, message=msg)
        filename = url.split('/')[-1]
        if not os.path.exists(R.img(f'setuweb/{filename}').path):
            await down_acgmx_img(url, token)
        img = R.img(f'setuweb/{filename}').cqcode
        result = await bot.send_group_msg(group_id=group_id, message=img)
        withdraw = int(config['withdraw'])
        ifwithdraw = True
        try:
            if not withdraw_groups[str(group_id)]:
                ifwithdraw = False
        except KeyError:
            ifwithdraw = False
        if ifwithdraw and withdraw and withdraw > 0:
            print(f'{withdraw}秒后撤回')
            await asyncio.sleep(withdraw)
            await bot.delete_msg(message_id=result['message_id'])
            return f'已发送到群{group_id}并撤回！'
        return f'已发送到群{group_id}！'


async def send_to_private(user_id: int, url: str, pid: str, p: str, title: str, author: str, ori_url: str):
    msg = await format_msg(url, pid, p, title, author, ori_url)
    await bot.send_private_msg(user_id=user_id, message=msg)
    filename = url.split('/')[-1]
    if not os.path.exists(R.img(f'setuweb/{filename}').path):
        await down_img(url)
    img = R.img(f'setuweb/{filename}').cqcode
    await bot.send_private_msg(user_id=user_id, message=img)


async def send_to_private_acgmx(user_id: int, url: str, pid: str, p: str, title: str, author: str, ori_url: str,
                                token: str):
    msg = await format_msg(url, pid, p, title, author, ori_url)
    await bot.send_private_msg(user_id=user_id, message=msg)
    filename = url.split('/')[-1]
    if not os.path.exists(R.img(f'setuweb/{filename}').path):
        await down_acgmx_img(url, token)

    img = R.img(f'setuweb/{filename}').cqcode
    await bot.send_private_msg(user_id=user_id, message=img)


def get_groups():
    groups = bot.get_group_list()
    return groups
