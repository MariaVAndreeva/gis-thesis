@echo off
@setlocal
rem run this script as admin from a directory, where 'qgis-db.accdb' database file is located
rem sets up an ODBC data source for (Q)GIS project 'Lanzen'
set DS_NAME=thesis-2017 
odbcconf configsysdsn "Microsoft Access Driver (*.mdb, *.accdb)" "DSN=%DS_NAME%|Description=Lanzen MSAccess Data Source fuer GIS|DBQ=%CD%\qgis-db.accdb"
echo ODBC Datenquelle %DS_NAME% erfolgreich registriert!
@endlocal
@echo on