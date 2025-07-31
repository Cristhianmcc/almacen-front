[Setup]
AppName=Almacen Instituto
AppVersion=1.0
DefaultDirName={pf}\AlmacenInstituto
DefaultGroupName=Almacen Instituto
OutputDir=dist
OutputBaseFilename=AlmacenInstituto-Setup
; SetupIconFile=icono.ico ; (opcional, pon tu icono aquí)
; LicenseFile=licencia.txt ; (opcional, pon tu licencia aquí)

[Files]
Source: "dist\AlmacenInstituto.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{desktop}\Almacen Instituto"; Filename: "{app}\AlmacenInstituto.exe"
Name: "{group}\Almacen Instituto"; Filename: "{app}\AlmacenInstituto.exe"
