#!/bin/bash

nohup python3 functionality/pos_ev_runners/nba_pos_ev_runner.py > nba_pos_ev.log &

nohup python3 functionality/pos_ev_runners/nhl_pos_ev_runner.py > nhl_pos_ev.log &

nohup python3 functionality/pos_ev_runners/mlb_pos_ev_runner.py > mlb_pos_ev.log &

nohup python3 functionality/pos_ev_runners/ncaab_pos_ev_runner.py > ncaab_pos_ev.log &

nohup python3 functionality/pos_ev_copier.py > pos_ev_copier.log &

nohup python3 functionality/pos_ev_runners/pos_ev_compiler.py > pos_ev_compiler.log &

nohup python3 functionality/pos_ev_runners/arb_compiler.py > arb_compiler.log &

echo "EV runners processes started."
