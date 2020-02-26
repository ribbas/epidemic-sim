#! /bin/sh

seed_begin=113
seed_end=$((${seed_begin} + 12))
make_cmd_str="make run-sst stats SEED"
make_cmd="${make_cmd_str}=${seed_begin}"
cpus=$(nproc --all)

# make install
while ((${seed_end} <= 200)); do
    for seed in $(seq $((${seed_begin} + 1)) ${seed_end}); do
        make_cmd+=" & ${make_cmd_str}=${seed}"
    done
    make_cmd+=";"
    echo ${make_cmd}
    # eval ${make_cmd}

    seed_begin=$((${seed_end} + 1))
    seed_end=$((${seed_begin} + 12))
    make_cmd="${make_cmd_str}=${seed_begin}"
done

echo -e "\e[1;34mDONE\e[0m"
