#! /usr/bin/env bash

# Authors: Adam Sperry, Travis Allen

# This script installs udev rules to grant non-root users permission
# to use Teensy devices. 

# Display summary text
echo
echo "This script will install udev rules to allow";
echo "serial communication with Teensy devices";
echo

# Get the absolute path to this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Install the udev rules needed to create the device files at boot time.
echo "Installing Udev rule...";
sudo cp $SCRIPT_DIR/00-teensy.rules /etc/udev/rules.d

# Print final message
echo
echo "udev rules have been installed!";
echo "You likely need to unplug the Teensy from the computer ";
echo "and plug it back in.";
