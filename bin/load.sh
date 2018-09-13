#!/usr/bin/env bash

# Check for evidence of being sourced
if [ "${BASH_SOURCE[0]}" == "$0" ]
then
  echo "Error: it appears script has not been sourced--it will have no effect." >&2
  return 1
  exit 1
fi

EPISOMIZER_HOME=$1
if [ -z "$EPISOMIZER_HOME" ]; then
    echo "Error: EPISOMIZER_HOME not set" >&2
    return 1
    exit 1
fi

prepend() {
  echo "$1" | tr : '\n' | awk -v new="`readlink -f $2`$3" 'BEGIN { print new } $0 != new { print }' | tr '\n' : | sed 's/:$//'
}
addbin() {
  if [ -d $1 ]; then NEWPATH=$(prepend "$PATH" "$1"); export PATH="$NEWPATH"; fi
}
addpython() {
  if [ -d $1 ]; then NEWPYTHONPATH=$(prepend "$PYTHONPATH" "$1"); export PYTHONPATH="$NEWPYTHONPATH"; fi
}
addperl() {
  if [ -d $1 ]; then NEWPERL5LIB=$(prepend "$PERL5LIB" "$1"); export PERL5LIB="$NEWPERL5LIB"; fi
}

addpython $EPISOMIZER_HOME/lib/python
addbin $EPISOMIZER_HOME/bin
echo "Sourcing completed successfully"
