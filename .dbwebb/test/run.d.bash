#!/usr/bin/env bash
#
# Executes scripts depedning on the "test_suite".
#
# Arguments:
#  course_dir           Absolute path to the basedir of the course repo.
#  course               Nickname of the course.
#  acronym              Acronym of the user executing the script.
#  test_suite           Name of the testsuite to execute.
#  <optional args>      Optional arguments
#

. ".dbwebb/test/functions.bash"

# Usage
if (( $# < 3 )); then
    printf "Usage: %s <course_dir> <course> <acronym> <test_suite> <optional args...>\n" \
        "$( basename -- "$0" )"
    exit 1
fi



# Handles optional agruments and if no "suit" is given.
tmp_test_suit="$4"
tmp_arguments="${@:5}"
if [[ -z "$tmp_test_suit" || $tmp_test_suit == -* ]]; then
    tmp_test_suit=$(pwd | awk -F/ '{print $NF}')
    tmp_arguments="${@:4}"
fi


# Prepare configuration
get_python_command
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHON_EXECUTER=$py
export EXAMINER_RUNNER="${DIR}/examiner/run_tests.py"
export COURSE_REPO_BASE="$1"
export COURSE="$2"
export ACRONYM="$3"
export ARGUMENTS=$tmp_arguments
export TESTSUITE=$tmp_test_suit



# Prepare the logdir and logfile
LOG_DIR="$COURSE_REPO_BASE/.log/test"
[[ -d $LOG_DIR ]] || install -d "$LOG_DIR"
export LOG="$( realpath "$COURSE_REPO_BASE/.log/test/$TESTSUITE.log" )"
(( $? == 0 )) || exit 2
> "$LOG" || exit 1



# Export to be used in test scripts
MSG_OK="\033[0;30;42mOK\033[0m"
MSG_DONE="\033[1;37;40mDONE\033[0m"
export MSG_WARNING="\033[43mWARNING\033[0m"
export MSG_FAILED="\033[0;37;41mFAILED\033[0m"



#
# Print a header
#
function header {
    printf "\033[32;01m>>> -------------- %-20s -------------------------\033[0m\n" "$1"
}



#
# Log to summary
#
function doLog {
    if (( $1 )); then
        echo "[-] $2
===========================================================" >> "$LOG"
    else
        echo "[+] $2
===========================================================" >> "$LOG"
    fi

    exit $1
}

export -f doLog



# prepare basename of filenames inside scripts.d/
examiner="examiner"
lab="lab"
validate="validate"

case "$TESTSUITE" in
    "kmom10" | try[1-9] ) echo "Not yet implemented" && exit 1  ;;
    kmom0[1-6]          ) files=($validate $lab $examiner)      ;;
    lab[1-9]            ) files=($validate $lab)                ;;
    *                   )

        is_valid_suite
        files=($validate $examiner)
        ;;
esac


# Executes scripts
header "Start"
printf "[%s] %s %s %s\n" "$ACRONYM" "$TARGET" "$TESTSUITE" "$( date )"

for file in "${files[@]}"; do
    output=
    target="scripts.d/${file}.d.bash"

    echo && header "$target"

    bash "${DIR}/$target"
    if (( $? )); then
        output="$MSG_FAILED $target
"
    else
        output="$MSG_OK $target
"
    fi
    printf "$output"
    summary="$summary$output"
done

# Adding summary to log-file
printf "$(header "Test summary")
$summary\n" >> "$LOG"

# Printing the output
printf "
$(header "LOG")
$(cat $LOG)

--------------------------------------------
Saved a log of the test output: less -R '$LOG'\n
"