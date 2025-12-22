#!/bin/bash
set -euo pipefail
LOG=/var/log/beverage/backup_raw_csv.log
RECIPIENT="elijah.silva@icloud.com"

echo "=== $(date) ===" >> $LOG

if ! rclone copy ~/beverage/data/raw google-drive:beverage/raw/$(date +%Y/%m/%d) \
  --exclude ".DS_Store" --exclude "rsync" --exclude "*.bak" -P >> $LOG 2>&1; then
  echo "Backup failed at $(date). Check $LOG for details." | \
    mail -s "Beverage backup failed" "$RECIPIENT"
  exit 1
fi