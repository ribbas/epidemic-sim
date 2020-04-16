#! /bin/zsh

ncpu=$(($(nproc --all) - 1))
seed_begin=$(($1))
seed_end=$(($2))

if [ "${@[-1]}" = "--stats" ]; then
    echo "Parsing outputs and generating statistics..."
    make_cmd_str="make stats SEED1"
elif [ "${@[-1]}" = "--run" ]; then
    echo "Running program..."
    make_cmd_str="timeout 30 make run SEED1"
else
    exit 22
fi

argn=$#
make generate install
if [ "$argn" -eq "3" ]; then

    seed_chunk=$((${seed_begin} + ${ncpu}))
    while ((${seed_chunk} <= ${seed_end})); do

        make_cmd="${make_cmd_str}=${seed_begin} SEED2=${seed_chunk}"
        echo ${make_cmd}
        eval ${make_cmd}

        seed_begin=$((${seed_chunk} + 1))
        seed_chunk=$((${seed_begin} + ${ncpu}))
        make_cmd="${make_cmd_str}=${seed_begin}"

    done

else

    argi=0
    seed_chunk=$((${argi} + ${ncpu}))
    for arg do
        shift
        argi=$(( argi + 1 ))
        if [[ "$argi" -lt "$argn" ]]; then
            make_cmd="${make_cmd_str}=${arg} SEED2=${arg}"
            echo ${make_cmd}
            eval ${make_cmd}
        fi
    done

fi
