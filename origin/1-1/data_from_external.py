data_from_external = ["union all blah blah --", 1, 11]


def check_safe_number(data):
    if isinstance(data, int):
        if 0 < data <= 10:
            print("안전한 변수")
        else:
            print("숫자 범위가 벗어났음")
    else:
        print("숫자가 아님")


for data in data_from_external:
    check_safe_number(data)
