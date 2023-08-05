#!/bin/bash

get_os(){
	platform='unknown'
	unamestr=$(uname)

	if [[ "$unamestr" == "Linux" ]]; then
        	echo "Linux"
	elif [[ "$unamestr" == "MINGW32_NT" ]]; then
        	echo "Windows"
	fi		
}

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
	echo "Error: virtual env is not installed. Please install it using the following command. 'pip insatall virtualenv' and try again"
	exit 1
fi 

# Name of virtual environment
VENV_NAME="tracker"

# check the OS Of the machine
OS=$(get_os)

# Create Virtual Environment
echo "========== CREATING VIRTUAL ENVIRONMENT =========="
virtualenv "${VENV_NAME}"
echo "========== VIRTUAL ENVIRONMENT CREATED =========="

# Activate the environment
echo "========== ACTIVATING VIRTUAL ENVIRONMENT =========="
if [ "$OS" == "Linux" ]; then
	source "$VENV_NAME/bin/activate"
elif [ "$OS" == "Windows" ]; then
	"$VENV_NAME/Scripts/Activate"
fi 
echo "========== VIRTUAL ENVIRONMENT ACTIVATED =========="

#Install dependencies
echo "========== INITIATING DEPENDENCY INSTALLATION =========="
pip install -r requirements.txt
echo "========== DEPENDENCY INSTALLATION COMPLETE =========="

# Deactivate Environment
echo "========== DEACTIVATING VIRTUAL ENVIRONMENT =========="
deactivate
echo "========== VIRTUAL ENVIRONMENT DEACTIVATED =========="

echo "========== Virtual environment created and dependencies installed successfully! =========="
