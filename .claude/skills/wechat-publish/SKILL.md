---
name: wechat-publish
description: 将博客文章发布到微信公众号。当用户说"发布到微信"、"推送到公众号"时使用。
disable-model-invocation: true
argument-hint: "[article-path]"
allowed-tools:
  - Bash
  - Read
  - Edit
---

# 微信公众号发布 Skill

将博客文章发布到微信公众号平台。

## 执行步骤

### 1. 验证文章路径

检查用户提供的文章路径是否存在：
- 如果用户提供了路径参数 `$ARGUMENTS`，使用该路径
- 如果未提供，询问用户要发布哪篇文章

### 2. 检查配置

确认环境变量已配置：
```bash
echo "检查微信公众号配置..."
if [ -z "$WECHAT_APPID" ] || [ -z "$WECHAT_SECRET" ]; then
    echo "错误：未配置微信公众号凭证"
    echo "请参考 .claude/skills/wechat-publish/README.md 进行配置"
    exit 1
fi
```

### 3. 执行发布

调用发布脚本：
```bash
bash .claude/skills/wechat-publish/scripts/publish.sh "$ARGUMENTS"
```

### 4. 处理结果

- 如果发布成功，显示 media_id 和后续操作提示
- 如果发布失败，显示错误信息和解决建议
- 自动更新对应的 .CLAUDE.md 文件记录发布信息

## 发布流程说明

1. **读取文章**：读取 markdown 文件内容
2. **转换格式**：使用 Python 脚本将 Markdown 转换为微信公众号 HTML
3. **提取元数据**：自动提取标题、摘要
4. **上传封面**：如果存在 `文章名_thumb.jpg`，自动上传为封面
5. **发布素材**：调用微信 API 创建图文素材
6. **记录发布**：在 .CLAUDE.md 中记录发布时间和 media_id

## 使用示例

```bash
# 发布指定文章
/wechat-publish zh-cn/openwrt/智能网络路由.md

# 不带参数调用，会提示选择文章
/wechat-publish
```

## 注意事项

1. **首次使用**：需要先配置环境变量（参考 README.md）
2. **封面图片**：可选，命名为 `文章名_thumb.jpg` 放在同目录
3. **内容审核**：发布后需要通过微信的内容审核
4. **素材管理**：发布的是素材，不是直接群发，需要在微信后台操作群发
5. **原文链接**：自动设置为 blog.codingdie.com 对应文章

## 错误处理

如果遇到错误：
- **access_token 失败**：检查 AppID 和 AppSecret 是否正确
- **上传失败**：检查图片大小（不超过 2MB）
- **发布失败**：检查标题长度（不超过 64 字符）、摘要长度（不超过 120 字符）

详细配置和故障排查请参考：[README.md](README.md)
