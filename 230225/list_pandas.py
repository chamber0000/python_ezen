import pandas as pd
import os

# 함수 생성
# 매개변수 2개 path, end_string
def list_df(path, end_string):
    # file_list 생성
    file_list = os.listdir(path)
    
    # 확장자가 end_string과 같은 경우의 리스트만 추출
    # case1
    file_list2 =[]
    for i in file_list:
        if i.endswith(end_string):
            file_list2.append(i)
    # case2
    file_list3 = [i for i in file_list if i.endswith(end_string)]
    print(file_list2 == file_list3)

    # file_list2의 리스트 항목들을 데이터프레임화하여
    # 하나의 데이터프레임으로 결합

    # 비어있는 데이터프레임 생성
    total_df = pd.DataFrame()
    
    # file_list2의 항목들을 가지고 반복문 실행
    for i in file_list2:
        # path는 매개변수, i는 file_list2 항목의 값
        if end_string =='.csv':
            df = pd.read_csv(path + i)
        elif end_string == '.json':
            df = pd.read_json(path + i)
        elif (end_string == '.xlsx') | (end_string == '.xls'):
            df = pd.read_excel(path + i)
        else : 
            return "확장자가 잘못 입력되었습니다."

        # 불러온 데이터프레임을 total_df에 단순한 행 결합
        total_df = pd.concat([total_df, df], axis=0, ignore_index=True)
    
    # 합쳐진 데이터프레임을 리턴
    return total_df