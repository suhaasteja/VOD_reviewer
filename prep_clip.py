#!/usr/bin/env python3
"""
Prep a Clash Royale clip for Perceptron Mk1.
Trims the last N seconds (lossless), then compresses to <~18MB with low fps + full resolution.

Usage:
    python prep_clip.py SRC.mp4 [--window 30] [--target-mb 18] [--fps 6] [--crop "in_w:in_h*0.78:0:in_h*0.11"]
"""
import argparse, subprocess, os, sys

def probe_duration(path):
    return float(subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nw=1:nk=1", path]).decode().strip())

def probe_video(path):
    out = subprocess.check_output([
        "ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height,r_frame_rate,bit_rate,duration",
        "-of","default=noprint_wrappers=1", path]).decode().strip()
    print(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--window", type=int, default=30, help="seconds from the end")
    ap.add_argument("--target-mb", type=float, default=18)
    ap.add_argument("--fps", type=int, default=6)
    ap.add_argument("--crop", default=None, help='ffmpeg crop expr, e.g. "in_w:in_h*0.78:0:in_h*0.11"')
    args = ap.parse_args()

    base    = os.path.splitext(os.path.basename(args.src))[0]
    outdir  = os.path.dirname(args.src) or "."
    trimmed = os.path.join(outdir, f"{base}_last{args.window}s.mp4")
    out     = os.path.join(outdir, f"{base}_perceptron_ready.mp4")

    # 1) lossless copy-trim of the last N seconds
    full = probe_duration(args.src)
    start = max(0, full - args.window)
    print(f"[trim] full={full:.1f}s -> {start:.1f}s..end")
    subprocess.run(["ffmpeg","-y","-ss",str(start),"-i",args.src,"-c","copy",trimmed], check=True)

    print("\n[trimmed clip specs]")
    probe_video(trimmed)

    # 2) compress: low fps, drop audio, spend bitrate on resolution
    dur = probe_duration(trimmed)
    v_kbps = int((args.target_mb * 8 * 1024) / dur)
    vf = f"fps={args.fps}" + (f",crop={args.crop}" if args.crop else "")
    print(f"\n[compress] dur={dur:.1f}s  bitrate={v_kbps}kbps  fps={args.fps}  crop={args.crop}")

    common = ["ffmpeg","-y","-i",trimmed,"-vf",vf,"-c:v","libx264",
              "-b:v",f"{v_kbps}k","-preset","slow","-an"]
    subprocess.run(common + ["-pass","1","-f","mp4",os.devnull], check=True)
    subprocess.run(common + ["-pass","2",out], check=True)

    # cleanup two-pass logs
    for f in os.listdir("."):
        if f.startswith("ffmpeg2pass"):
            try: os.remove(f)
            except OSError: pass

    print(f"\n[done] {out}  ->  {os.path.getsize(out)/1e6:.1f} MB")
    print("[final specs]")
    probe_video(out)

if __name__ == "__main__":
    sys.exit(main())
