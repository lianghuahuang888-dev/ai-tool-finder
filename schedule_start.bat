@echo off
cd /d "C:\Users\Administrator\Desktop\GenericAgent\temp\ai-tool-finder"
echo Starting Daily Monitor (24h loop, Ctrl+C to stop)
python daily_monitor.py --schedule --audit
