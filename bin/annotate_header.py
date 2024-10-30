import argparse
import csv

def main():
    parser = argparse.ArgumentParser(description="Replace FASTA headers with annotations from a TSV file.")
    parser.add_argument("--metadata", required=True, help="Path to the metadata TSV file")
    parser.add_argument("--metadata-columns", required=True, help="Comma-separated list of column names to include in the header")
    parser.add_argument("--sequences", required=True, help="Path to the input FASTA file")
    args = parser.parse_args()

    # Read metadata
    metadata = {}
    with open(args.metadata, 'r') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            accession = row['accession']  # Assuming 'accession' is the column name for the matching identifier
            metadata[accession] = [row[col.strip()] for col in args.metadata_columns.split(',')]

    # Process FASTA file
    with open(args.sequences, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith('>'):
                accession = line.strip()[1:].split('|')[0]  # Extract accession from the original header
                if accession in metadata:
                    new_header = f">{accession}|{'|'.join(metadata[accession])}"
                    print(new_header)
                else:
                    print(line.strip())
            else:
                print(line.strip())

if __name__ == "__main__":
    main()