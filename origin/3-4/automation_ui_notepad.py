from pywinauto.application import Application
import subprocess
import time
import os

# 메모장를 띄운다.
app = Application().start("notepad.exe")
 
# 메모장에 파이썬 스크립트를 입력한다.
app.UntitledNotepad.Edit.type_keys("print {(}'ui automation sample'{)}", with_spaces = True)
 
# 파일을 c:\python\security 폴더에 UTF-8 포맷으로 저장한다.
app.UntitledNotepad.menu_select("파일(&F)->저장(&S)")
app.다른_이름으로_저장.Edit1.set_edit_text("c:\python\security\samplecode.py")
app.다른_이름으로_저장.ComboBox2.select("모든 파일")
app.다른_이름으로_저장.ComboBox3.select("UTF-8")

time.sleep(1.0)
app.다른_이름으로_저장.Button1.click()
app.UntitledNotepad.menu_select("파일(&F)->끝내기(X)")

# 파일을 실행 하고 실행 결과를 받아 프린트 한다.
cmd = subprocess.run(["python", "samplecode.py"], capture_output=True)
stdout = cmd.stdout.decode()
print(stdout)

# 메모장으로 작성했던 파일을 지운다.
os.remove("samplecode.py")