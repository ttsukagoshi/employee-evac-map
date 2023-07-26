# Fakerを使って架空の300名分の従業員リストを作成する
# リストの項目はID、NAME、ADDRESSとして、それに加えてBLOCK（町名）とする
# Fakerのlocaleは日本語版とし、できたリストをCSVファイルとしてdata/mock_employee_list.csvに保存する

import pandas as pd
from faker import Faker
import random


def get_town_list():
    """
    秋田市の町名リストをdata/akita-2022-ichijoho.csvから取得する
    """
    # CSVファイルを読み込む
    df = pd.read_csv("data/akita-2022-ichijoho.csv", encoding="utf-8")

    # 町名の列を取得
    town_list = df["大字町丁目名"].values.tolist()

    return town_list


def create_employee_list():
    fake = Faker("ja_JP")
    town_list = get_town_list()

    # リストの初期化
    employee_list = []

    # リストに項目を追加
    for _ in range(300):
        employee_list.append(
            [
                fake.unique.random_number(digits=8),
                fake.name(),
                random.choice(town_list),
            ]
        )

    # リストをデータフレームに変換
    df = pd.DataFrame(employee_list, columns=["ID", "NAME", "BLOCK"])

    # BLOCK列の値に基づいて、ADDRESS列を追加。それぞれランダムに番地を追加する（山王一丁目→秋田市山王一丁目1-1）
    df["ADDRESS"] = df["BLOCK"].apply(
        lambda x: "秋田市"
        + x
        + str(fake.random_number(digits=2))
        + "-"
        + str(fake.random_number(digits=2))
    )

    # BLOCK列とADDRESS列の順序を入れ替える
    df = df[["ID", "NAME", "ADDRESS", "BLOCK"]]

    # データフレームをCSVファイルとして保存
    df.to_csv("data/mock_employee_list.csv", index=False)


if __name__ == "__main__":
    create_employee_list()
