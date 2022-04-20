#!/bin/bash

# Colors.
readonly BOLD_WHITE="\e[1;37m"
readonly SUCCESS="\e[1;32m"
readonly ERROR="\e[1;31m"
readonly RESET="\e[0m"

# Prints out the preceding string to stderr and exits with status code 1.
function abort() {
	printf "${ERROR}Error${BOLD_WHITE}: %s${RESET}\n" "$@" >&2
	exit 1
}

# Installs BuildDoc to your system!
function install_builddoc() {
	printf "Install!"
}

# Checking if the script was run in bash.
if [[ -z "${BASH_VERSION}" ]]
then
	abort "You must run this script in bash."
else
	install_builddoc
fi
