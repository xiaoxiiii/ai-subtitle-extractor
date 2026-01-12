#!/usr/bin/env python3
"""
超简单的 HTTP 服务器
用于桥接前端和 B站字幕提取脚本
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import urllib.parse
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        """处理 GET 请求（健康检查）"""
        if self.path == '/' or self.path == '/health':
            # Render 的健康检查端点
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = json.dumps({"status": "ok", "message": "AI Subtitle Extractor is running"})
                self.wfile.write(response.encode('utf-8'))
            except (BrokenPipeError, ConnectionResetError):
                pass
        else:
            self.send_error_response({"error": "Not Found"}, 404)

    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/api/extract':
            try:
                print(f"[INFO] 收到提取请求")

                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                url = data.get('url', '')
                print(f"[INFO] URL: {url}")

                if not url:
                    self.send_error_response({"error": "请提供视频链接"})
                    return

                print(f"[INFO] 开始处理视频...")
                # 调用 AI 识别脚本（使用更长的超时时间）
                # 获取当前脚本所在目录
                script_dir = os.path.dirname(os.path.abspath(__file__))
                extract_script = os.path.join(script_dir, 'bilibili_extract_ai.py')

                result = subprocess.run(
                    ['python3', extract_script, url],
                    capture_output=True,
                    text=True,
                    timeout=600  # 10分钟超时，因为 small 模型处理较慢
                )

                if result.returncode == 0:
                    print(f"[INFO] 处理成功，返回结果")
                    response_data = json.loads(result.stdout)
                    self.send_json_response(response_data)
                else:
                    print(f"[ERROR] 处理失败: {result.stderr[:200]}")
                    self.send_error_response({"error": f"处理失败: {result.stderr}"})

            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"[WARNING] 客户端断开连接: {e}")
            except Exception as e:
                print(f"[ERROR] 异常: {e}")
                try:
                    self.send_error_response({"error": str(e)})
                except (BrokenPipeError, ConnectionResetError):
                    pass
        else:
            self.send_error_response({"error": "Not Found"}, 404)

    def send_json_response(self, data):
        """发送 JSON 响应"""
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            print(f"[WARNING] 发送响应时连接断开")

    def send_error_response(self, data, code=400):
        """发送错误响应"""
        try:
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            print(f"[WARNING] 发送错误响应时连接断开")

    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    try:
        print('=' * 50, flush=True)
        print('🔧 开始启动服务器...', flush=True)

        # Railway 会提供 PORT 环境变量，本地开发使用 8000
        port = int(os.environ.get('PORT', 8000))
        print(f'📌 使用端口: {port}', flush=True)

        server_address = ('', port)
        print(f'📌 绑定地址: {server_address}', flush=True)

        httpd = HTTPServer(server_address, SimpleHandler)
        print('🚀 服务器启动成功！', flush=True)
        print(f'📡 监听地址: http://localhost:{port}', flush=True)
        print(f'📝 API 端点: POST http://localhost:{port}/api/extract', flush=True)
        print('=' * 50, flush=True)

        httpd.serve_forever()
    except Exception as e:
        print(f'❌ 服务器启动失败: {e}', flush=True)
        import traceback
        traceback.print_exc()
        raise
