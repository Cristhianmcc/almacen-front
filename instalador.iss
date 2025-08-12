; =============================================================================
; Script de instalación para AlmacenInstituto
; Versión: 2.0 - Instalador Profesional
; Autor: CrisLissRen
; Fecha: 2025
; =============================================================================

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName=Sistema de Almacén - Instituto
AppVersion=2.0.0
AppVerName=Sistema de Almacén - Instituto v2.0.0
AppPublisher=CrisLissRen
AppPublisherURL=https://almacen-instituto.onrender.com
AppSupportURL=https://almacen-instituto.onrender.com
AppUpdatesURL=https://almacen-instituto.onrender.com
AppContact=soporte@almacen-instituto.com
AppComments=Sistema profesional de gestión de inventario con lógica FEFO
AppCopyright=Copyright © 2025 CrisLissRen. Todos los derechos reservados.

DefaultDirName={autopf}\AlmacenInstituto
DefaultGroupName=Sistema de Almacén
AllowNoIcons=yes
OutputBaseFilename=AlmacenInstituto-Setup-v2.0
SetupIconFile=ui\img\icono.ico
UninstallDisplayIcon={app}\AlmacenInstituto.exe
UninstallDisplayName=Sistema de Almacén - Instituto

Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=2

PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no

AllowUNCPath=false
UsePreviousAppDir=yes
DirExistsWarning=yes
CreateAppDir=yes

OutputDir=Output

VersionInfoVersion=2.0.0.0
VersionInfoCompany=CrisLissRen
VersionInfoDescription=Sistema de Almacén - Instituto - Instalador
VersionInfoCopyright=Copyright © 2025 CrisLissRen
VersionInfoProductName=Sistema de Almacén - Instituto
VersionInfoProductVersion=2.0.0.0

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startupicon"; Description: "{cm:AutoStartProgram,Sistema de Almacén}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "associatefiles"; Description: "&Asociar archivos .alm"; GroupDescription: "Opciones de archivo:"; Flags: unchecked
Name: "firewall"; Description: "Configurar &Firewall de Windows"; GroupDescription: "Configuración de red:"; Flags: unchecked

[Files]
Source: "dist\AlmacenInstituto\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "ui\img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sistema de Almacén - Instituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"; Comment: "Sistema de gestión de inventario FEFO"
Name: "{group}\Desinstalar Sistema de Almacén"; Filename: "{uninstallexe}"; IconFilename: "{app}\icono.ico"
Name: "{userdesktop}\Sistema de Almacén - Instituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Sistema de Almacén - Instituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"; Tasks: quicklaunchicon
Name: "{userstartup}\Sistema de Almacén - Instituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"; Tasks: startupicon

[Registry]
Root: HKCU; Subkey: "Software\AlmacenInstituto"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\AlmacenInstituto"; ValueType: string; ValueName: "Version"; ValueData: "2.0.0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\AlmacenInstituto"; ValueType: string; ValueName: "InstallDate"; ValueData: "{code:GetInstallDate}"; Flags: uninsdeletekey

Root: HKCR; Subkey: ".alm"; ValueType: string; ValueName: ""; ValueData: "AlmacenInstitutoFile"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "AlmacenInstitutoFile"; ValueType: string; ValueName: ""; ValueData: "Archivo de Almacén Instituto"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "AlmacenInstitutoFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icono.ico"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "AlmacenInstitutoFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\AlmacenInstituto.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: associatefiles

[Run]
Filename: "{app}\AlmacenInstituto.exe"; Description: "{cm:LaunchProgram,Sistema de Almacén - Instituto}"; Flags: nowait postinstall skipifsilent
Filename: "netsh.exe"; Parameters: "advfirewall firewall add rule name=""Sistema de Almacén Instituto"" dir=in action=allow program=""{app}\AlmacenInstituto.exe"" enable=yes"; Flags: runhidden; Tasks: firewall; StatusMsg: "Configurando firewall de Windows..."

[UninstallDelete]
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: dirifempty; Name: "{app}"

[Code]
function GetInstallDate(Param: String): String;
begin
  Result := GetDateTimeString('yyyy-mm-dd', '-', ':');
end;

procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel1.Caption := 'Bienvenido al instalador del Sistema de Almacén - Instituto';
  WizardForm.WelcomeLabel2.Caption := 'Este asistente le guiará en la instalación del sistema profesional de gestión de inventario con lógica FEFO.' + #13#10 + #13#10 + 
                                     'Antes de continuar, asegúrese de:' + #13#10 +
                                     '• Cerrar todas las aplicaciones abiertas' + #13#10 +
                                     '• Tener permisos de administrador' + #13#10 +
                                     '• Tener conexión a internet para la configuración inicial';
end;
