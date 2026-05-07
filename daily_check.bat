@echo off
cd /d "C:\Users\Administrator\Desktop\GenericAgent\temp\ai-tool-finder"
python daily_monitor.py --oneshot --audit >> daily_check.log 2>&1
