#! /bin/sh

make install
for i in {0..36..12}; do
    make run-sst stats SEED=$i &
    make run-sst stats SEED=$((i+1)) &
    make run-sst stats SEED=$((i+2)) &
    make run-sst stats SEED=$((i+3)) &
    make run-sst stats SEED=$((i+4)) &
    make run-sst stats SEED=$((i+5)) &
    make run-sst stats SEED=$((i+6)) &
    make run-sst stats SEED=$((i+7)) &
    make run-sst stats SEED=$((i+8)) &
    make run-sst stats SEED=$((i+9)) &
    make run-sst stats SEED=$((i+10)) &
    make run-sst stats SEED=$((i+11))
done
