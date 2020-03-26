#! /bin/zsh

ncpu=$(nproc --all)
seed_begin=5
seed_term=$(($1))
seed_end=$((${seed_begin} + ${ncpu}))
make_run_cmd_str="make run SEED"
make_cmd="${make_run_cmd_str}=${seed_begin}"

# array=()
# for seed in ${array[@]} ; do
#     make_cmd+=" & ${make_run_cmd_str}=${seed}"
# done
# echo ${make_cmd}
# eval ${make_cmd}

# make generate install
while ((${seed_end} <= ${seed_term})); do

    for seed in $(seq $((${seed_begin} + 1)) ${seed_end}); do
        make_cmd+=" & ${make_run_cmd_str}=${seed}"
    done

    echo ${make_cmd}
    eval ${make_cmd}

    seed_begin=$((${seed_end} + 1))
    seed_end=$((${seed_begin} + ${ncpu}))
    make_cmd="${make_run_cmd_str}=${seed_begin}"

done

echo "\e[1;34mDONE\e[0m"
