#!/usr/bin/env bash

# =============================================================================
# Maven-like Test Execution Script for pytest
# =============================================================================
# Usage:
#   ./run_tests.sh --env=QAB --tags=smoke
#   ./run_tests.sh --env=PROD --tags="smoke and critical"
#   ./run_tests.sh --clean
# =============================================================================

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT="DEV"
TAGS=""
CLEAN=false
VERBOSE=false
ALLURE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env=*)
            ENVIRONMENT="${1#*=}"
            shift
            ;;
        --tags=*)
            TAGS="${1#*=}"
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --allure)
            ALLURE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Print configuration
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🧪 Running Tests${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
if [ -n "$TAGS" ]; then
    echo -e "Tags:        ${YELLOW}$TAGS${NC}"
fi
echo -e "${GREEN}========================================${NC}"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# Build pytest command
PYTEST_CMD="pytest"

# Add environment parameter
PYTEST_CMD="$PYTEST_CMD --env=$ENVIRONMENT"

# Add tags filter
if [ -n "$TAGS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m \"$TAGS\""
fi

# Add verbosity
if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -vv"
else
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add Allure reporting
if [ "$ALLURE" = true ] || [ "$CLEAN" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --alluredir=allure-results"
    if [ "$CLEAN" = true ]; then
        PYTEST_CMD="$PYTEST_CMD --clean-alluredir"
    fi
fi

# Run tests
echo -e "${YELLOW}🚀 Executing: $PYTEST_CMD${NC}"
echo ""
eval $PYTEST_CMD
TEST_EXIT_CODE=$?

# Generate Allure report if requested
if [ "$ALLURE" = true ]; then
    echo ""
    echo -e "${YELLOW}📊 Generating Allure report...${NC}"
    allure serve allure-results
fi

# Exit with test exit code
exit $TEST_EXIT_CODE
