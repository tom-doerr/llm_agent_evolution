#!/bin/bash

for i in {1..100}
do
    aider --read spec.md --file notes.md --model openrouter/deepseek/deepseek-r1 --yes-always  --subtree-only **/*py **/*md task_list.md --message 'Review the project and update the task_list.md file with tasks sorted by priority.'
    sleep 60
done
