#!/bin/bash

echo "🛑 正在停止所有服务（包括公网隧道）..."

# 停止所有相关进程
pkill -f "python3.*server.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
pkill -f "localtunnel" 2>/dev/null
pkill -f "npx" 2>/dev/null

sleep 2

echo "✅ 所有服务已停止"
