# TinyLabs

*~ Huge application in a bottle ~*

&nbsp;

&nbsp;

## I - Description

## Overview

As indicated by its name, TinyLabs is a tiny application that allows you to create & manage some little things called : *"labs"*. \
A labs is nothing more than a directory on your computer or on a distant server (equiped with some settings files & stuff). \
A lab has 3 roles :
 - Store projects (under the form of a GIT repository)
 - Perform scheduled actions on them (tests, CI, CD... basically: DevOps)
 - Manage access towards a variety of users
 - Organize your projects using groups

The names & most of the basic ideas have been taken from the [GitLab](https://gitlab.com) project and a tiny bit from [GitHub](https://github.com) as well.

&nbsp;

### Objectives

The main objective of TinyLabs is to provide an **easilly accessible** project manager for every one. \

Here are some points where TinyLabs offers easiness over some existing repository managers :
 - TinyLabs is mostly **PASSIVE**, that means that labs does not necessarily require an active server running. \
 - The only resource you **can** require to make a lab work is to launch its **scheduler** but you will need this only if you are performing scheduled operations. \
   A lab with no scheduled actions will not have to run its scheduler.
 - Groups & Projects inside a lab are fully transparent in filesystem so it is possible to manage your data storage over several devices using mount points or symbolic links for instance.

&nbsp;

### Requirements

Here are all the requirements for installing the labs application :
 - A GNU/Linux operating system.
 - Python3 package.
 - Make package.

Here are all the requirements for the storage devices that stores your labs :
 - Partitions in ext4 format.

&nbsp;

&nbsp;


## II - Installation Process

### Install TinyLabs
```bash
./TinyLabs/install
```
By default the installation directory is `/opt/TinyLabs` but you can modify it by editing the `install` program. \
**WARNING : Mind that you will have to edit source file `src/tools/general.py` as well.**

&nbsp;

### Uninstall TinyLabs

To uninstall TinyLabs, you just have to remove the directory where you install it :
```bash
#by default: /opt/TinyLabs
rm --recursive /opt/TinyLabs
```
**NOTE: This will not affect the labs you have deployed with it. \
It only concerns the lab management application.**

&nbsp;

&nbsp;


## III - Use

There is 2 ways of using TinyLabs :
 - CLI (Command line interface)
 - WUI (Web User interface)

### CLI

TinyLabs can be accessed using the program installed before. \
```bash
tinylabs --help
```

Everything you should know after this is given in the `--help` menus.

&nbsp;

### WUI

This option has not been implemented yet. \
**WE'RE HIRING !!!**

&nbsp;

That's it for TinyLabs. \
You can now enjoy both simplicity & efficiency !

&nbsp;

&nbsp;


*Contact    : i.a.sebsil83@gmail.com*<br>
*Youtube    : https://www.youtube.com/user/IAsebsil83*<br>
*Repository : https://github.com/iasebsil83*<br>

Let's Code ! &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By I.A.
