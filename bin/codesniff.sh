#!/usr/bin/env bash

files=$(git log --name-only HEAD^..HEAD | grep -F ".ph")

if [ ${#files} -gt 0 ]; then
    phpcs --standard=Ecg -n $files
else
    echo "no PHP files modified"
fi