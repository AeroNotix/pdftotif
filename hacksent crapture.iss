; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{52C10E67-0021-4F2B-AF91-8B8F818C2333}
AppName=Hacksent Crapture
AppVersion=0.1
;AppVerName=Hacksent Crapture 0.1
AppPublisher=Aaron
AppPublisherURL=www.hp.com
AppSupportURL=www.hp.com
AppUpdatesURL=www.hp.com
DefaultDirName={pf}\Hacksent Crapture
DefaultGroupName=Hacksent Crapture
OutputDir=C:\Documents and Settings\francea\Desktop\hacksent crapture
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Documents and Settings\francea\Desktop\scanning_tools\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Documents and Settings\francea\Desktop\scanning_tools\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Documents and Settings\francea\Desktop\scanning_tools\gs\*"; DestDir: "{app}\gs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Documents and Settings\francea\Desktop\scanning_tools\gs853w32.exe"; DestDir: "{app}";
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Hacksent Crapture"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,Hacksent Crapture}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Hacksent Crapture"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\gs853w32.exe"
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Hacksent Crapture}"; Flags: nowait postinstall skipifsilent
