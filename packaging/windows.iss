[Setup]
AppId=n0ngXarm.Allzip
AppName=Allzip
AppVersion=1.1.1
AppPublisher=n0ngXarm
AppPublisherURL=https://github.com/n0ngXarm/Allzip
DefaultDirName={localappdata}\Programs\Allzip
DefaultGroupName=Allzip
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=Allzip-1.1.1-windows-x64-setup
SetupIconFile=..\assets\app.ico
UninstallDisplayIcon={app}\Allzip.exe
LicenseFile=..\LICENSE
Compression=lzma2
SolidCompression=yes
CloseApplications=yes
RestartApplications=no
WizardStyle=modern
[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; Flags: unchecked
[Files]
Source: "..\dist\Allzip\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\Allzip"; Filename: "{app}\Allzip.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\Allzip"; Filename: "{app}\Allzip.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\Allzip.exe"; Description: "Open Allzip"; Flags: nowait postinstall skipifsilent
