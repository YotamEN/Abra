#!/bin/bash

"$@" &

printf 'Loading' > /dev/tty
while kill -0 $!; do
    printf '.' > /dev/tty
    sleep 5
done

printf '\n' > /dev/tty