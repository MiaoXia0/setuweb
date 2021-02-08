from .bot import get_groups, send_to_group, send_to_group_acgmx
from quart import Blueprint, render_template, request
import aiohttp
import os

try:
    import ujson as json
except ImportError:
    import json

curr_dir = os.path.dirname(__file__)
bp = Blueprint('setu', 'setuweb', static_folder=f'{curr_dir}/static', template_folder=f'{curr_dir}/templates')
config = json.load(open(f'{curr_dir}/config.json'))


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
            kwargs = {
                'apikey': apikey,
                'proxy': config['proxy'],
                'r18': form['r18'],
                'num': form['num'],
                'size1200': form['size1200'],
            }
        else:
            kwargs = {
                'apikey': config['apikey'],
                'proxy': config['proxy'],
                'keyword': keyword,
                'r18': form['r18'],
                'num': form['num'],
                'size1200': form['size1200'],
            }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.lolicon.app/setu/', kwargs=kwargs) as rq:
                result = json.loads(rq.text)
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
    url = form['url']
    pid = form['pid']
    p = form['p']
    ori_url = f'https://www.pixiv.net/artworks/{pid}'
    title = form['title']
    author = form['author']
    group_id = int(form['group_id'])
    result = await send_to_group(group_id, url, pid, p, title, author, ori_url)
    return result


@bp.route('/acgmxsend', methods=['POST'])
async def acgmxsend():
    form = await request.form
    url = form['url']
    pid = form['pid']
    ori_url = f'https://www.pixiv.net/artworks/{pid}'
    title = form['title']
    author = form['author']
    group_id = int(form['group_id'])
    result = await send_to_group_acgmx(group_id, url, pid, title, author, ori_url, config['acgmx_token'])
    return result


@bp.route('/acgmx', methods=['GET'])
async def acgmx():
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
    title = res['data']['title']
    author = res['data']['user']['name']
    uid = res['data']['user']['id']
    return render_template('acgmx.html', img_url=img_url, pid=pid, title=title, author=author, uid=uid)
