import subprocess
import sys

COMPOSE_COMMAND=['docker-compose', '--project-directory', '.']
COMPOSE_BASE='compose/compose-base.yml'
COMPOSE_DEV='compose/compose-dev.override.yml'
COMPOSE_DEPLOY='compose/compose-deploy.override.yml'
COMPOSE_SSL='compose/compose-ssl.override.yml'
COMPOSE_REGISTRY='compose/compose-registry.yml'
ERROR_MSG_FIRST_ARG_EXCEPTED='First argument is excepted to be dev/deploy/both/dev-ssl/deploy-ssl/both-ssl'

if len(sys.argv) < 2:
    print(ERROR_MSG_FIRST_ARG_EXCEPTED)
    exit(1)

try:
    if sys.argv[1] == 'dev':
        subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_DEV] + sys.argv[2:])
    elif sys.argv[1] == 'deploy':
        subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_DEPLOY] + sys.argv[2:])
    elif sys.argv[1] == 'both':
        if subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_DEV] + sys.argv[2:]).returncode == 0:
            subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_DEPLOY] + sys.argv[2:])
    elif sys.argv[1] == 'dev-ssl':
        subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_SSL, '-f', COMPOSE_DEV] + sys.argv[2:])
    elif sys.argv[1] == 'deploy-ssl':
        subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_SSL, '-f', COMPOSE_DEPLOY] + sys.argv[2:])
    elif sys.argv[1] == 'both-ssl':
        if subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_SSL, '-f', COMPOSE_DEV] + sys.argv[2:]).returncode == 0:
            subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_BASE, '-f', COMPOSE_SSL, '-f', COMPOSE_DEPLOY] + sys.argv[2:])
    elif sys.argv[1] == 'registry':
        subprocess.run(COMPOSE_COMMAND + ['-f', COMPOSE_REGISTRY] + sys.argv[2:])
    else:
        print(ERROR_MSG_FIRST_ARG_EXCEPTED)
        exit(1)
except KeyboardInterrupt:
    print('be patient...')