#!/bin/bash

set -e

rm -rf build
mkdir -p build

pip install -r requirements.txt -t build/
cp bot.py build/

cd build
zip -r ../telegram_bot_deployment_package.zip .
cd ..
rm -rf build
