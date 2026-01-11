"""
简单的视频字幕提取后端服务
支持 URL 和本地文件上传
使用 yt-dlp 下载视频 + Faster-Whisper 识别字幕
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import tempfile
import subprocess
import json
from typing import Optional, List, Dict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Video Subtitle Extractor API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str


class SubtitleResponse(BaseModel):
    title: str
    duration: str
    platform: str
    thumbnail: Optional[str] = None
    subtitles: List[Dict[str, str]]
    summary: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "AI Video Subtitle Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "/api/extract-url": "POST - 从 URL 提取字幕",
            "/api/extract-file": "POST - 从本地文件提取字幕"
        }
    }


@app.post("/api/extract-url", response_model=SubtitleResponse)
async def extract_from_url(request: URLRequest):
    """
    从视频 URL 提取字幕
    支持 Bilibili、抖音、小红书、YouTube 等平台
    """
    logger.info(f"收到 URL 提取请求: {request.url}")

    try:
        # 使用 yt-dlp 获取视频信息
        video_info = get_video_info(request.url)

        # 下载音频
        audio_path = download_audio(request.url)

        # 使用 Whisper 识别字幕
        subtitles = transcribe_audio(audio_path)

        # 生成摘要（简单版本）
        summary = generate_summary(subtitles)

        # 清理临时文件
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return SubtitleResponse(
            title=video_info.get("title", "未知标题"),
            duration=format_duration(video_info.get("duration", 0)),
            platform=detect_platform(request.url),
            thumbnail=video_info.get("thumbnail"),
            subtitles=subtitles,
            summary=summary
        )

    except Exception as e:
        logger.error(f"处理 URL 时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/api/extract-file", response_model=SubtitleResponse)
async def extract_from_file(file: UploadFile = File(...)):
    """
    从上传的视频/音频文件提取字幕
    """
    logger.info(f"收到文件上传: {file.filename}")

    try:
        # 保存上传的文件
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 提取音频（如果是视频）
        audio_path = extract_audio_from_file(file_path)

        # 使用 Whisper 识别字幕
        subtitles = transcribe_audio(audio_path)

        # 生成摘要
        summary = generate_summary(subtitles)

        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(audio_path) and audio_path != file_path:
            os.remove(audio_path)

        return SubtitleResponse(
            title=file.filename,
            duration="--:--",
            platform="本地文件",
            thumbnail=None,
            subtitles=subtitles,
            summary=summary
        )

    except Exception as e:
        logger.error(f"处理文件时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


def get_video_info(url: str) -> dict:
    """使用 yt-dlp 获取视频信息"""
    try:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            logger.warning(f"yt-dlp 获取信息失败: {result.stderr}")
            return {"title": "视频", "duration": 0}
    except Exception as e:
        logger.error(f"获取视频信息出错: {str(e)}")
        return {"title": "视频", "duration": 0}


def download_audio(url: str) -> str:
    """使用 yt-dlp 下载音频"""
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "audio.mp3")

    cmd = [
        "yt-dlp",
        "-x",  # 只提取音频
        "--audio-format", "mp3",
        "--output", output_path,
        url
    ]

    subprocess.run(cmd, check=True, timeout=300)
    return output_path


def extract_audio_from_file(video_path: str) -> str:
    """从视频文件提取音频"""
    if video_path.lower().endswith(('.mp3', '.wav', '.m4a')):
        return video_path

    audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # 不包含视频
        "-acodec", "libmp3lame",
        "-y",  # 覆盖已存在的文件
        audio_path
    ]

    subprocess.run(cmd, check=True, timeout=300)
    return audio_path


def transcribe_audio(audio_path: str) -> List[Dict[str, str]]:
    """
    使用 Whisper 转录音频
    注意：这需要安装 faster-whisper 或 openai-whisper
    如果未安装，返回模拟数据
    """
    try:
        # 尝试使用 faster-whisper
        from faster_whisper import WhisperModel

        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language="zh")

        subtitles = []
        for segment in segments:
            subtitles.append({
                "timestamp": format_timestamp(segment.start),
                "text": segment.text.strip()
            })

        return subtitles

    except ImportError:
        logger.warning("faster-whisper 未安装，使用 openai-whisper")
        try:
            import whisper
            model = whisper.load_model("small")
            result = model.transcribe(audio_path, language="zh")

            subtitles = []
            for segment in result["segments"]:
                subtitles.append({
                    "timestamp": format_timestamp(segment["start"]),
                    "text": segment["text"].strip()
                })

            return subtitles

        except ImportError:
            logger.error("Whisper 未安装，返回模拟数据")
            # 返回模拟数据
            return [
                {"timestamp": "00:00", "text": "欢迎使用 AI 字幕提取工具"},
                {"timestamp": "00:03", "text": "这是一个演示字幕"},
                {"timestamp": "00:06", "text": "请安装 faster-whisper 或 openai-whisper 以获得真实识别功能"},
            ]


def generate_summary(subtitles: List[Dict[str, str]]) -> str:
    """生成简单摘要"""
    if not subtitles:
        return "暂无内容摘要"

    # 简单摘要：取前 3 条字幕
    text = " ".join([s["text"] for s in subtitles[:3]])
    return f"视频主要内容：{text}..."


def format_duration(seconds: float) -> str:
    """格式化时长"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_timestamp(seconds: float) -> str:
    """格式化时间戳"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def detect_platform(url: str) -> str:
    """检测视频平台"""
    if "bilibili.com" in url or "b23.tv" in url:
        return "Bilibili"
    elif "douyin.com" in url:
        return "抖音"
    elif "xiaohongshu.com" in url or "xhslink.com" in url:
        return "小红书"
    elif "youtube.com" in url or "youtu.be" in url:
        return "YouTube"
    else:
        return "未知平台"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
