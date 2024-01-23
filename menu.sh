#!/bin/bash

function build {
    clean
    migrate
    load
}

function clean {
    source clean.sh
}

function load {
    source load.sh
}

function migrate {
    source migrare.sh
}

function run {
    source run.sh
}

# Main

function init {

    while true; do
    echo "1: Build."
    echo "2: Clean."
    echo "3: Load."
    echo "4: Migrate."
    echo "5: Run."
    echo "0: Exit."
    read -p "Info: Input a value from 0 to 5: " input
    
    re='^[0-5]$'
    if ! [[ $input =~ $re ]] ; then
    echo "Error: Only integer values from 0 to 5."
    fi

    if [ "$input" == 0 ]; then
        echo "Exiting..."
        break
    fi

    if [ "$input" == 1 ]; then
        build
    fi

    if [ "$input" == 2 ]; then
        clean
    fi

    if [ "$input" == 3 ]; then
        load
    fi

    if [ "$input" == 4 ]; then
        migrate
    fi

    if [ "$input" == 5 ]; then
        run
    fi

    done
}

init