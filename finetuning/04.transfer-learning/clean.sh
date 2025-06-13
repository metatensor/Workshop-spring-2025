#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

rm -rf $SCRIPT_DIR/outputs $SCRIPT_DIR/*.ckpt $SCRIPT_DIR/*.pt $SCRIPT_DIR/error.log $SCRIPT_DIR/*.xyz $SCRIPT_DIR/*.png
