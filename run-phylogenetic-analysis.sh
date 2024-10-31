#! /usr/bin/env bash

set -euv

INPUT_SEQUENCE_FILE=$1
OUTDIR=results

[[ -d $OUTDIR ]] || mkdir $OUTDIR

# python annotate_header.py \
#   --metadata wnv.tsv \
#   --metadata-columns "region,country,division,host,clade_membership,p_lineage,date" \
#   --sequences wgs.fasta \
#   | tr ' ' '_' \
#   > wnv.fasta

mafft --auto --adjustdirection --thread 4 $INPUT_SEQUENCE_FILE > ${OUTDIR}/aligned.fasta

fasttree -nt ${OUTDIR}/aligned.fasta > ${OUTDIR}/tree.nwk

# Open in FigTree
# Midpoint Root
# Start pulling out outliers
# Start adding filtering
# Start adding metadata and subsampling
# Remove duplicates
