import winreg

try:
    # 키를 정의 한다.
    hKey = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Office\\16.0\\Excel\\File MRU")

    # 키 안에 들어 있는 모든 키에 대해 루프를 돈다.
    for i in range(0, winreg.QueryInfoKey(hKey)[1]):
        name, value, type = winreg.EnumValue(hKey, i)

        # Item 으로 시작하는 이름일 때 프린트 한다.
        if name.startswith("Item"):
            print (name + ": " + value)

except FileNotFoundError:
    print("엑셀이 설치되지 않았습니다.")
