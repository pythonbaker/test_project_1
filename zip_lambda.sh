#!/bin/bash
set -e

LAMBDA_DIR="lambda_build"

rm -rf $LAMBDA_DIR
mkdir -p $LAMBDA_DIR

cp -r src/* $LAMBDA_DIR/
cd $LAMBDA_DIR
zip -r ../terraform/lambda_function.zip .
cd ..

