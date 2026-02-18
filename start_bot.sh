#!/bin/bash
tmux detach
echo "jumped out of tmux session"
tmux kill-session -t botsession
echo "killed server"
tmux new -d -s "botsession" "$HOME/discordbot/venv/bin/python VoiceBot.py"
echo "restarted a session"
