# Hoshinobot 在线setu插件
## 简介
本插件可调用loliconapi在线查找setu并发送
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
|groupallow|允许当前群发送setu|
|groupforbid|禁止当前群发送setu|
|r18allow|允许当前群发送r18setu|
|r18forbid|禁止当前群发送r18setu|
|来\\发\\给(数量)份\\点\\张\\幅(R\\r18)(关键字)\\涩\\瑟\\色图|群内色图括号内容可选|

groupallow和groupforbid只有管理员以上及主人才能使用\
r18选项仅对lolicon api有效
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

group_api为acg_mx时只能获取单张随机setu 