#!/bin/bash
# AI 视频字幕提取工具 - 启动脚本
# 这个脚本会启动前端和后端服务器，并保持它们运行

echo "🚀 正在启动 AI 视频字幕提取工具..."
echo ""

# 检查并停止旧的进程
echo "📋 检查旧进程..."
pkill -9 -f "python3.*server.py" 2>/dev/null
pkill -9 -f "vite" 2>/dev/null
sleep 2

# 确保端口已释放
echo "🔍 确保端口已释放..."
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  端口 8000 仍被占用，强制释放..."
    kill -9 $(lsof -ti:8000) 2>/dev/null
    sleep 1
fi
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "⚠️  端口 5173 仍被占用，强制释放..."
    kill -9 $(lsof -ti:5173) 2>/dev/null
    sleep 1
fi

# 启动后端服务器
echo "🔧 启动后端服务器 (端口 8000)..."
cd /Users/xixi/subtitle-backend
nohup python3 server.py > backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# 检查后端是否启动成功
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "✅ 后端服务器启动成功 (PID: $BACKEND_PID)"
else
    echo "❌ 后端服务器启动失败，请检查 /Users/xixi/subtitle-backend/backend.log"
    exit 1
fi

# 启动前端服务器
echo "🎨 启动前端服务器 (端口 5173)..."
cd /Users/xixi/ai-video-subtitle-extractor
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 5

# 检查前端是否启动成功
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "✅ 前端服务器启动成功 (PID: $FRONTEND_PID)"
else
    echo "❌ 前端服务器启动失败，请检查 /Users/xixi/ai-video-subtitle-extractor/frontend.log"
    exit 1
fi

echo ""
echo "🎉 所有服务器启动成功！"
echo "================================================"
echo "📱 前端地址: http://localhost:5173/"
echo "🔌 后端地址: http://localhost:8000"
echo "🧪 测试页面: http://localhost:5173/test.html"
echo "================================================"
echo ""
echo "💡 提示："
echo "  - 在浏览器打开: http://localhost:5173/"
echo "  - 如果无法提取，先访问测试页面: http://localhost:5173/test.html"
echo "  - 查看后端日志: tail -f /Users/xixi/subtitle-backend/backend.log"
echo "  - 查看前端日志: tail -f /Users/xixi/ai-video-subtitle-extractor/frontend.log"
echo "  - 停止服务器: /Users/xixi/subtitle-backend/stop_all.sh"
echo ""
echo "🔧 故障排除："
echo "  1. 如果提示'无法连接到服务器'，刷新页面并重试"
echo "  2. 如果仍然失败，运行: /Users/xixi/subtitle-backend/start_all.sh"
echo "  3. 检查服务器状态: lsof -ti:5173 && lsof -ti:8000"
echo ""
