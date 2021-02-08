from nonebot import get_bot
from hoshino import R
from .blueprint import bp
import os
try:
    import ujson as json
except ImportError:
    import json

path = R.img('setuweb/').path

if not os.path.exists(path):
    os.makedirs(path)
allow_path = os.path.dirname(__file__) + '/allowed_groups.json'
if not os.path.exists(allow_path):
    allowed_groups = {}
    json.dump(allowed_groups, open(allow_path, 'w'))
else:
    allowed_groups = json.load(open(allow_path, 'r'))

bot = get_bot()
app = bot.server_app
app.register_blueprint(bp, '/setu')  # 注册蓝图
