from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"
    TRAINING_BY_ALL = "TA"
    TRAINING_BY_LOW_SAMPLE = "TL"
    TRAINING_BY_PREVIOUS_AND_MEAN = "TPM"
    TRAINING_BY_CURRENT = "TC"
    TRAINING_BY_PREVIOUS = "TP"
    TRAINING_BY_MISSING_DATA = "TM"


class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90
    LOW_SAMPLE = 10
    ENOUGH_SAMPLE = 5000


test_mode = Const.TRAINING_BY_ALL.value

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

if test_mode == Const.TRAINING_BY_LOW_SAMPLE:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.LOW_SAMPLE)
else:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.ENOUGH_SAMPLE)

ml_df = pd.DataFrame.from_records(random_set)

# 성공은 노랑, 실패는 빨강은 노랑으로 표시되도록 칼라로 치환한다.
ml_df.loc[ml_df[0] == "N", 0] = "red"
ml_df.loc[ml_df[0] == "Y", 0] = "yellow"

# 컬럼 이름을 달아준다.
ml_df.columns = ["result", "previous_score", "current_score", "mean"]
print(ml_df.head(3))

# 데이터 프레임을 라벨과 데이터로 나눈다.
data = ml_df.iloc[:, 1:]
label = ml_df.iloc[:, 0]

# 테이터 나누기
data_train, data_test, label_train, label_test = train_test_split(data, label)

data_test_original = data_test.copy()

# 테스트 1 (과거 성적, 평균으로만 학습 시키기)
if test_mode == Const.TRAINING_BY_PREVIOUS_AND_MEAN:
    data_test = data_test.iloc[:, [0, 2]]
    data_train = data_train.iloc[:, [0, 2]]
# 테스트 2 (현재 성적으로만 학습 시키기)
elif test_mode == Const.TRAINING_BY_CURRENT:
    data_test = data_test.iloc[:, [1]]
    data_train = data_train.iloc[:, [1]]
# 테스트 3 (과거 성적으로만 학습 시키기)
elif test_mode == Const.TRAINING_BY_PREVIOUS:
    data_test = data_test.iloc[:, [0]]
    data_train = data_train.iloc[:, [0]]

# 학습시켜 모델 만들기(Random Forest)
model = RandomForestClassifier()

if test_mode == Const.TRAINING_BY_MISSING_DATA:
    ml_missing_df = ml_df.query('previous_score < 90 and current_score < 90')
    print(ml_missing_df.head(3))

    data_missing = ml_missing_df.iloc[:, 1:]
    label_missing = ml_missing_df.iloc[:, 0]

    data_missing_train, data_missing_test, label_missing_train, \
    label_missing_test = train_test_split(data_missing, label_missing)

    model.fit(data_missing_train, label_missing_train)
else:
    model.fit(data_train, label_train)

# 학습 시킨 모델로 데이터 예측
predict = model.predict(data_test)
print("predict:" + str(predict))

# 결과에 대한 통계 값
accuracy_score = metrics.accuracy_score(label_test, predict)
classification_report = metrics.classification_report(label_test, predict)

print("Accuracy: ", accuracy_score)
print("Statistic: \n", classification_report)


axis1 = ml_df.plot.scatter(x="previous_score",
                      y="current_score",
                      c="result",
                      colormap="viridis")
axis1.set_title("Rule based")

axis2 = data_test_original.plot.scatter(x="previous_score",
                                      y="current_score",
                                      c=predict,
                                      colormap="viridis")
axis2.set_title("Random Forest")

plt.show()
