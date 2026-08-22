@echo off
title Velocity Japanese - Video Generator
echo ========================================================
echo         VELOCITY JAPANESE - REELS / SHORTS BOT
echo ========================================================
echo.
echo Select an option:
echo [1] Daily Auto-Pilot (Picks a fresh new concept automatically)
echo [2] Preset 1: Days of the Week (35s)
echo [3] Preset 2: Must-Know JLPT N5 Kanji (35s)
echo [4] Preset 3: Essential Japanese Phrases (35s)
echo [5] Custom Topic (Pollinations AI)
echo [6] Generate 3-Video Batch
echo [7] Exit
echo.
set /p choice="Enter choice (1-7): "

if "%choice%"=="1" (
    python main.py --auto
) else if "%choice%"=="2" (
    python main.py --preset 0
) else if "%choice%"=="3" (
    python main.py --preset 1
) else if "%choice%"=="4" (
    python main.py --preset 2
) else if "%choice%"=="5" (
    set /p custom_topic="Enter Japanese topic (e.g. Japanese Street Food, Travel Phrases, Tokyo Subway): "
    python main.py --topic "%custom_topic%"
) else if "%choice%"=="6" (
    python main.py --batch 3 --auto
) else (
    echo Exiting...
)
pause
