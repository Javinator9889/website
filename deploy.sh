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

# Adjust permissions
echo "Setting directory permissions to 0770 (rwx rwx ---)"
find webserver/ -type d -exec chmod 0770 {} \;

echo "Setting file permissions to 0660 (rw- rw- ---)"
find webserver/ -type f -exec chmod 0660 {} \;

echo "Syncing files..."
rsync -avh --exclude='.DS_Store' --delete webserver/ ${DIR}

echo "Removing webserver directory..."
rm -rv webserver/

exit 0
