# Hoshinobot 在线setu插件
## 简介
本插件可调用loliconapi在线查找setu并发送
## 安装方法
1. 在hoshino/modules文件夹下使用git clone本项目
2. 在config.json中添加(可添加多个)自己申请的apikey(<https://api.lolicon.app/>)
3. (可选)修改config.json中的proxy（代理）
4. 在hoshino/config/\_\_bot\_\_.py中添加本插件
## 指令说明
|指令|功能|
|---|---|
|setuhelp|查看帮助|
|groupallow|允许当前群发送setu|
|groupforbid|禁止当前群发送setu|

groupallow和groupforbid只有管理员以上及主人才能使用\
本插件图片发送前下载至资源文件夹中img/setuweb\
若图片已存在不下载直接发送\
若有多个apikey 失败时将自动切换\
若全部失败 显示最后一个的失败信息