#! /usr/bin/env python3

import argparse
import re

def parse_cds_range(genbank_file):
    min_start = float('inf')
    max_end = 0

    with open(genbank_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip().startswith('CDS'):
                matches = re.findall(r'(\d+)\.\.(\d+)', line)
                if matches:
                    start, end = map(int, matches[0])
                    min_start = min(min_start, start)
                    max_end = max(max_end, end)

    return min_start, max_end

def trim_genbank(input_file, output_file, start, end):
    new_length=end-start+1
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        sequence = ""
        in_sequence = False
        for line in infile:
            if line.startswith('ORIGIN'):
                in_sequence = True
                outfile.write(line)
            elif in_sequence:
                if line.strip() == '//':
                    in_sequence = False
                    trimmed_seq = sequence[start-1:end]
                    for i in range(0, len(trimmed_seq), 60):
                        outfile.write(f"{i+1:>9} {' '.join(trimmed_seq[i:i+60][j:j+10] for j in range(0, 60, 10))}\n")
                    outfile.write(line)
                else:
                    sequence += ''.join(line.split()[1:])
            elif line.startswith('LOCUS'):
                #LOCUS       KM822128                3428 bp    RNA     linear   VRL 14-OCT-2014
                matches = re.findall(r'(.+\s)(\d+)(\s+bp.+)', line)
                outfile.write(f"{matches[0][0]}{new_length}{matches[0][2]}\n")
            elif any(line.strip().startswith(feature) for feature in ['CDS', 'gene', 'mRNA']):
                # CDS             complement(1..3428)
                matches = re.findall(r'(.+)complement\((\d+)\.\.(\d+)\)', line)
                if matches:
                    outfile.write(f"{matches[0][0]}complement({int(matches[0][1])-start+1}..{int(matches[0][2])-start+1})\n")
                else:
                    # CDS             1..3428
                    matches = re.findall(r'(.+\s)(\d+)\.\.(\d+)', line)
                    if matches:
                        outfile.write(f"{matches[0][0]}{int(matches[0][1])-start+1}..{int(matches[0][2])-start+1}\n")
            else:
                outfile.write(line)

def main():
    parser = argparse.ArgumentParser(description="Trim GenBank file based on CDS range")
    parser.add_argument("input_file", help="Path to the input GenBank file")
    parser.add_argument("output_file", help="Path to the output GenBank file")
    args = parser.parse_args()

    start, end = parse_cds_range(args.input_file)
    print(f"Detected range: {start}..{end}")

    trim_genbank(args.input_file, args.output_file, start, end)
    print(f"Trimmed GenBank file saved as {args.output_file}")

if __name__ == "__main__":
    main()