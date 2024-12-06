#!/bin/sh

git submodule update --init --recursive

pip install -e .
