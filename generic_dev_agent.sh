#!/bin/bash

for i in {1..100}
do
    aider --read spec.md --file notes.md --model openrouter/deepseek/deepseek-r1 --yes-always  --subtree-only **/*py **/*md --message 'Please work on the highest priority tasks. Keep in mind that having a low complexity codebase with isolated micro packages is highest priority.'
    sleep 1
done
