#!/bin/bash
# Build script for Render: clone the day-trader-skill dependency
set -e
if [ ! -d "day-trader-skill" ]; then
  echo "Cloning day-trader-skill..."
  git clone --depth 1 https://github.com/Jakeschincariol/day-trader-skill.git day-trader-skill
fi
echo "Build complete."
