#!/bin/bash

function clean {
    source scripts/clean.sh
}

function migrate {
    source scripts/migrate.sh
}

function load {
    source scripts/load.sh
}

function django {
    source scripts/run.sh
}

function redis {
    # Kill Redis PID
    if sudo lsof -i :6379; then
        sudo lsof -t -i :6379 | sudo xargs kill
    fi
    # Restart Redis service
    sudo systemctl restart redis.service
    # Run Redis
    gnome-terminal --tab --title "Redis" -- bash -c "redis-server"
}

function celery {
    # Run Celery Worker
    gnome-terminal --tab --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"
    # Run Celery Beat
    gnome-terminal --tab --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"
}

# Combinations

function services {
    redis
    celery
}

function start {
    django
    services
}

function build {
    clean
    migrate
    load
}

# Main

function init {

    while true; do
    echo "1: Build"
    echo "2: Clean"
    echo "3: Load Fixtures"
    echo "4: Migrate"
    echo "5: Start"
    echo "6: Start Celery"
    echo "7: Start Django"
    echo "8: Start Redis"
    echo "9: Start Redis/Celery"
    echo "0: Exit"
    read -p "Input a value from 0 to 9: " input
    
    re='^[0-9]$'
    if ! [[ $input =~ $re ]] ; then
    echo "Only integer values from 0 to 9."
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
        start
    fi

    if [ "$input" == 6 ]; then
        celery
    fi

    if [ "$input" == 7 ]; then
        django
    fi

    if [ "$input" == 8 ]; then
        redeis
    fi

    if [ "$input" == 9 ]; then
        services
    fi

    done
}

init