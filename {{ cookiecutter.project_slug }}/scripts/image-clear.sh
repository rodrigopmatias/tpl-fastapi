#!/bin/bash

for version in $(podman image ls $1 -n | awk '{print $2}')
do
  podman image rm $1:$version
done
