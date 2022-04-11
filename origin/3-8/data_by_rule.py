from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
import matplotlib.pyplot as plt


class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"


class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90


# 룰을 이용해서 결과를 판단한다
# (현재 성적이 70 점 이상 and 전 시험과의 평균이 50 점 이상) or 현재 90점 이상
def check_exam_list(score_list):
    rule = {"or":
                [{"and":
                      [{">=": [{"var": "current_score"},
                               LearningConfig.RULE_CURRENT_SCORE]},
                       {">=": [{"var": "mean"},
                               LearningConfig.RULE_MEAN]}]},
                 {">=": [{"var": "current_score"},
                         LearningConfig.RULE_FREE_PASS_SCORE]}]
            }

    exam_dict = {}
    exam_dict["current_score"] = score_list[1]
    exam_dict["mean"] = score_list[2]

    rule_result = jsonLogic(rule, exam_dict)

    if rule_result:
        return Const.PASS.value
    else:
        return Const.FAIL.value


# 랜덤 데이터 만들어 줌.
def make_random_numbers(previous_min, previous_max, current_min,
                        current_max, sample_number):
    my_set = set()

    # 겹치는 데이터가 없게 하기 위해서 set을 사용하여 중복 생성 데이터 제거
    while 1:
        previous_score = random.randint(previous_min, previous_max)
        current_score = random.randint(current_min, current_max)
        score_mean = mean([previous_score, current_score])
        my_set.add(tuple([previous_score, current_score, score_mean]))
        if len(my_set) == sample_number:
            break

    random_list = [list(x) for x in my_set]

    # 룰 엔진 정답 맨 앞에 추가
    for index, item in enumerate(random_list):
        result = check_exam_list(item)
        item.insert(0, result)

    return random_list


random_set = make_random_numbers(0, 100, 0, 100, 5000)
sample_dataframe = pd.DataFrame.from_records(random_set)

# 성공은 노랑, 실패는 빨강은 노랑으로 표시되도록 칼라로 치환한다.
sample_dataframe.loc[sample_dataframe[0] == "N", 0] = "red"
sample_dataframe.loc[sample_dataframe[0] == "Y", 0] = "yellow"

# 컬럼 이름을 달아준다.
sample_dataframe.columns = ["result", "previous_score",
                            "current_score", "mean"]
print(sample_dataframe.head(3))

# 과거, 현재 성적을 축으로 하고, 성공 여부를 색으로 표시하는 그래프를 그려준다.
ax1 = sample_dataframe.plot.scatter(x="previous_score",
                      y="current_score",
                      c="result",
                      colormap="viridis")
ax1.set_title("Rule based")
plt.show()
