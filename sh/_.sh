function clean {
    source sh/clean.sh
}

function migrate {
    source sh/migrate.sh
}

function load {
    source sh/load.sh
}

function django {
    source sh/run.sh
}

function redis {
    source sh/redis.sh
}

function celery {
    source sh/celery.sh
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
    migarte
    load
    start
}

# Main

function init {

    echo "0: to exit"
    echo "1: to clean"
    echo "2: to migrate"
    echo "3: to load"
    echo "4: to start Django"
    echo "5: to start Redis"
    echo "6: to start Celery"
    echo "7: to start Redis and Celery"
    echo "8: to clean, migrate and load fixtures."
    echo "9: to start Django, Redis and Celery servers."

    while true; do
    read -p "Enter a value from 0 to 9: " input
    
    if [ "$input" == 0 ]; then
        echo "Exiting..."
        break
    fi

    if [ "$input" == 1 ]; then
        clean
    fi

    if [ "$input" == 2 ]; then
        migrate
    fi

    if [ "$input" == 3 ]; then
        load
    fi

    if [ "$input" == 4 ]; then
        django
    fi

    if [ "$input" == 5 ]; then
        redis
    fi

    if [ "$input" == 6 ]; then
        celery
    fi

    if [ "$input" == 7 ]; then
        services
    fi

    if [ "$input" == 8 ]; then
        build
    fi

    if [ "$input" == 9 ]; then
        start
    fi

    done
}

init