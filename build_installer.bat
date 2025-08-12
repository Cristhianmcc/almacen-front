@echo off
chcp 65001 >nul
echo ========================================
echo  CONSTRUCTOR DE INSTALADOR PROFESIONAL
echo  Sistema de Almacén - Instituto v2.0
echo ========================================
echo.

echo [1/5] Limpiando carpetas anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "Output" rmdir /s /q "Output"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo ✅ Limpieza completada
echo.

echo [2/5] Verificando dependencias...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller no está instalado
    echo Instalando PyInstaller...
    pip install PyInstaller
    if errorlevel 1 (
        echo ❌ Error al instalar PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller verificado
echo.

echo [3/5] Compilando aplicación con PyInstaller...
echo Usando archivo de especificación: AlmacenInstituto.spec
pyinstaller --clean AlmacenInstituto.spec
if errorlevel 1 (
    echo ❌ Error en la compilación con PyInstaller
    pause
    exit /b 1
)
echo ✅ Compilación completada
echo.

echo [4/5] Verificando archivos compilados...
if not exist "dist\AlmacenInstituto\AlmacenInstituto.exe" (
    echo ❌ No se encontró el ejecutable compilado
    pause
    exit /b 1
)
echo ✅ Ejecutable encontrado: dist\AlmacenInstituto\AlmacenInstituto.exe
echo.

echo [5/5] Generando instalador con Inno Setup...
echo.
echo ⚠️  IMPORTANTE: Asegúrate de tener Inno Setup instalado
echo    Descarga desde: https://jrsoftware.org/isdl.php
echo.
echo Presiona cualquier tecla cuando Inno Setup esté listo...
pause >nul

if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Compilando instalador con Inno Setup 6...
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" instalador.iss
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    echo Compilando instalador con Inno Setup 6...
    "C:\Program Files\Inno Setup 6\ISCC.exe" instalador.iss
) else (
    echo ❌ Inno Setup no encontrado
    echo Por favor, instala Inno Setup y ejecuta manualmente:
    echo   iscc instalador.iss
    echo.
    echo O abre el archivo instalador.iss en Inno Setup Compiler
)

echo.
echo ========================================
echo  PROCESO COMPLETADO
echo ========================================
echo.
echo 📁 Archivos generados:
echo    - dist\AlmacenInstituto\ (Aplicación compilada)
echo    - Output\AlmacenInstituto-Setup-v2.0.exe (Instalador)
echo.
echo 🚀 Para distribuir, envía el archivo .exe del Output
echo.
pause
