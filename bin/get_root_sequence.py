#!/usr/bin/env python3

import json
import argparse

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract root sequence from JSON and write to FASTA.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input auspice JSON file with an inline root sequence (e.g. root_sequence )"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output the inline root sequence as a FASTA file"
    )
    return parser.parse_args()

def extract_root_sequence(json_file):
    """Extracts the root nucleotide sequence from an auspice JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        return data["root_sequence"]["nuc"]
    except KeyError:
        raise ValueError("Could not find root_sequence.nuc in the input JSON.")

def write_fasta(sequence, output_file):
    """Writes the sequence to a FASTA file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(">root_sequence\n")
        f.write(f"{sequence}\n")

def main():
    args = parse_args()

    root_seq = extract_root_sequence(args.input)
    write_fasta(root_seq, args.output)

if __name__ == "__main__":
    main()
