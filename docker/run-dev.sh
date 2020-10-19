#!/bin/bash

docker run \
	-v /home/schsia/.cache:/home/schsia/.cache:ro \
	-v /group/brooks:/group/brooks:ro \
	-v /group/vlsiarch:/group/vlsiarch:rw \
	-v /etc/passwd:/etc/passwd:ro \
	-v /data/:/data/:ro \
	-it --rm --user $(id -u) scalesim:cpu  /bin/bash