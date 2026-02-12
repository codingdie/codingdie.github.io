# 微信公众号发布使用示例

## 快速开始

### 1. 配置环境变量

```bash
# 编辑 ~/.bashrc 或 ~/.zshrc
export WECHAT_APPID="wxXXXXXXXXXXXXXXXX"
export WECHAT_SECRET="your_secret_here"

# 重新加载配置
source ~/.bashrc
```

### 2. 准备文章

确保文章文件存在：
```
zh-cn/openwrt/智能网络路由.md
zh-cn/openwrt/智能网络路由.CLAUDE.md
```

可选：准备封面图片（推荐尺寸 900x500）：
```
zh-cn/openwrt/智能网络路由_thumb.jpg
```

### 3. 发布文章

在 Claude Code 中执行：
```bash
/wechat-publish zh-cn/openwrt/智能网络路由.md
```

## 完整示例

### 示例 1：发布带封面的文章

```bash
# 1. 准备封面图片
cp cover.jpg zh-cn/openwrt/智能网络路由_thumb.jpg

# 2. 发布
/wechat-publish zh-cn/openwrt/智能网络路由.md
```

输出示例：
```
==========================================
微信公众号发布工具
==========================================
文章: /home/user/blog/zh-cn/openwrt/智能网络路由.md

[INFO] 获取 access_token...
[INFO] access_token 获取成功: 65_xxxxxxxxxxxxx...
[INFO] 转换 Markdown 到微信 HTML...
[INFO] 文章标题: st网络管家：智能学习，纵享丝滑网络
[INFO] 文章摘要: 这是一篇介绍 st-dns 和 st-proxy 两个网络优化工具...

[INFO] 上传封面图片: zh-cn/openwrt/智能网络路由_thumb.jpg
[INFO] 封面图片上传成功: xxxxxxxxxxxxx
[INFO] 发布图文素材...
[INFO] 图文素材发布成功: xxxxxxxxxxxxx
[INFO] 更新 CLAUDE.md 发布记录...
[INFO] CLAUDE.md 更新完成

==========================================
发布成功！
==========================================
Media ID: xxxxxxxxxxxxx
原文链接: https://blog.codingdie.com/#/zh-cn/openwrt/智能网络路由

下一步：
1. 登录微信公众平台查看素材
2. 在素材管理中找到刚发布的图文
3. 可以进行群发或预览
```

### 示例 2：发布不带封面的文章

```bash
/wechat-publish zh-cn/blog/my-article.md
```

输出示例：
```
[INFO] 获取 access_token...
[INFO] access_token 获取成功: 65_xxxxxxxxxxxxx...
[INFO] 转换 Markdown 到微信 HTML...
[WARN] 未找到封面图片，将不显示封面
[INFO] 发布图文素材...
[INFO] 图文素材发布成功: xxxxxxxxxxxxx
```

### 示例 3：直接使用脚本

也可以直接调用脚本：
```bash
bash .claude/skills/wechat-publish/scripts/publish.sh zh-cn/openwrt/智能网络路由.md
```

## 发布后的操作

### 在微信公众平台查看

1. 登录 https://mp.weixin.qq.com
2. 进入"素材管理" -> "图文消息"
3. 找到刚发布的文章
4. 可以进行以下操作：
   - 预览：发送到手机预览效果
   - 编辑：微调格式和内容
   - 群发：发送给所有关注者
   - 分享：获取分享链接

### 群发文章

在微信公众平台：
1. 进入"群发功能"
2. 选择"图文消息"
3. 从素材库选择刚发布的文章
4. 选择群发对象（全部用户或标签用户）
5. 确认群发

## 发布记录

发布成功后，会在对应的 `.CLAUDE.md` 文件中自动添加记录：

```markdown
## 修改历史

### 2026-02-13 15:30:00 - 发布到微信公众号

- media_id: xxxxxxxxxxxxx
- 发布状态: 成功
```

## 常见问题

### Q1: 如何测试发布功能？

A: 可以先用测试文章发布，然后在微信公众平台预览效果。

### Q2: 发布后可以修改吗？

A: 可以在微信公众平台的素材管理中编辑，但已群发的文章无法修改。

### Q3: 如何批量发布多篇文章？

A: 可以写一个循环脚本：
```bash
for article in zh-cn/openwrt/*.md; do
    /wechat-publish "$article"
    sleep 5  # 避免频率限制
done
```

### Q4: 发布失败怎么办？

A: 查看错误信息，常见原因：
- access_token 过期：重新获取
- 标题或摘要过长：修改文章
- 图片过大：压缩图片
- 网络问题：检查网络连接

## 高级用法

### 自定义样式

修改 `scripts/md2wechat.py` 中的样式定义：
```python
self.styles = {
    'h1': 'font-size: 24px; ...',
    'h2': 'font-size: 20px; ...',
    # 自定义其他样式
}
```

### 批量处理图片

如果文章中有多张图片，需要先上传到微信服务器：
```bash
# TODO: 实现图片批量上传功能
```

### 定时发布

结合 cron 实现定时发布：
```bash
# 每天 9:00 发布
0 9 * * * cd /path/to/blog && /wechat-publish latest.md
```

## 参考资料

- [微信公众平台开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [素材管理接口](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html)
- [Markdown 转换最佳实践](https://github.com/lyricat/wechat-format)
