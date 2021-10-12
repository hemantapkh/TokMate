# Due to a bug in appleboy/ssh-action@master, some commands shows error and fails to execute.
# So, running a bash file instead of commands

echo $1 > /opt/TokMate/TokMate/src/config.json  && pkill -f tokmate.py ; source /opt/TokMate/venv/bin/activate && cd /opt/TokMate/TokMate && screen -dm python3 tokmate.py