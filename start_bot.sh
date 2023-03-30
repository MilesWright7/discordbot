#!/bin/bash
tmux detach
tmux kill-server
tmux new -d -s botsession 'python3.9 VoiceBot.py'
