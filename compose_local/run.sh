#!/bin/bash
set -e
cd "$(dirname "$0")"

clean() {
    [ "$(docker ps -aq)" ] && docker rm -vf $(docker ps -aq)
    [ "$(docker images -q -f dangling=true)" ] && docker rmi --force $(docker images -q -f dangling=true)
}

clean_all() {
    clean
    docker builder prune --force
    docker system prune --force --all
}

case "${1:-up}" in
    up)
        docker compose up --build -d
        sleep 3
        curl -s http://localhost:8765/health && echo " ✅ http://localhost:8765/"
        ;;
    down)
        docker compose down
        ;;
    logs)
        docker compose logs -f
        ;;
    restart)
        docker compose down && docker compose up --build -d
        ;;
    status)
        docker compose ps
        ;;
    clean)
        clean
        ;;
    clean-all)
        clean_all
        ;;
    fix)
        clean
        docker compose up --build -d
        ;;
    *)
        echo "Usage: $0 {up|down|logs|restart|status|clean|clean-all|fix}"
        ;;
esac
