#!/bin/bash

docker run \
       --rm -it \
       -v /etc/passwd:/etc/passwd:ro \
       -v /etc/group:/etc/group:ro \
       -v $(pwd):$(pwd) \
       -w $(pwd) \
       -u $(id -u):$(id -g) \
       daytona-builder \
       $@

# EOF
