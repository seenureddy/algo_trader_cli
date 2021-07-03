set -e

# function definitions
help(){
    echo "Usage: $0 [OPTION]..."
    echo "  -h, --help         Show this help output"
    echo "  -p, --pep8         Run pep8 checks"
    echo "  -l, --lint         Run pylint checks and some extra custom style checks"
    echo "  -pl, --pl        Run pep8 and pylint checks"
    echo "  -b, --bandit       Run bandit source code security analyser"
    echo "  --no-coverage      Don't make a unit test coverage report"
    echo ""
    exit 0;
}

fail(){
    echo "FAILURE"
    echo -e "$1"
    exit 1;
}

run_python_tests(){
    COVERAGE_REPORT=results/coverage.xml
    TEST_REPORT=results/test_results.xml

    if $(echo "${OSTYPE}" | grep -q darwin); then
        SED_COMMAND="sed -i'' -e"
    else
        SED_COMMAND="sed -i"
    fi

    pytest --cov-config=.coveragerc --cov=tests/ --cov-report term --cov-report xml:$COVERAGE_REPORT --junit-xml=$TEST_REPORT

    if [ $include_coverage -eq 1 ]; then
        COVERAGE_REPORT=$(coverage report -m)
        echo "Coverage Report"
        echo "$COVERAGE_REPORT"
    fi
    echo "checking the status"
    # Fixes the paths in the coverage report. If your coverage is showing as zero in the
    # Sonar Web UI, then please refer to the following wiki page for more information:
    # https://wiki.cisco.com/display/ITSDLC/Paths+in+Pytest+Test+and+Coverage+Files
    $SED_COMMAND '/.*<\/source>/s@\/app@\.@g' results/coverage.xml

    echo " run tests function ran successfully"
}

run_lint_check(){
    echo "************** Running pylint checks ******************************"
    pylint no2_cli/ --rcfile=".pylintrc"
    echo "SUCCESS"
}

run_bandit_check(){
    echo "************** Running bandit checks ******************************"
    bandit -r no2_cli/ -s B101,B110,B106,B322
    echo "SUCCESS"
}

# Determine script behavior based on passed options

# default behavior
just_lint=0
just_unit=0
just_func=0
just_bandit=0
testargs=""
include_coverage=1
all_style_checks=0

while [ "$#" -gt 0 ]; do
    case "$1" in
        -h|--help) shift; help;;
        -l|--lint) shift; just_lint=1;;
        -u|--unit) shift; just_unit=1;;
        -f|--func) shift; just_func=1;;
        -pl|--pl) shift; all_style_checks=1;;
        -b|--bandit) shift; just_bandit=1;;
        --no-coverage)shift; include_coverage=0;;
        *) testargs="$testargs $1"; shift;
    esac
done



if [ $just_unit -eq 1 ]; then
    run_python_tests
    exit $?
fi

if [ $just_lint -eq 1 ]; then
    run_lint_check
    exit $?
fi

if [ $just_bandit -eq 1 ]; then
    run_bandit_check
    exit $?
fi

if [ $all_style_checks -eq 1 ]; then
    run_lint_check
    exit $?
fi

#run_python_tests || exit
