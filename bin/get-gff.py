#! /usr/bin/env python

import argparse
from Bio import SeqIO

def sanitize_id(s):
    """Sanitize ID strings to be GFF3-safe."""
    return s.replace(" ", "_").replace(":", "_")

def genbank_to_gff3(input_file, output_file):
    with open(output_file, 'w') as gff_out:
        for record in SeqIO.parse(input_file, "genbank"):
            seq_id = record.id
            seq_len = len(record.seq)

            # GFF3 required headers
            gff_out.write("##gff-version 3\n")
            gff_out.write(f"##sequence-region {seq_id} 1 {seq_len}\n")

            gene_id_map = {}  # Maps gene names to unique IDs (for Parent)

            gene_counter = 1
            cds_counter = 1

            for feature in record.features:
                if feature.type in ['gene', 'CDS']:
                    start = int(feature.location.start) + 1  # GFF is 1-based
                    end = int(feature.location.end)
                    strand = '+' if feature.location.strand == 1 else '-'
                    qualifiers = feature.qualifiers

                    gene_name = qualifiers.get('gene', qualifiers.get('product', ['unknown']))[0]
                    safe_name = sanitize_id(gene_name)

                    if feature.type == "gene":
                        gene_id = f"gene-{safe_name}"
                        gene_id_map[(start, end)] = gene_id  # Use location as key
                        attr_str = f"ID={gene_id};Name={safe_name}"
                    else:  # CDS
                        parent_gene_id = gene_id_map.get((int(feature.location.start) + 1, end), f"gene-{safe_name}")
                        cds_id = f"cds-{safe_name}"
                        attr_str = f"ID={cds_id};Parent={parent_gene_id};Name={safe_name}"

                    gff_line = f"{seq_id}\tGenbank\t{feature.type}\t{start}\t{end}\t.\t{strand}\t.\t{attr_str}\n"
                    gff_out.write(gff_line)

def main():
    parser = argparse.ArgumentParser(description="Convert a GenBank file to GFF3 format.")
    parser.add_argument("--input", required=True, help="Path to the input GenBank (.gb) file.")
    parser.add_argument("--output", required=True, help="Path to the output GFF3 (.gff3) file.")
    args = parser.parse_args()

    genbank_to_gff3(args.input, args.output)

if __name__ == "__main__":
    main()
