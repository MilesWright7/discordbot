#!/bin/bash
tmux kill-server
tmux new-session -d -s botsession 'python3 VoiceBot.py'