#!/bin/bash
cd /app
echo "=== Files in /app ==="
ls -la
echo "=== Python files ==="
find /app -name "*.py" -type f

if [ -n "$BOT_FILE" ]; then
    echo "=== Running specified bot: $BOT_FILE ==="
    python3 "/app/$BOT_FILE"
    exit $?
fi

echo "=== Running slash quotes bot ==="
python3 /app/slash_quotes_bot.py
