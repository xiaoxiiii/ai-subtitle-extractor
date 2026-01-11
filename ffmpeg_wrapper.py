#!/usr/bin/env python3
"""
ffmpeg wrapper - 强制使用 imageio-ffmpeg 提供的 ffmpeg
"""
import sys
import os
import subprocess

# 获取真实的 ffmpeg 路径
import imageio_ffmpeg
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

# 调用真实的 ffmpeg
result = subprocess.run([ffmpeg_path] + sys.argv[1:])
sys.exit(result.returncode)
