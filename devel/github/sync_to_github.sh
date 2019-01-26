#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
GITHUB_DIR="/home/dan/LocalRepositories/GITHUB/DirectorySync"
## script to sync to github
rsync -av --exclude-from ${DIR}/rsync_github_exclude.txt ${DIR}/../../ ${GITHUB_DIR}/
cd ${GITHUB_DIR};
git add .
git commit -am "Mirror push from main development repo";
git push origin master;
printf "\nPushed to Github!\n";