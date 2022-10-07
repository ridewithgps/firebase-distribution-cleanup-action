#!/bin/sh

echo "$INPUT_AUTHENTICATIONFILE" > /auth.json

export GOOGLE_APPLICATION_CREDENTIALS="/auth.json"

python3 /cleanup.py \
  "$INPUT_APPID" \
  "$INPUT_CRITERIA"
