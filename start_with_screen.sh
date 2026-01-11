#!/bin/bash
# 保持服务器运行的脚本 - 使用 screen 会话

echo "🚀 启动 AI 视频字幕提取工具（使用 screen）..."
echo ""

# 检查 screen 是否安装
if ! command -v screen &> /dev/null; then
    echo "❌ screen 未安装，正在安装..."
    echo "请稍等..."
    # macOS 默认自带 screen，如果没有就提示
    echo "请手动运行: brew install screen"
    exit 1
fi

# 停止旧的 screen 会话
echo "📋 清理旧会话..."
screen -S subtitle-backend -X quit 2>/dev/null
screen -S subtitle-frontend -X quit 2>/dev/null
sleep 2

# 启动后端（在 screen 会话中）
echo "🔧 启动后端服务器..."
screen -dmS subtitle-backend bash -c "cd /Users/xixi/subtitle-backend && python3 -u server.py"
sleep 3

# 检查后端
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "✅ 后端启动成功 (screen 会话: subtitle-backend)"
else
    echo "❌ 后端启动失败"
    exit 1
fi

# 启动前端（在 screen 会话中）
echo "🎨 启动前端服务器..."
screen -dmS subtitle-frontend bash -c "cd /Users/xixi/ai-video-subtitle-extractor && npm run dev"
sleep 8

# 检查前端
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "✅ 前端启动成功 (screen 会话: subtitle-frontend)"
else
    echo "❌ 前端启动失败"
    exit 1
fi

echo ""
echo "🎉 所有服务器启动成功！"
echo "================================================"
echo "📱 前端地址: http://localhost:5173/"
echo "🔌 后端地址: http://localhost:8000"
echo "================================================"
echo ""
echo "💡 使用说明："
echo "  - 浏览器打开: http://localhost:5173/"
echo "  - 服务器在 screen 会话中运行，不会被关闭"
echo ""
echo "📊 查看服务器日志："
echo "  - 后端日志: screen -r subtitle-backend"
echo "  - 前端日志: screen -r subtitle-frontend"
echo "  - 退出日志查看: 按 Ctrl+A 然后按 D"
echo ""
echo "🛑 停止服务器："
echo "  - 运行: /Users/xixi/subtitle-backend/stop_all.sh"
echo ""
echo "✅ 服务器现在会一直运行，即使关闭 Terminal"
echo ""
