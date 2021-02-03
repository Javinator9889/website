#!/bin/bash

# Exit on error
set -e

if [ -f .env ];
then
    source ./.env
fi

# Check if remote directory is set
if [ -z "$DIR" ];
then
    echo "Remote directory is not set. Please, update \$DIR"
    exit 1
fi

rsync -azvh --exclude='.DS_Store' --delete webserver/ ${DIR}

exit 0
