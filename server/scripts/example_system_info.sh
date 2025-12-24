#!/bin/bash
# Example shell script - Shows system information

echo "=========================================="
echo "System Information"
echo "=========================================="
echo ""
echo "Hostname: $(hostname)"
echo "Date: $(date)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo ""
echo "--- Disk Usage ---"
df -h / 2>/dev/null | tail -1
echo ""
echo "--- Memory ---"
free -h 2>/dev/null | head -2 || vm_stat 2>/dev/null | head -5
echo ""
echo "--- CPU Load ---"
uptime | awk -F'load average:' '{ print $2 }'
echo ""
echo "=========================================="
echo "Done!"

