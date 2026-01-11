#!/bin/bash
# 诊断脚本 - 测试前后端连接

echo "🔍 开始诊断..."
echo ""

# 1. 检查服务器状态
echo "1️⃣ 检查服务器状态"
echo "------------------------"
if lsof -ti:5173 > /dev/null 2>&1; then
    echo "✅ 前端服务器运行中 (PID: $(lsof -ti:5173))"
else
    echo "❌ 前端服务器未运行"
fi

if lsof -ti:8000 > /dev/null 2>&1; then
    echo "✅ 后端服务器运行中 (PID: $(lsof -ti:8000))"
else
    echo "❌ 后端服务器未运行"
fi
echo ""

# 2. 测试后端 API（简单测试）
echo "2️⃣ 测试后端 API（快速测试）"
echo "------------------------"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"url":"test"}' \
  --max-time 3)

if echo "$RESPONSE" | grep -q "error"; then
    echo "✅ 后端 API 响应正常"
    echo "响应片段: $(echo $RESPONSE | cut -c1-100)..."
else
    echo "❌ 后端 API 无响应或异常"
    echo "响应: $RESPONSE"
fi
echo ""

# 3. 测试前端可访问性
echo "3️⃣ 测试前端可访问性"
echo "------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 前端页面可访问 (HTTP $HTTP_CODE)"
else
    echo "❌ 前端页面无法访问 (HTTP $HTTP_CODE)"
fi
echo ""

# 4. 测试 CORS
echo "4️⃣ 测试 CORS 配置"
echo "------------------------"
CORS_HEADER=$(curl -s -X OPTIONS http://localhost:8000/api/extract \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -I | grep -i "access-control-allow-origin")

if [ ! -z "$CORS_HEADER" ]; then
    echo "✅ CORS 配置正常"
    echo "$CORS_HEADER"
else
    echo "❌ CORS 配置可能有问题"
fi
echo ""

# 5. 查看后端日志
echo "5️⃣ 后端最近日志"
echo "------------------------"
if [ -f /Users/xixi/subtitle-backend/backend.log ]; then
    LINES=$(wc -l < /Users/xixi/subtitle-backend/backend.log)
    if [ "$LINES" -gt 0 ]; then
        echo "日志行数: $LINES"
        echo "最近 5 行:"
        tail -5 /Users/xixi/subtitle-backend/backend.log
    else
        echo "⚠️  日志文件为空"
    fi
else
    echo "⚠️  日志文件不存在"
fi
echo ""

# 6. 进程信息
echo "6️⃣ 服务器进程信息"
echo "------------------------"
ps aux | grep -E "(vite|python.*server)" | grep -v grep | head -5
echo ""

echo "✅ 诊断完成"
echo ""
echo "💡 建议："
echo "  - 如果后端 API 不响应，重启服务器: /Users/xixi/subtitle-backend/start_all.sh"
echo "  - 如果 CORS 有问题，检查 server.py 的 CORS 配置"
echo "  - 访问测试页面: http://localhost:5173/test.html"
