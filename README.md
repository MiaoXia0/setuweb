# Hoshinobot 在线setu插件
## 简介
本插件可调用lolicon api或acgmx api查找setu并可发送到bot所在群中\
支持在线查找以及群内调用\
在线使用地址为http://bot地址/setu
可通过setuhelp指令获取\
群内使用方法见指令说明
支持私聊（需魔改Hoshinobot源码）\
私聊不撤回，不检测r18\
佛系编程 想要什么功能建议自己改

### Hoshinobot魔改

1. 在priv.py中找到不允许私聊的注释(第78行)将False改为True
2. 找到msghandler.py中第8行的if event.detail_type != 'group':\
下一行的return改为pass 或者删除整个if块(第8行, 第9行)

## 安装方法
1. 在hoshino/modules文件夹下使用git clone本项目
2. 在config.json中添加(可添加多个)lolicon的apikey(<https://api.lolicon.app/>)
3. 在config.json中添加acgmx的apikey(<https://www.acgmx.com/>)
4. (可选)修改config.json中的proxy（代理）
5. 在hoshino/config/\_\_bot\_\_.py中添加本插件

## 指令说明
|指令|功能|
|---|---|
|setuhelp|查看帮助|
|setpsw|设置本群密码|
|setuallow|允许当前群发送setu|
|setuforbid|禁止当前群发送setu|
|r18allow|允许当前群发送r18setu|
|r18forbid|禁止当前群发送r18setu|
|withdrawon|开启当前群撤回|
|withdrawoff|关闭当前群撤回|
|setwithdraw|时间设置撤回时间(秒)|
|setpsw|设置当前群的web端密码|
|antishielding(0关\\类型1\\2\\3)|查看或设置反和谐类型|
|来\\发\\给(数量)份\\点\\张\\幅(R\\r18)(关键字)\\涩\\瑟\\色图|群内色图括号内容可选|

各种群内开关只有管理员以上及主人才能使用\
r18选项仅对lolicon api有效\
群内撤回默认关闭\
撤回时间为全局设置 仅主人可以设置\
撤回时间默认60秒 设为0为全局关闭撤回\
本插件图片发送前下载至资源文件夹中img/setuweb\
若图片已存在不下载直接发送\
若有多个lolicon apikey 失败时将自动切换\
若全部失败 显示最后一个的失败信息

## config说明
|key|value|类型|
|---|---|---|
|apikey|lolicon.app的apikey|字符串列表|
|size1200|群内触发时是否size1200|布尔|
|proxy|lolicon.app的代理|字符串|
|acgmx_token|acgmx的token|字符串|
|group_api|群内触发setu所用的api|字符串("lolicon"/"acgmx")|
|withdraw|撤回时间 0为全局关闭|整数|
|antishielding|反和谐类型0关1随机像素2旋转3混合|整数(0\\1\\2\\3)|
|url|自定义页面url代替说明中的http://ip:port/|字符串|
|forward|是否启用卡片消息|布尔|
group_api为acg_mx时只能获取单张随机setu

# 提问的智慧
<https://github.com/ryanhanwu/how-to-ask-questions-the-smart-way>