# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0.html)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [14.4.1-beta] - 2023/03/25
- [added] update method in load_steps
- [added] in confirmation erasure process Ctrl+Z to Stop
- [changed] improve settings.ini.example file
- [fixed] display erase type at startup
- [fixed] fix erase steps when compute total steps
- [fixed] default values in dynamic steps

## [14.4.0-beta] - 2023/03/21
- [added] ask for confirmation to proceed with erasure (rel #4288)
- [added] allow to define each erasure step within settings (rel #4294)
- [added] print erasure steps on start
- [changed] settings.ini.example file
- [fixed] fix len dynamic steps
- [fixed] thread step type value as str instead int

## [14.3.0-beta] - 2023/03/16
- [added] boot_iso command in Makefile using qemu
- [changed] write zeros or random depending on the erasure type (rel #4286)
- [removed] WB_DEBUG settings variable
- [fixed] generate debug information by default (rel #4287)

## [14.2.0-beta] - 2023/02/22
- [added] display path where the snapshots will be saved (rel #4255)
- [added] print settings version at startup
- [added] if no token or url in settings don't post snapshot (rel #4260)
- [changed] improving feedback when there is no internet (rel #4254)
- [changed] modify default settings values with basic erasure (rel #4253)

## [14.1.0-beta] - 2023/01/24
- [added] new var settings version
- [added] execute erwb in /mnt 
- [added] cleanup bash history
- [changed] settings folder name
- [changed] snapshots folder name
- [changed] execute erwb in /mnt

## [14.0.0-beta] - 2022/08/04
- [added] upgrade base system to Debian 11
- [added] build ISO file script
- [added] Makefile  
- [changed] snapshot folder path
- [changed] configuration folder path

## [12.1.1-beta] - 2021/11/06
- [removed] encode snapshot feature with JWT
- [changed] snapshot folder path to /home/user/wb/snapshots/
- [changed] configuration folder path /home/user/wb/settings/

## [12.1.0-beta] - 2021/11/05
- [added] add datetime (hh:mm:ss) on snapshot filename
- [changed] snapshot folder path
- [changed] configuration folder path
- [fixed] erase settings variables
- [fixed] token on submit function
- [fixed] requirement pyjwt version on Debian 9

## [12.0.0-beta] - 2021/05/25
- [added] first version with decoupled configuration

## [11.1.0-beta]
- [added] adding new settings.ini file
- [added] adding config.py file with python-decouple
