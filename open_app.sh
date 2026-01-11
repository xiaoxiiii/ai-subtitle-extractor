#!/bin/bash
# 打开 AI 字幕提取工具

# 检查服务器是否运行
if ! lsof -ti:5173 > /dev/null 2>&1; then
    echo "⚠️  服务器未运行，正在启动..."
    /Users/xixi/subtitle-backend/start_all.sh
    sleep 10
fi

# 使用 Chrome 打开（优先）
if open -a "Google Chrome" http://127.0.0.1:5173/ 2>/dev/null; then
    echo "✅ 已在 Chrome 中打开"
elif open -a "Firefox" http://127.0.0.1:5173/ 2>/dev/null; then
    echo "✅ 已在 Firefox 中打开"
else
    # 使用默认浏览器
    open http://127.0.0.1:5173/
    echo "✅ 已在默认浏览器中打开"
fi

echo ""
echo "📱 如果浏览器没有自动打开，请手动访问："
echo "   http://127.0.0.1:5173/"
echo ""
echo "💡 提示：建议使用 Chrome 浏览器，Safari 可能有兼容性问题"
