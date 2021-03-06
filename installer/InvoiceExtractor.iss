; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName GetEnv('APP_NAME')
#define MyAppDistDir GetEnv('DIST_DIR')
#define MyAppInstallerDir GetEnv('INSTALLER_DEST_DIR')

#define MyAppVersion "1.0"
#define MyAppPublisher "Alexander Genio"
#define MyAppExeName MyAppName + ".exe"
#define MyAppInstallerName MyAppName + "Installer"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A3CD900B-1D10-461F-89A0-52E946B85BB1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir={#MyAppInstallerDir}
OutputBaseFilename={#MyAppInstallerName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#MyAppDistDir}\{#MyAppName}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_asyncio.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_overlapped.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_queue.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\d3dcompiler_47.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\InvoiceExtractor.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\libcrypto-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\libEGL.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\libffi-7.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\libGLESv2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\libssl-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\MSVCP140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\MSVCP140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\opengl32sw.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\python39.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Core.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5DBus.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Gui.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Network.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Qml.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5QmlModels.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Quick.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Svg.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5WebSockets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\Qt5Widgets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\VCRUNTIME140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppDistDir}\{#MyAppName}\fitz\*"; DestDir: "{app}\fitz"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyAppDistDir}\{#MyAppName}\PIL\*"; DestDir: "{app}\PIL"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyAppDistDir}\{#MyAppName}\PyQt5\*"; DestDir: "{app}\PyQt5"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

