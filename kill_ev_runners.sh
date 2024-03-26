#!/bin/bash

pkill -f functionality/pos_ev_runners/nba_pos_ev_runner.py

pkill -f functionality/pos_ev_runners/nhl_pos_ev_runner.py

pkill -f functionality/pos_ev_runners/ncaab_pos_ev_runner.py

pkill -f functionality/pos_ev_copier.py

pkill -f functionality/pos_ev_runners/pos_ev_compiler.py

pkill -f functionality/pos_ev_runners/arb_compiler.py

#pkill -f functionality/pos_ev_runners/market_view_compiler.py

echo "Processes related to ev runners scripts killed."
