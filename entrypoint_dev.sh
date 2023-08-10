#!/bin/bash
set -m
#service to start the notebook

#run the original notebook entrypoint
#usermod -u $UID notebook
#groupmod -g $GID users
#chgrp users /home/notebook
#normal notebook exec command to run the simple.sh
#exec gosu notebook simple.sh &
docker_entrypoint.sh simple.sh --NotebookApp.token='' &

#exec "$@"
"$@"
