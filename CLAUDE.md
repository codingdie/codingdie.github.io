# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog site hosted on GitHub Pages using Docsify. The site is primarily in Chinese and covers technical topics including OpenWrt, IM (Instant Messaging) system design, P2P networking, and personal essays.

**Domain**: blog.codingdie.com

## Architecture

### Docsify Static Site

- **Framework**: Docsify v4 (client-side rendering)
- **No build process**: Docsify renders markdown files directly in the browser
- **Configuration**: All site configuration is in [index.html](index.html)
- **Deployment**: GitHub Pages (`.nojekyll` file prevents Jekyll processing)

### Content Structure

```
/
├── index.html              # Main entry point with Docsify configuration
├── _navbar.md              # Top navigation bar (language switcher)
├── _sidebar.md             # Root sidebar navigation
├── zh-cn/                  # Chinese content (primary)
│   ├── openwrt/           # OpenWrt tutorials
│   ├── im/                # IM system design articles
│   ├── p2p/               # P2P networking articles
│   │   ├── nat/          # NAT traversal subtopic
│   │   └── tunnel/       # Tunneling subtopic
│   ├── blog/              # Personal essays
│   └── tianya/            # Tianya forum posts collection
└── en/                     # English content (minimal)
```

### Navigation System

- Each directory has its own `_sidebar.md` for section-specific navigation
- `_navbar.md` is shared across all pages (configured via alias in index.html)
- Docsify automatically loads the appropriate sidebar based on the current path

## Content Management

### ⚠️ 重要：博客文章文件结构

**这是一个博客文章项目，每个博客由两个文件组成：**

1. **xxx.md** - 博客内容文件（发布的正式内容）
2. **xxx.CLAUDE.md** - 博客修改意见和内容总结文件（记录讨论、修改建议、内容摘要）

**工作流程：**
- 每次修改博客时，都需要同时更新这两个文件
- xxx.CLAUDE.md 用于记录与 Claude 的讨论内容、修改意见、优化建议和内容总结
- 这样可以保持修改历史和思路的连续性

### Adding New Articles

1. Create markdown file in the appropriate topic directory (e.g., `zh-cn/im/04.md`)
2. Update the corresponding `_sidebar.md` to add navigation link
3. Follow existing naming conventions (numbered files like `01.md`, `02.md`)

### Creating New Topic Sections

1. Create new directory under `zh-cn/` (e.g., `zh-cn/new-topic/`)
2. Add `README.md` as the section landing page
3. Add `_sidebar.md` for section navigation
4. Update root `_sidebar.md` to link to the new section

### Markdown Files

- Use standard markdown syntax
- Docsify supports emoji plugin (`:emoji_name:`)
- Images should use relative paths
- Internal links use Docsify routing format: `/zh-cn/topic/article`

## Docsify Configuration

Key settings in [index.html](index.html):

- **loadSidebar**: true - Enables custom sidebar navigation
- **loadNavbar**: true - Enables top navigation bar
- **subMaxLevel**: 12 - Deep heading nesting support
- **autoHeader**: true - Auto-generates headers from sidebar
- **search**: 'auto' - Built-in search functionality
- **pagination**: Enabled with Chinese labels
- **count**: Word count plugin enabled
- **ga**: Google Analytics tracking (G-TLS9EHY08Z)

## Deployment

This site deploys automatically via GitHub Pages:

1. Push changes to the `main` branch
2. GitHub Pages serves the site directly (no build step)
3. Changes are live immediately after push

**No build commands needed** - Docsify renders everything client-side.

## Local Development

To preview locally:

```bash
# Install docsify-cli globally (one-time setup)
npm i docsify-cli -g

# Serve the site locally
docsify serve .

# Site will be available at http://localhost:3000
```

Alternatively, use any static file server:

```bash
python -m http.server 8000
# or
npx serve .
```

## Git Workflow

- Main branch: `main`
- Direct commits to main (no PR process for personal blog)
- Commit messages typically just "update"

## Important Notes

- The `zh-cn/private/` directory is untracked (contains private drafts)
- ICP filing number in footer: 京ICP备14008864号-3
- Ad removal script runs every second to clean up Disqus ads
- All CDN resources loaded from jsdelivr.net and unpkg.com

## Claude 工作习惯

### 语言偏好

默认使用中文进行交流和编写代码注释。

### Git 配置与规范
**重要：所有 Git 操作必须遵循以下规范**

- 用户名：codingdie
- 邮箱：codingdie@gmail.com
- 所有提交必须使用此身份
- **不要在 commit message 中添加 Co-Authored-By 标签**
- 修改代码后**不要自动 commit**
- 等待用户明确说"提交"、"commit"或"push"后，再执行 `git commit` + `git push`
- 可以使用 `git diff` 或 `git status` 查看改动，但不要自动提交
