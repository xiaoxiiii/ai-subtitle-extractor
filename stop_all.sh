#!/bin/bash
# 停止所有服务器

echo "🛑 正在停止所有服务器..."

# 停止 screen 会话
screen -S subtitle-backend -X quit 2>/dev/null
screen -S subtitle-frontend -X quit 2>/dev/null

# 停止进程
pkill -f "python3.*server.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

sleep 1

echo "✅ 所有服务器已停止"
