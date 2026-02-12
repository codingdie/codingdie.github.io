# 微信公众号发布配置指南

## 前置条件

1. **微信公众号**：需要有已认证的微信公众号（订阅号或服务号）
2. **开发者权限**：需要有公众号的开发者权限
3. **依赖工具**：
   - `curl` - HTTP 请求工具
   - `jq` - JSON 处理工具
   - `pandoc`（可选）- Markdown 转 HTML 工具

## 配置步骤

### 1. 获取微信公众号凭证

登录微信公众平台：https://mp.weixin.qq.com

1. 进入"开发" -> "基本配置"
2. 获取 **AppID** 和 **AppSecret**
3. 将服务器 IP 地址加入白名单

### 2. 设置环境变量

在你的 shell 配置文件中添加（`~/.bashrc` 或 `~/.zshrc`）：

```bash
export WECHAT_APPID="你的AppID"
export WECHAT_SECRET="你的AppSecret"
```

然后重新加载配置：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

### 3. 验证配置

```bash
# 测试获取 access_token
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$WECHAT_APPID&secret=$WECHAT_SECRET"
```

如果返回包含 `access_token` 字段，说明配置成功。

## 使用方法

### 发布文章

```bash
# 在 Claude Code 中使用
/wechat-publish zh-cn/openwrt/智能网络路由.md
```

### 发布流程

1. Claude 会读取文章内容和元信息
2. 将 Markdown 转换为微信公众号支持的 HTML 格式
3. 处理文章中的图片（上传到微信服务器）
4. 调用微信 API 创建图文素材
5. 在 .CLAUDE.md 中记录发布信息

## 微信公众号 API 限制

- **access_token 有效期**：7200 秒（2 小时）
- **图片大小限制**：不超过 2MB
- **标题长度**：不超过 64 个字符
- **摘要长度**：不超过 120 个字符
- **调用频率**：每天有调用次数限制

## 注意事项

1. **内容审核**：发布的内容需要符合微信公众平台运营规范
2. **原创声明**：如需声明原创，需要在微信后台手动操作
3. **群发限制**：订阅号每天可群发 1 次，服务号每月可群发 4 次
4. **素材管理**：发布后的素材会保存在微信公众号的素材库中

## 故障排查

### 问题 1：获取 access_token 失败

- 检查 AppID 和 AppSecret 是否正确
- 检查服务器 IP 是否在白名单中
- 检查网络连接是否正常

### 问题 2：图片上传失败

- 检查图片大小是否超过 2MB
- 检查图片格式是否支持（jpg, png）
- 检查图片路径是否正确

### 问题 3：发布失败

- 检查标题和摘要长度是否超限
- 检查内容是否包含敏感词
- 检查 access_token 是否过期

## 相关链接

- [微信公众平台开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [素材管理接口](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html)
- [群发接口](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html)
