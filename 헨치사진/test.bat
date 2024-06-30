# 디렉터리 경로 설정
$directory = "C:\Users\Administrator\Documents\GitHub\Mizmaster-S9\헨치사진\테스트"  # 실제 디렉터리 경로로 변경해야 합니다

# 디렉터리 내의 모든 파일에 대해 이름 변경
Get-ChildItem -Path $directory | ForEach-Object {
    $newName = $_.Name -replace "데블", "데빌"
    Rename-Item -Path $_.FullName -NewName $newName -Force
    Write-Output "$($_.Name) -> $newName"
}
