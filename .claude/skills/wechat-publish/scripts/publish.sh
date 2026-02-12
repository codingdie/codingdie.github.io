#!/bin/bash

# 微信公众号发布辅助脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    local missing_deps=()

    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi

    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi

    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "缺少依赖工具: ${missing_deps[*]}"
        log_error "请安装: sudo apt-get install ${missing_deps[*]}"
        exit 1
    fi
}

# 检查环境变量
check_env() {
    if [ -z "$WECHAT_APPID" ] || [ -z "$WECHAT_SECRET" ]; then
        log_error "请设置环境变量 WECHAT_APPID 和 WECHAT_SECRET"
        log_error "参考: .claude/skills/wechat-publish/README.md"
        exit 1
    fi
}

# 获取 access_token
get_access_token() {
    log_info "获取 access_token..."

    local response=$(curl -s -X GET \
        "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$WECHAT_APPID&secret=$WECHAT_SECRET")

    local access_token=$(echo "$response" | jq -r '.access_token')

    if [ "$access_token" = "null" ] || [ -z "$access_token" ]; then
        log_error "获取 access_token 失败"
        echo "$response" | jq '.'
        exit 1
    fi

    log_info "access_token 获取成功: ${access_token:0:20}..."
    echo "$access_token"
}

# 上传封面图片
upload_thumb() {
    local thumb_path=$1
    local access_token=$2

    if [ ! -f "$thumb_path" ]; then
        log_warn "封面图片不存在: $thumb_path"
        log_warn "将使用默认封面"
        return 1
    fi

    log_info "上传封面图片: $thumb_path"

    local response=$(curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$access_token&type=image" \
        -F "media=@$thumb_path")

    local media_id=$(echo "$response" | jq -r '.media_id')

    if [ "$media_id" = "null" ] || [ -z "$media_id" ]; then
        log_error "上传封面图片失败"
        echo "$response" | jq '.'
        return 1
    fi

    log_info "封面图片上传成功: $media_id"
    echo "$media_id"
}

# 转换 Markdown 到微信 HTML
convert_markdown() {
    local markdown_file=$1

    log_info "转换 Markdown 到微信 HTML..."

    local result=$(python3 "$SCRIPT_DIR/md2wechat.py" "$markdown_file")

    if [ $? -ne 0 ]; then
        log_error "Markdown 转换失败"
        exit 1
    fi

    echo "$result"
}

# 发布图文素材
publish_article() {
    local title=$1
    local content=$2
    local digest=$3
    local source_url=$4
    local thumb_media_id=$5
    local access_token=$6

    log_info "发布图文素材..."

    local json_data=$(jq -n \
        --arg title "$title" \
        --arg content "$content" \
        --arg digest "$digest" \
        --arg url "$source_url" \
        --arg thumb "$thumb_media_id" \
        '{
            articles: [{
                title: $title,
                author: "codingdie",
                digest: $digest,
                content: $content,
                content_source_url: $url,
                thumb_media_id: $thumb,
                show_cover_pic: 1,
                need_open_comment: 1,
                only_fans_can_comment: 0
            }]
        }')

    local response=$(curl -s -X POST \
        "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=$access_token" \
        -H "Content-Type: application/json" \
        -d "$json_data")

    local media_id=$(echo "$response" | jq -r '.media_id')

    if [ "$media_id" = "null" ] || [ -z "$media_id" ]; then
        log_error "发布图文素材失败"
        echo "$response" | jq '.'
        exit 1
    fi

    log_info "图文素材发布成功: $media_id"
    echo "$response"
}

# 更新 CLAUDE.md 记录
update_claude_md() {
    local article_file=$1
    local media_id=$2

    local claude_file="${article_file%.md}.CLAUDE.md"

    if [ ! -f "$claude_file" ]; then
        log_warn "CLAUDE.md 文件不存在: $claude_file"
        return
    fi

    log_info "更新 CLAUDE.md 发布记录..."

    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 在"修改历史"部分添加记录
    if grep -q "## 修改历史" "$claude_file"; then
        sed -i "/## 修改历史/a\\
\\
### $timestamp - 发布到微信公众号\\
\\
- media_id: $media_id\\
- 发布状态: 成功" "$claude_file"
    else
        echo -e "\n## 修改历史\n\n### $timestamp - 发布到微信公众号\n\n- media_id: $media_id\n- 发布状态: 成功" >> "$claude_file"
    fi

    log_info "CLAUDE.md 更新完成"
}

# 主函数
main() {
    local article_file=$1

    if [ -z "$article_file" ]; then
        log_error "用法: $0 <article-file>"
        exit 1
    fi

    # 转换为绝对路径
    if [[ ! "$article_file" = /* ]]; then
        article_file="$PROJECT_ROOT/$article_file"
    fi

    if [ ! -f "$article_file" ]; then
        log_error "文件不存在: $article_file"
        exit 1
    fi

    log_info "=========================================="
    log_info "微信公众号发布工具"
    log_info "=========================================="
    log_info "文章: $article_file"
    log_info ""

    # 检查依赖和环境
    check_dependencies
    check_env

    # 获取 access_token
    local access_token=$(get_access_token)

    # 转换 Markdown
    local article_json=$(convert_markdown "$article_file")
    local title=$(echo "$article_json" | jq -r '.title')
    local digest=$(echo "$article_json" | jq -r '.digest')
    local content=$(echo "$article_json" | jq -r '.content')
    local source_url=$(echo "$article_json" | jq -r '.source_url')

    log_info "文章标题: $title"
    log_info "文章摘要: ${digest:0:50}..."
    log_info ""

    # 上传封面图片（可选）
    local thumb_media_id=""
    local thumb_path="${article_file%.md}_thumb.jpg"
    if [ -f "$thumb_path" ]; then
        thumb_media_id=$(upload_thumb "$thumb_path" "$access_token")
    else
        log_warn "未找到封面图片，将不显示封面"
        # 使用默认封面或跳过
    fi

    # 发布图文素材
    local result=$(publish_article "$title" "$content" "$digest" "$source_url" "$thumb_media_id" "$access_token")
    local media_id=$(echo "$result" | jq -r '.media_id')

    # 更新 CLAUDE.md
    update_claude_md "$article_file" "$media_id"

    log_info ""
    log_info "=========================================="
    log_info "发布成功！"
    log_info "=========================================="
    log_info "Media ID: $media_id"
    log_info "原文链接: $source_url"
    log_info ""
    log_info "下一步："
    log_info "1. 登录微信公众平台查看素材"
    log_info "2. 在素材管理中找到刚发布的图文"
    log_info "3. 可以进行群发或预览"
}

main "$@"
