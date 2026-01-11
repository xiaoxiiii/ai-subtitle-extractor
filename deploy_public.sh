#!/bin/bash

echo "🌐 正在部署 AI 视频字幕提取工具到公网..."
echo ""

# 1. 停止旧进程
echo "📌 步骤 1/4: 停止旧进程..."
pkill -9 -f "python3.*server.py" 2>/dev/null
pkill -9 -f "vite" 2>/dev/null
pkill -9 -f "localtunnel" 2>/dev/null
sleep 2

# 2. 启动后端服务器
echo "📌 步骤 2/4: 启动后端服务器..."
cd /Users/xixi/subtitle-backend
nohup python3 -u server.py > backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

# 检查后端是否启动成功
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "   ✅ 后端启动成功 (PID: $BACKEND_PID)"
else
    echo "   ❌ 后端启动失败，请检查 backend.log"
    exit 1
fi

# 3. 启动前端服务器
echo "📌 步骤 3/4: 启动前端服务器..."
cd /Users/xixi/ai-video-subtitle-extractor
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 8

# 检查前端是否启动成功
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "   ✅ 前端启动成功 (PID: $FRONTEND_PID)"
else
    echo "   ❌ 前端启动失败，请检查 frontend.log"
    exit 1
fi

# 4. 启动内网穿透
echo "📌 步骤 4/4: 创建公网访问隧道..."
echo ""
echo "⏳ 正在连接到公网服务器，请稍候..."
echo ""

# 使用 npx 运行 localtunnel，不需要全局安装
cd /Users/xixi/ai-video-subtitle-extractor
npx localtunnel --port 5173 --print-requests

# 注意：localtunnel 会一直运行，Ctrl+C 停止
