#!/bin/bash
# 一键启动脚本 - 简化版

echo "🚀 启动 AI 视频字幕提取工具..."

# 停止旧进程
pkill -9 -f "python3.*server.py" 2>/dev/null
pkill -9 -f "vite" 2>/dev/null
sleep 2

# 启动后端
echo "🔧 启动后端..."
cd /Users/xixi/subtitle-backend
nohup python3 -u server.py > backend.log 2>&1 &
sleep 2

# 启动前端
echo "🎨 启动前端..."
cd /Users/xixi/ai-video-subtitle-extractor
nohup npm run dev > frontend.log 2>&1 &
sleep 8

# 验证
if lsof -ti:8000 > /dev/null && lsof -ti:5173 > /dev/null; then
    echo ""
    echo "🎉 启动成功！"
    echo "================================================"
    echo "📱 请在浏览器打开: http://localhost:5173/"
    echo "================================================"
    echo ""
    echo "💡 提示："
    echo "  - 如果打不开，试试: http://127.0.0.1:5173/"
    echo "  - 使用 Chrome 浏览器效果最好"
    echo "  - 停止服务器: /Users/xixi/subtitle-backend/stop_all.sh"
else
    echo "❌ 启动失败，请检查日志"
fi
