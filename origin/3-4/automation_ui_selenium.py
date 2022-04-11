from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from dataclasses import dataclass, field, asdict
from typing import List
from urllib.parse import urljoin


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
        {"pyodbc.programmingerror"}
    return judgment_strings


# 공격에 사용할 문자열들을 가져온다.
def get_injection_strings():
    injection_strings = InjectionString()
    injection_strings.strings += \
        {"'", "tom", "tom'"}
    return injection_strings


# 페이지 중 <form>~</form> 태그 사이의 값을 가져온다.
# 현재 소스에서는 form 이 1개만 있다고 가정한다.
def get_form_area(url):
    # 브라우저를 띄우고 최대 3초동안 기다리면서 form 태그를 찾는다.
    browser.get(url)
    try:
        element = WebDriverWait(browser, 3).until(
            ec.presence_of_element_located((By.TAG_NAME, "form"))
        )
    except TimeoutException:
        print("not found")
        return ""

    return element


# 폼 내부에서 input 필드를 모두 가져온다.
def get_form_info(form_area):
    form_field = FormField()

    form_field.action = form_area.get_attribute("action").lower()
    form_field.method = form_area.get_attribute("method").lower()

    input_tags = form_area.find_elements_by_tag_name("input")

    for input_tag in input_tags:
        if input_tag.get_attribute("type").lower() != "text":
            continue

        input_field = InputField()
        input_field.type = input_tag.get_attribute("type")
        input_field.name = input_tag.get_attribute("name")
        input_field.value = input_tag.get_attribute("value")
        form_field.input_fields.append(input_field)

    return form_field


# 공격 인자를 넣어 호출한 페이지의 응답 값 안에 판단에 필요한 문자열이 있는지 체크한다.
def check_vulnerability(response, url, injection_string):
    judgment_strings = get_judgment_strings()

    for judgment_string in judgment_strings.strings:
        if judgment_string in response.lower():
            print("인젝션 발견: ", url, "\n테스트 데이터: ", str(injection_string),
                  "\n검출 문구: ", judgment_string, "\n", "-"*10)


# 페이지에 공격용 인자를 실어 전송 후 결과를 받는다.
def send_injection(url, form_info, injection_string):
    # 브라우저에서 url 을 로딩 한다.
    browser.get(url)

    # 텍스트 입력 박스들에 인젝션 문구를 넣은 후 전송 버튼을 누른다.
    for input_field in form_info.input_fields:
        input_element = browser.find_element_by_name(input_field.name)
        input_element.send_keys(injection_string)

    form_element = browser.find_element_by_tag_name("form")
    form_element.submit()

    # 최대 3초 동안 기다리면서 errermsg 라는 class 이름을 찾는다.
    try:
        element = WebDriverWait(browser, 3).until(
            ec.presence_of_element_located((By.CLASS_NAME, "errormsg"))
        )
    except TimeoutException:
        return ""
    return element.text


def page_scan(start_url):
    form_area = get_form_area(start_url)
    form_info = get_form_info(form_area)
    injection_strings = get_injection_strings()

    for injection_string in injection_strings.strings:
        url = urljoin(start_url, form_info.action)
        response = send_injection(url, form_info, injection_string)
        check_vulnerability(response, url, injection_string)


if __name__ == "__main__":
    # 크롬 웹 드라이버를 생성 한다.
    browser = webdriver.Chrome()

    page_url = "http://127.0.0.1:5000/item_search"
    page_scan(page_url)
