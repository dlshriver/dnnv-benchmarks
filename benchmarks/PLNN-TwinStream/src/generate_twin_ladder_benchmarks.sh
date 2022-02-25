#!/bin/bash
# based on the version in the PLNN-Verification repo
# https://github.com/oval-group/PLNN-verification/blob/9eb91f4a53d30aee432258d3f81bceffdbf49421/scripts/generate_twin_ladder_benchmarks.sh
possible_width=(5 10 25)
possible_nb_layers=(2 4 5)
possible_nb_inputs=(5 10 25)
possible_margin=(1e-2 1 10)

TARGET_DIR=twin_ladder/benchmark

mkdir -p $TARGET_DIR

trap "exit" INT
for width in "${possible_width[@]}"; do
    for nb_layers in "${possible_nb_layers[@]}"; do
        for nb_input in "${possible_nb_inputs[@]}"; do
            for margin in "${possible_margin[@]}"; do
                model_name="twin_ladder-${nb_input}_inp-${nb_layers}_layers-${width}_width-${margin}_margin"
                prop_name="twin_ladder"
                target_name="$model_name $prop_name"
                layer_pattern=$(for a in $(seq $nb_layers); do echo -n "$width "; done)

                echo "./twin_ladder/generate_twinladder_net.py $TARGET_DIR $target_name $margin $nb_input $layer_pattern"
                ./twin_ladder/generate_twinladder_net.py $TARGET_DIR $target_name $margin $nb_input $layer_pattern
            done
        done
    done
done
