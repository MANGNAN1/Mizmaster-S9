; CSV 파일 경로 설정 (스크립트와 같은 디렉토리)
csvFile := A_ScriptDir . "\henchies.csv"

; 헨치 데이터를 저장할 배열
henchies := []

; CSV 파일 읽기
FileRead, csvData, %csvFile%
Loop, Parse, csvData, `n, `r
{
    if (A_Index = 1)
        continue ; 헤더 행 건너뛰기

    fields := StrSplit(A_LoopField, ",")
    hench := {name: fields[1], kr_name: fields[2], au_name: fields[3], habitat: fields[4], aggro_status: fields[5], drop_status: fields[6], level: fields[7], attack_type: fields[8], attribute: fields[9], img: fields[10]}
    henchies.Push(hench)
}

; GUI 만들기
Gui, Font, s12 cBlack, Arial ; 폰트 사이즈 조절 및 색상 설정
Gui, Color, White ; 배경색 설정
Gui, Add, Text, x20 y20 w200 h30, 헨치 도감
Gui, Add, Text, x20 y70 w150 h20, 헨치 이름을 입력하세요:
Gui, Add, Edit, x180 y70 w200 h20 vHenchName gEnterPressed, ; Edit 컨트롤에서 엔터 키 입력을 감지하도록 설정
Gui, Add, Button, x400 y70 w60 h20 gSearchHench, 검색

; 텍스트 박스 스타일
Gui, Add, Text, x20 y120 w300 h300 +BackgroundTrans cBlack vHenchInfo, ; 텍스트 정보용 컨트롤

; 이미지 박스 스타일
Gui, Add, Picture, x340 y120 w200 h200 BackgroundTrans vHenchPic, ; 이미지 표시용 컨트롤

; GUI 크기 설정
Gui, Show, w600 h500, 헨치 도감
Return

SearchHench:
Gui, Submit, NoHide
henchName := HenchName
found := False

; 헨치 검색 및 정보 표시
for index, hench in henchies
{
    if (hench.name = henchName)
    {
        GuiControl,, HenchInfo, % "한국 이름: " hench.kr_name "`n호주 이름: " hench.au_name "`n서식지: " hench.habitat "`n선공 여부: " hench.aggro_status "`n득 여부: " hench.drop_status "`n레벨: " hench.level "`n공격 타입: " hench.attack_type "`n속성: " hench.attribute
        GuiControl,, HenchPic, % hench.img
        found := True
        break
    }
}

if (!found)
{
    GuiControl,, HenchInfo, 헨치를 찾을 수 없습니다.
}

Return

EnterPressed:
Gui, Submit, NoHide
Gosub, SearchHench
Return

GuiClose:
ExitApp

PgDn::
ExitApp
