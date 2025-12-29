#!/bin/bash

# Ubuntu System Checks Script

echo "=== Ubuntu System Information ==="
echo ""

echo "1. OS Version:"
cat /etc/os-release | grep -E "^NAME|^VERSION"
echo ""

echo "2. Kernel Information:"
uname -r
echo ""

echo "3. System Uptime:"
uptime
echo ""

echo "4. CPU Information:"
nproc
echo "CPU cores available"
echo ""

echo "5. Memory Usage:"
free -h
echo ""

echo "6. Disk Usage:"
df -h
echo ""

echo "7. Available Packages:"
apt-get update -qq
apt-cache search curl | head -1
echo ""

echo "=== System checks completed successfully ==="
