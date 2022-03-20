#!/bin/bash
# Bash Menu Script Example

PS3='Please enter your choice: '
names=`lsblk -d | tail -n+2 | awk '{print $1}'`
names_array=', ' read -r -a names <<< "$string"
sizes=`lsblk -d | tail -n+2 | awk '{print $4}'`
opts=`lsblk -d | tail -n+2 | awk '{print $1"("$4")"}'`
options=(${opts})
select opt in "${options[@]}"
do
    case $opt in
        "Option 1")
            echo "you chose choice 1"
            ;;
        "Option 2")
            echo "you chose choice 2"
            ;;
        "Option 3")
            echo "you chose choice $REPLY which is $opt"
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
