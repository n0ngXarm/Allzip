# Windows installer validation: Allzip 1.1.1

Build commit: 67a50668135396c5f7fe9a6cbc46932418cc1eb6
Windows CI: https://github.com/n0ngXarm/Allzip/actions/runs/42184988875
Result: SUCCESS

Verified: regression suite; per-user installer; install path with Thai characters and spaces; installed GUI launch; reinstall/update; Start Menu shortcut; HKCU uninstall registration; uninstallation; separate user fixture retained.

10 regression tests. Installed runtime creates and reads back a ZIP with a Thai input filename and opens the Tk GUI. Failure/overwrite preservation, empty folders, unreadable files and publication races are covered. No 10+ GB acceptance claim.

Microsoft Defender custom scan completed on the CI runner (see SECURITY-REPORT.txt). Binaries are unsigned; SmartScreen reputation and every antivirus cannot be guaranteed. CI uses windows-latest, not a human-operated Windows 10/11 device. No firewall changes, security exclusions, services or startup tasks are installed.
