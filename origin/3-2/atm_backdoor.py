def do_withdraw(request_money):
    print("인출: " + str(request_money))


def click_withdraw(request_money):
    if isinstance(request_money, str):
        if request_money == "show me the money":
            do_withdraw(1000000000)
            return

    if isinstance(request_money, int):
        if request_money >=1 and request_money <=10000:
            do_withdraw(request_money)
        else:
            print("잔고 부족")
    else:
        print("정상적인 금액을 넣어주세요")


click_withdraw("show me the money")