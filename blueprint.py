from .bot import get_groups, send_to_group, send_to_group_acgmx, group_psw
from quart import Blueprint, render_template, request
import aiohttp
import os
import asyncio

try:
    import ujson as json
except ImportError:
    import json

curr_dir = os.path.dirname(__file__)
bp = Blueprint('setu', 'setuweb', static_folder=f'{curr_dir}/static', template_folder=f'{curr_dir}/templates')
config = json.load(open(f'{curr_dir}/config.json', 'r'))


@bp.route('/', methods=['GET'])
async def setuindex():
    return await render_template('index.html')


@bp.route('/result', methods=['POST'])
async def seturesult():
    form = await request.form
    groups = await get_groups()
    keyword = form['keyword']
    uids = form['uids'].strip()
    if uids != '':
        uids = uids.split(' ')
        try:
            uids = [int(uid) for uid in uids]
        except ValueError:
            uids = []
    else:
        uids = []

    tags = form['tags'].strip()
    if tags != '':
        tags = tags.split(' ')
    else:
        tags = []
    result = {}
    code = -1
    # for apikey in apikeys:
    # if keyword == '':
    #     params = {
    #         'apikey': apikey,
    #         'proxy': config['proxy'],
    #         'r18': form['r18'],
    #         'num': form['num'],
    #         'size': form['size'],
    #     }
    # else:
    #     params = {
    #         'apikey': config['apikey'],
    #         'proxy': config['proxy'],
    #         'keyword': keyword,
    #         'r18': form['r18'],
    #         'num': form['num'],
    #         'size': form['size'],
    #     }
    datas = {
        'proxy': config['proxy'],
        'r18': form['r18'],
        'num': form['num'],
        'size': form['size']
    }
    if keyword != '':
        datas['keyword'] = keyword
    if uids:
        datas['uid'] = uids
    if tags:
        datas['tag'] = tags
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.lolicon.app/setu/v2', data=datas) as rq:
            result = await rq.read()
            result = json.loads(result)
    err = result['error']
    data = result['data']
    return await render_template('result.html',
                                 err=err,
                                 data=data,
                                 size=form['size'],
                                 groups=groups)


@bp.route('/send', methods=['POST'])
async def send():
    form = await request.form
    group_id = form['group_id']
    psw = form['psw']
    try:
        password = group_psw[group_id]
    except KeyError:
        return '请先在群内设置密码'
    if psw != password:
        return '密码错误'
    group_id = int(group_id)
    r18 = form['r18'] == 'True'  # 前端获取的是字符串 比较判断
    url = form['url']
    pid = form['pid']
    p = form['p']
    ori_url = f'https://www.pixiv.net/artworks/{pid}'
    title = form['title']
    author = form['author']
    result = await send_to_group(group_id, url, pid, p, title, author, ori_url, r18)
    return result


@bp.route('/acgmxsend', methods=['POST'])
async def acgmxsend():
    form = await request.form
    group_id = form['group_id']
    psw = form['psw']
    try:
        password = group_psw[group_id]
    except KeyError:
        return '请先在群内设置密码'
    if psw != password:
        return '密码错误'
    pid = form['pid']
    p = form['p']
    url = form['url']
    ori_url = f'https://www.pixiv.net/artworks/{pid}'
    title = form['title']
    author = form['author']
    group_id = int(group_id)
    result = await send_to_group_acgmx(group_id, url, pid, p, title, author, ori_url, config['acgmx_token'])
    return result


@bp.route('/acgmx', methods=['GET'])
async def acgmx():
    groups = await get_groups()
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
    pageCount = res['data']['pageCount']
    xRestrict = res['data']['xRestrict']
    restrict = res['data']['restrict']
    title = res['data']['title']
    author = res['data']['user']['name']
    uid = res['data']['user']['id']
    img_type = img_url.split('.')[-1]
    if pageCount == '1':
        pixiv_cat_url = f'https://pixiv.cat/{pid}.{img_type}'
    else:
        pixiv_cat_url = f'https://pixiv.cat/{pid}-{xRestrict}.{img_type}'
    return await render_template('acgmx.html',
                                 img_url=img_url,
                                 pixiv_cat_url=pixiv_cat_url,
                                 pid=pid,
                                 p=restrict,
                                 title=title,
                                 author=author,
                                 uid=uid,
                                 groups=groups)
