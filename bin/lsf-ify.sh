#! /usr/bin/env bash
# Auth: Jennifer Chang
# Date: 2026/03/09

set -e
set -u

# === Usage Statement
if [[ $# -lt 1 ]]; then
  echo "USAGE: bash lsf-ify.sh [script.sh] > [script.lfs]"          >&2
  echo "  Given a bash script"  >&2
  echo "  Return a formatted lsf script">&2
  echo " " >&2
  exit 0
fi

# === Print LSF Header using HEREDOC method
cat << '_EOF'
#! /usr/bin/env bash
#BSUB -n 1
#BSUB -o out.%J
#BSUB -e err.%J
#BSUB -J JOBB
set -e
set -u

start=`date +%s`

# === Load Modules here
## TODO: source ~/mybin/config_module_names.sh        # <= switching between ceres and condo, may need to edit path
# == Module names are M_PARALLEL or similar
# module load <name of module>
_EOF

# === attempt to pull modules from main script
grep "# module load" $1 | sed 's/# module/module/g' 

cat << '_EOF'

# === Get input size and module versions
# echo "started JOBB.lfs: " `date` " seconds" >> LOGGER.txt
# module list >> LOGGER.txt
# ls -ltr ${INPUT}    # <= list any input files here
# === Main Program
_EOF

# === Print bash script without the shebang and my usual headers
cat $1 |\
    grep -v "^#!" |\
    grep -v "# module load" |\
    grep -v "# Auth" |\
    grep -v "# Date" |\
    grep -v "set -e" |\
    grep -v "set -u"

# === Print LSF Footer using HEREDOC method
cat<<'_EOF'

end=`date +%s`

# === Log msgs and resource use                          
echo "ran JOBB.lfs: " `date` "; Execution time: " $((${end}-${start})) " seconds" >> LOGGER.txt
_EOF