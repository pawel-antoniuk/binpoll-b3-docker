import subprocess
import sys

if len(sys.argv) < 2:
    print('dev/deploy as second argument excepted')
    exit(1)

try:
    if sys.argv[1] == 'dev':
        subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-dev.override.yml'] + sys.argv[2:])
    elif sys.argv[1] == 'deploy':
        subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-deploy.override.yml'] + sys.argv[2:])
    elif sys.argv[1] == 'both':
        if subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-dev.override.yml'] + sys.argv[2:]).returncode == 0:
            subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-deploy.override.yml'] + sys.argv[2:])
    elif sys.argv[1] == 'dev-ssl':
        subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-ssl.override.yml', '-f', 'compose-dev.override.yml'] + sys.argv[2:])
    elif sys.argv[1] == 'deploy-ssl':
        subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-ssl.override.yml', '-f', 'compose-deploy.override.yml'] + sys.argv[2:])
    elif sys.argv[1] == 'both-ssl':
        if subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-ssl.override.yml', '-f', 'compose-dev.override.yml'] + sys.argv[2:]).returncode == 0:
            subprocess.run(['docker-compose',  '-f', 'compose-base.yml', '-f', 'compose-ssl.override.yml', '-f', 'compose-deploy.override.yml'] + sys.argv[2:])
    else:
        print('dev/deploy as second argument excepted')
        exit(1)
except KeyboardInterrupt:
    print('be patient...')