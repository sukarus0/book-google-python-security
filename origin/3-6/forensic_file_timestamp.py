import os, time

file = "test.txt"

# 파일 생성일 출력
created = os.path.getctime(file)
created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created))
print("생성 시간: " + created_time)

# 파일 수정일 출력
modified = os.path.getmtime(file)
modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified))
print("수정 시간: " + modified_time)

# 파일 접근일 출력
accessed = os.path.getatime(file)
accessed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(accessed))
print("접근 시간: " + accessed_time)
 