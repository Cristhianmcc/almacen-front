; Script de instalación profesional para AlmacenInstituto
[Setup]
AppName=AlmacenInstituto
AppVersion=1.0
AppPublisher=CrisLissRen
AppPublisherURL=https://almacen-instituto.onrender.com
AppSupportURL=https://almacen-instituto.onrender.com
AppUpdatesURL=https://almacen-instituto.onrender.com
DefaultDirName={pf}\AlmacenInstituto
DefaultGroupName=AlmacenInstituto
AllowNoIcons=yes
OutputBaseFilename=AlmacenInstituto-Setup
SetupIconFile=ui\img\icono.ico
Compression=lzma
SolidCompression=yes
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no
PrivilegesRequired=admin
VersionInfoCompany=CrisLissRen
VersionInfoDescription=Instalador de AlmacenInstituto
VersionInfoCopyright=Copyright © 2025 CrisLissRen
VersionInfoProductName=AlmacenInstituto

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "dist\AlmacenInstituto.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "ui\img\icono.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\AlmacenInstituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"
Name: "{commondesktop}\AlmacenInstituto"; Filename: "{app}\AlmacenInstituto.exe"; IconFilename: "{app}\icono.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\AlmacenInstituto.exe"; Description: "Iniciar AlmacenInstituto"; Flags: nowait postinstall skipifsilent

[LicenseFile]
LicenseFile=license.txt

[Tasks]
Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'Bienvenido al instalador de AlmacenInstituto';
  WizardForm.WelcomeLabel2.Caption := 'Este asistente le guiará en la instalación del sistema de inventario.';
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpLicense then
    WizardForm.LicenseAcceptedRadio.Checked := False;
end;
