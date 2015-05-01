##
# Copyright (c) 2015, Dominique Pizzie
# Copyrights licensed under the MIT License (MIT).
# See the accompanying LICENSE file for terms.
##

# This script is used to provision VPN accounts and will output a script file
 
import argparse

parser = argparse.ArgumentParser(
    description="""This program will take a list or file of users and create
        a script for a Fortigate UTM to create VPN accounts.""")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-f', '--file', help="input filename (must be in same directory as script)")
group.add_argument('-u', '--users', nargs='+', help="space delimited list of users")
group.add_argument('-ug', '--usergroup', nargs='+', help="space delimited list of user:group")

parser.add_argument('-g', '--group', help="select group user(s) should be added to")
parser.add_argument('-o', '--output', default='FortigateScript.txt',
    help="output file name (default: %(default)s)")

args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as inputFile:
        clidList = inputFile.read().splitlines()
elif args.users:
    clidList = args.users
elif args.usergroup:
    userList,groupList = [],[]
    for userGroups in args.usergroup:
        userGroups = userGroups.split(":")
        userList.append(userGroups[0])
        groupList.append(userGroups[1])
    clidList = userList
   
with open(args.output, 'w') as outFile:
    outFile.write("config vdom\n")
    outFile.write("edit VPN_gateway\n")
    for clid in clidList:
        outFile.write("config user local\n")
        outFile.write("\tedit " + clid + "\n")
        outFile.write("\tset type ldap\n")
        outFile.write("\tset ldap-server [insert server name here]\n")
        outFile.write("end\n")
    if args.group:
        groups = args.group.replace(' ', '\ ')
        outFile.write("config user group\n")
        outFile.write("\tedit " +groups+ "\n")
        outFile.write("\tset member " + " ".join(clidList) + "\n")
        outFile.write("end\n")
    elif args.usergroup:
        for clid, group in zip(clidList,groupList):
            group = group.replace(' ', '\ ')
            outFile.write("config user group\n")
            outFile.write("\tedit " +group+ "\n")
            outFile.write("\tset member " + clid + "\n")
            outFile.write("end\n")
