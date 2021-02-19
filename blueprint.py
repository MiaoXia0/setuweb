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
    apikeys = config['apikey']
    result = {}
    code = -1
    for apikey in apikeys:
        if keyword == '':
            params = {
                'apikey': apikey,
                'proxy': config['proxy'],
                'r18': form['r18'],
                'num': form['num'],
                'size1200': form['size1200'],
            }
        else:
            params = {
                'apikey': config['apikey'],
                'proxy': config['proxy'],
                'keyword': keyword,
                'r18': form['r18'],
                'num': form['num'],
                'size1200': form['size1200'],
            }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.lolicon.app/setu/', params=params) as rq:
                result = await rq.read()
                result = json.loads(result)
        code = result['code']
        if code == 0:
            break
    msg = result['msg']
    quota = result['quota']
    quota_min_ttl = result['quota_min_ttl']
    count = result['count']
    data = result['data']
    return await render_template('result.html',
                                 code=code,
                                 msg=msg,
                                 quota=quota,
                                 quota_min_ttl=quota_min_ttl,
                                 count=count,
                                 data=data,
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
    group_id = int(form['group_id'])
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
    pid = form['pid']
    p = form['p']
    url = form['url']
    ori_url = f'https://www.pixiv.net/artworks/{pid}'
    title = form['title']
    author = form['author']
    group_id = int(form['group_id'])
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
