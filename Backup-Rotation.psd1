function Backup-Rotation{
<#
.SYNOPSIS
  Rotates backups based on a desired number daily or monthly files retained.
.DESCRIPTION
  This script will remove a files in a folder that fall outside
  the desired timestamp range. Monthly files are those stamped on the
  first day of the month.
.NOTES
  Author:  Mike McDowell
.PARAMETER SourceFolders
  The folders to be included in file rotation. This can be an array.
.PARAMETER MonthlyBackups
  The number of months to retain files from the 1st.
.PARAMETER DailyBackups
  The number of days to retain files daily.
.EXAMPLE
  PS> Backup-Rotation -SourcesFolders C:\tftp\netbackups\,C:\tftp\weblogs\ -MonthlyBackups 12 -DailyBackups 30
#>
	[CmdletBinding()]
	param(
		[String[]] $SourceFolders,
		[Int] $MonthlyBackups,
		[Int] $DailyBackups
		)

foreach($sf in $SourceFolders){
    $files = Get-ChildItem $sf 
    Set-Location $sf
    foreach($item in $files){
        if($item.LastWriteTime.Day -eq 1 -and !$item.PSIsContainer -and 
        $item.LastWriteTime.Date -lt (Get-Date -Hour 0 -Minute 0 -Second 0).AddMonths(-$MonthlyBackups)){
            Remove-Item $item -Force
        }
        if($item.LastWriteTime.Day -ne 1 -and !$item.PSIsContainer -and
        $item.LastWriteTime.Date -lt (Get-Date -Hour 0 -Minute 0 -Second 0).AddDays(-$DailyBackups)){
            Remove-Item $item -Force
         }

    }
}
