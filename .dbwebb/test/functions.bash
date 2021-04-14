#
# Makes sure that the given python version ($1) is supported couse.
#
check_python_version () {
    command=$1
    VERSION=$(${command} -V 2>&1 | cut -d\  -f 2) # python 2 prints version to stderr
    VERSION=(${VERSION//./ }) # make an version parts array 
    if [[ ${VERSION[0]} -lt 3 ]] || [[ ${VERSION[0]} -eq 3 && ${VERSION[1]} -lt 5 ]] ; then
        return 1
    fi
    return 0
}

#
# Gets the valid "python" command 
#
get_python_command () {
    for cmd in python3 python py py3
    do
        check_python_version $cmd
        if [[ $? -eq 0 ]] ; then
            py=$cmd
            return 0
        fi
    done
    echo "Can't find valid Python command. Python 3.5+ needed!"
    echo "Have tried with python3, python, py and py3"
    exit 1
}


#
# Checks if it is a valid testsuite for the examiner script.
#
is_valid_suite () {
    if [ -z $(find "${COURSE_REPO_BASE}/.dbwebb/test/suite.d" -name ${TESTSUITE} -and -type d) ]
    then
        printf "'${COURSE}' + '${TESTSUITE}' is not a valid target.\n"
        exit 1
    fi
}
