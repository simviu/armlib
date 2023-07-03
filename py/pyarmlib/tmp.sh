#!/bin/bash

for i in {1..10000}
do
  echo "Loop spin:" $i
  echo "  err: -_-" >&2 
  sleep 1
done

