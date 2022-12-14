#!/bin/bash

for set in anaphora lexical_choice; do
    paste $set.prev.en $set.current.en $set.prev.fr $set.current.fr | perl -pe "s/\t/ <eos>/; s/\t/MATT/; s/\t/ <eos>/; s/MATT/\t/" > score.$set
done

for set in anaphora lexical_choice; do
    paste $set.prev.en $set.current.en $set.prev.fr | perl -pe "s/\t/ <eos>/" > decode.$set
done
