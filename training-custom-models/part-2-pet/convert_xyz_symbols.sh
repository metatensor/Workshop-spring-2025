#!/bin/bash

input="ethanol.xyz"
output="ethanol_converted.xyz"

# Mapping: 1 → C, 2 → H, 3 → O
awk '{
  if (NF == 4 && $1 ~ /^[123]$/) {
    atom = ($1 == 1 ? "C" : ($1 == 2 ? "H" : "O"))
    printf "%s %s %s %s\n", atom, $2, $3, $4
  } else {
    print $0
  }
}' "$input" > "$output"

echo "Converted '$input' → '$output' with atom types labeled."