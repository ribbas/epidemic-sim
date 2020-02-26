#! /bin/sh

ncpu=$((2 * $(nproc --all)))
seed_begin=993
seed_end=$((${seed_begin} + ${ncpu}))
make_cmd_str="make run-sst stats SEED"
make_cmd="${make_cmd_str}=${seed_begin}"

# make install
while ((${seed_end} <= 1042)); do

    for seed in $(seq $((${seed_begin} + 1)) ${seed_end}); do
        make_cmd+=" & ${make_cmd_str}=${seed}"
    done

    echo ${make_cmd}
    eval ${make_cmd}

    seed_begin=$((${seed_end} + 1))
    seed_end=$((${seed_begin} + ${ncpu}))
    make_cmd="${make_cmd_str}=${seed_begin}"

done

echo -e "\e[1;34mDONE\e[0m"
