#!/usr/bin/env python

import os
import yaml
import subprocess


def main():
    output = {}
    if os.path.exists('/var/lib/docker/swarm/control.sock'):
        try:
            output["docker_swarm_tokens"] = {
                'worker': subprocess.check_output(["docker", "swarm", "join-token", "-q", "worker"]).strip(),
                'manager': subprocess.check_output(["docker", "swarm", "join-token", "-q", "manager"]).strip()
            }
        except subprocess.CalledProcessError:
            pass

    if os.path.exists('/var/lib/docker/swarm/state.json'):
        with open('/var/lib/docker/swarm/state.json') as fh:
            state = yaml.load(fh)
            for key, value in state[0].iteritems():
                output["docker_swarm_%s" % key] = value

    if os.path.exists('/var/lib/docker/swarm/docker-state.json'):
        with open('/var/lib/docker/swarm/docker-state.json') as fh:
            state = yaml.load(fh)
            for key, value in state.iteritems():
                output["docker_swarm_%s" % key] = value

    if output:
        return output
    else:
        return None
