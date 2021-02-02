#!/bin/sh

# Exit on error
set -e

# Check if remote username is set
if [ -z "$USER" ]; then
    echo "Remote host username is not set. Please, update \$USER"
    exit 1
fi

# Check if remote host is set
if [ -z "$HOST" ]; then
    echo "Remote host is not set. Please, update \$HOST"
    exit 1
fi

# Check if remote directory is set
if [ -z "$DIR" ];
then
    echo "Remote directory is not set. Please, update \$DIR"
    exit 1
fi

rsync -azvh --exclude='.DS_Store' --delete public/ ${USER}@${HOST}:~/${DIR}

exit 0
