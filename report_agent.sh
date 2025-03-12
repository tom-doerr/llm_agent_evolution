#!/bin/bash

for i in {1..100}
do
    aider --read spec.md --file notes.md --model openrouter/deepseek/deepseek-r1 --yes-always  --subtree-only **/*py **/*md project_report.md --message 'Review the project and update/improve the project_report.md'
    sleep 60
done
