#! /usr/bin/env python
# ChatGPT 4o 2025-07-15
# PROMPT: Since recent Snakemake dropped --stats support can we create a python scripts that takes a benchmark directory (e.g. benchmarks/rule_name.txt) and generate a stats.json file?
# PROMPT: Ah, allow for nested benchmark files (e.g. benchmark/{gene}/rule_name.txt)
# PROMPT: Can we add arg parse for "--benchmark-dir" with default "benchmarks" and output "--stats" with default "stats.json"?
# PROMPT: Files section is missing, why?
# ANSWER: (summarized) Not enough information of generated output file in the benchmark files, only timing, can create file entries per rule (e.g. benchmark file)
# PROMPT: Yes, create file entries per rule
# PROMPT: Noticed start and stop time are missing, can we use the benchmark file creation date as stop-time and use duration to infer back the start time?
# TEST: Drag and drop onto https://blab.github.io/snakemake-stats/
# DISCUSSION: Next steps (optional) could be generating an html execution report directly (could look at the above code) or try to create something simialr to https://www.nextflow.io/docs/latest/reports.html#execution-timeline

import os
import csv
import time
import json
import argparse
from statistics import mean
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(
        description="Aggregate Snakemake benchmark files into a stats.json-style summary with rule and file stats."
    )
    parser.add_argument("--benchmark-dir", default="benchmarks", help="Directory with benchmark .txt files")
    parser.add_argument("--stats", default="stats.json", help="Output JSON file path")
    return parser.parse_args()

def find_benchmark_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".txt"):
                yield os.path.join(dirpath, file)

def format_time(epoch_seconds):
    return time.strftime("%a %b %e %H:%M:%S %Y", time.localtime(epoch_seconds))

def parse_benchmark(filepath):
    runtimes = []
    file_records = []

    try:
        stop_epoch = os.path.getmtime(filepath)
        stop_str = format_time(stop_epoch)
    except Exception:
        stop_epoch = None
        stop_str = None

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                duration = float(row["s"])
                runtimes.append(duration)

                if stop_epoch:
                    start_epoch = stop_epoch - duration
                    start_str = format_time(start_epoch)
                else:
                    start_str = None

                record = {
                    "start-time": start_str,
                    "stop-time": stop_str,
                    "duration": duration,
                    "priority": int(row.get("priority", 0)),
                    "resources": {
                        "_cores": int(row.get("cores", 1)),
                        "_nodes": int(row.get("nodes", 1)),
                        "tmpdir": row.get("tmpdir", "/tmp")
                    }
                }
                file_records.append(record)
            except (KeyError, ValueError):
                continue

    return runtimes, file_records

def collect_stats(benchmark_dir):
    rules = {}
    files = {}
    total_runtime = 0.0

    for filepath in find_benchmark_files(benchmark_dir):
        runtimes, file_records = parse_benchmark(filepath)
        if not runtimes:
            print(f"Warning: no valid 's' runtimes in {filepath}")
            continue

        rel_path = os.path.relpath(filepath, benchmark_dir)
        rule_id = rel_path.replace(os.sep, "__").replace(".txt", "")

        rules[rule_id] = {
            "mean-runtime": mean(runtimes),
            "min-runtime": min(runtimes),
            "max-runtime": max(runtimes)
        }

        for i, record in enumerate(file_records):
            file_id = f"{rule_id}__{i}" if len(file_records) > 1 else rule_id
            files[file_id] = record
            total_runtime += record["duration"]

    return {
        "total_runtime": total_runtime,
        "rules": rules,
        "files": files
    }

def write_json(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

def main():
    args = parse_args()
    stats = collect_stats(args.benchmark_dir)
    write_json(stats, args.stats)
    print(f"Stats written to {args.stats}")

if __name__ == "__main__":
    main()
