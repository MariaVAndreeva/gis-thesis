Option Compare Database

'The target folder where to extract the attachements to, it is configured in QGIS_CONIG table
Public Property Get gAttachmentsDir() As String
On Error GoTo Err_Handler
    Dim db As DAO.Database
    Dim rs As DAO.Recordset
    Set db = CurrentDb
    Set rs = db.OpenRecordset("SELECT * FROM QGIS_CONFIG WHERE KEY = 'ATTACHMENTS_DIR'")
    rs.MoveFirst
    gAttachmentsDir = rs("VALUE")
    
Exit_Handler:
    'Clean up
    rs.Close
    db.Close
    Set rs = Nothing
    Set db = Nothing
    Exit Function
    
Err_Handler:
    MsgBox "Error " & Err.Number & ": " & Err.Description
    Resume Exit_Handler
End Property

'creates a directory fro the given path recursively
Private Function CreateFolderRecursive(fullPath As String)
  Dim arr, child, path As String
  'some gurading at the beginning
  If Len(dir(fullPath, vbDirectory + vbHidden)) <> 0 Then Exit Function
  arr = Split(fullPath, "\")
  path = ""
  For Each child In arr
    If path <> "" Then path = path & "\"
    path = path & child
    If Len(dir(path, vbDirectory + vbHidden)) = 0 Then MkDir path
  Next
End Function

Public Function ExtractAttachments(targetDir As String) As Long
On Error GoTo Err_Handler
Dim db As DAO.Database
Dim rs As DAO.Recordset
Dim attachmentsRs As DAO.Recordset2
Dim attachments, parentId As DAO.Field2
Dim absolutePath As String

'Show the hour glass
DoCmd.Hourglass True
'Get the database, recordset, and attachment field
Set db = CurrentDb
Set rs = db.OpenRecordset("T_Fund_Abbildung")
Set attachments = rs("Fund_Abbildung")
Set parentId = rs("ID_Fund_Abbildung")
'first create the root directory for extractions
CreateFolderRecursive targetDir
rs.MoveLast 'Needed to get the accurate number of records
'Show the progress bar
SysCmd acSysCmdInitMeter, "Extrahiere Bilder für QGIS...", rs.RecordCount
rs.MoveFirst 'jump back to the 1st record
'Navigate through the table
Do Until rs.EOF
       'Get the recordset for the Attachments field
       Set attachmentsRs = attachments.Value
    
       'Save all attachments in the field
       Do Until attachmentsRs.EOF
               'the absolute path is constructed from the configured target directory, unique ID of the parent record and the file name
               absolutePath = targetDir & "\" & parentId.Value & "-" & attachmentsRs("FileName")
               'Make sure the file does not exist and save
               If dir(absolutePath) = "" Then
                   attachmentsRs("FileData").SaveToFile absolutePath
               End If
               'Increment the number of files saved
               ExtractAttachments = ExtractAttachments + 1
               'Next attachment
               attachmentsRs.MoveNext
               'Update the progress bar
               SysCmd acSysCmdUpdateMeter, ExtractAttachments
        Loop
    attachmentsRs.Close
    'Next record
    rs.MoveNext
Loop

Exit_Handler:
    'Clean up
    rs.Close
    db.Close
    Set attachments = Nothing
    Set attachmentsRs = Nothing
    Set rs = Nothing
    Set db = Nothing
    'Remove the progress bar
    SysCmd acSysCmdRemoveMeter
    'Show the normal cursor again
    DoCmd.Hourglass False
    Exit Function

Err_Handler:
    MsgBox "Error " & Err.Number & ": " & Err.Description
    Resume Exit_Handler
 
End Function

Sub test()
    ExtractAttachments gAttachmentsDir
End Sub
