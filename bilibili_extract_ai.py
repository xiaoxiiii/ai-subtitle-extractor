#!/usr/bin/env python3
"""
B站视频 AI 字幕提取（使用 Whisper 语音识别）
"""

import sys
import json
import subprocess
import tempfile
import os

def extract_bilibili_subtitle_ai(url):
    """使用 AI 提取 B站视频字幕"""

    temp_dir = tempfile.gettempdir()
    audio_file = os.path.join(temp_dir, "bilibili_audio.mp3")

    try:
        # 步骤1: 获取视频信息
        print(json.dumps({"status": "获取视频信息..."}), file=sys.stderr)
        info_cmd = [
            "yt-dlp",  # 使用系统 PATH 中的 yt-dlp
            "--dump-json",
            "--no-download",
            url
        ]

        result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(json.dumps({"error": f"无法获取视频信息: {result.stderr}"}))
            return

        lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
        video_info = json.loads(lines[-1] if lines else '{}')

        title = video_info.get("title", "未知标题")
        duration = format_duration(video_info.get("duration", 0))
        thumbnail = video_info.get("thumbnail", "")

        # 步骤2: 下载视频
        print(json.dumps({"status": "正在下载视频..."}), file=sys.stderr)
        video_template = os.path.join(temp_dir, "bilibili_video.%(ext)s")
        download_cmd = [
            "yt-dlp",  # 使用系统 PATH 中的 yt-dlp
            "--output", video_template,
            "--no-playlist",
            url
        ]

        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            print(json.dumps({"error": f"视频下载失败: {result.stderr}"}))
            return

        # 查找实际下载的文件（优先选择音频文件）
        import glob
        audio_files = glob.glob(os.path.join(temp_dir, "bilibili_video.*.m4a"))
        if not audio_files:
            # 如果没有音频文件，尝试查找视频文件
            audio_files = glob.glob(os.path.join(temp_dir, "bilibili_video.*.mp4"))

        if not audio_files:
            print(json.dumps({"error": "找不到下载的音视频文件"}))
            return

        audio_file = audio_files[0]  # 使用找到的第一个文件

        # 步骤3: 使用 Whisper 识别
        print(json.dumps({"status": "AI 正在识别语音..."}), file=sys.stderr)

        import whisper
        import imageio_ffmpeg

        # 获取当前脚本所在目录（本地）或工作目录（Railway）
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 检查是否有本地的 ffmpeg wrapper（本地开发环境）
        local_ffmpeg = os.path.join(script_dir, 'ffmpeg')
        if os.path.exists(local_ffmpeg):
            # 本地开发环境：使用 wrapper
            os.environ['PATH'] = script_dir + ':' + os.environ.get('PATH', '')
            print(json.dumps({"status": "使用本地 ffmpeg wrapper"}), file=sys.stderr)
        else:
            # Railway 环境：直接使用 imageio-ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(json.dumps({"status": f"使用 imageio-ffmpeg: {ffmpeg_path}"}), file=sys.stderr)

        # 使用 base 模型（约 140MB，适合免费部署）
        # 如果是本地开发，可以改成 small 以获得更好的准确度
        model_size = os.environ.get('WHISPER_MODEL', 'base')
        print(json.dumps({"status": f"加载 Whisper {model_size} 模型..."}), file=sys.stderr)
        model = whisper.load_model(model_size)

        # 转录音频
        result = model.transcribe(audio_file, language="zh", verbose=False)

        # 格式化字幕
        subtitle_list = []
        for segment in result["segments"]:
            subtitle_list.append({
                "timestamp": format_timestamp(segment["start"]),
                "text": segment["text"].strip()
            })

        # 生成摘要
        full_text = " ".join([s["text"] for s in subtitle_list])
        summary = f"视频标题：{title}\n\n内容摘要：\n{full_text[:200]}..."

        # 清理临时文件
        if os.path.exists(audio_file):
            os.remove(audio_file)

        # 返回结果
        response = {
            "title": title,
            "duration": duration,
            "platform": "Bilibili",
            "thumbnail": thumbnail,
            "subtitles": subtitle_list,
            "summary": summary
        }

        print(json.dumps(response, ensure_ascii=False))

    except Exception as e:
        # 清理临时文件
        if os.path.exists(audio_file):
            os.remove(audio_file)
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

def format_duration(seconds):
    """格式化时长"""
    if not seconds:
        return "00:00"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def format_timestamp(seconds):
    """格式化时间戳"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请提供 B站视频链接"}))
        sys.exit(1)

    extract_bilibili_subtitle_ai(sys.argv[1])
