import pandas as pd
import numpy as np

# 1번 함수 생성 
def first(_df, _col, _time):
    # 결측치와 이상치를 제거 
    result = _df[~_df.isin([np.nan, np.inf, -np.inf]).any(1)]
    # 기준이 되는 컬럼을 제외한 나머지 컬럼을 삭제
    result = result.loc[:,[_col]]
    # 이동 평균선, 상단밴드, 하단밴드 생성
    result['center'] = result[_col].rolling(20).mean()
    result['ub'] = result['center'] + 2*result[_col].rolling(20).std()
    result['lb'] = result['center'] - 2*result[_col].rolling(20).std()

    # 시작시간부터 마지막 데이터까지 필터링
    result = result.loc[_time:]
    # 결과를 리턴
    return result

# 2번 함수
# 거래내역을 추가하는 함수
def second(_df):
    # trade 컬럼을 생성 -> 값은 ""
    result = _df
    result['trade'] = ''
    # 기준이 되는 컬럼의 이름은 가변
    # 위치는 변하지 않기 때문에
    # 기준이 되는 컬럼은 첫번째
    col = result.columns[0]
 
    # trade 내역 추가  
    for i in result.index:
        # 기준이 되는 컬럼이 상단 밴드보다 큰 경우
        if result.loc[i,col] > result.loc[i,'ub']:
            if result.shift(1).loc[i,'trade'] == 'buy':
                result.loc[i,'trade'] = ''
            else:
                result.loc[i,'trade'] = ''
        # 기준이 되는 컬럼이 하단 밴드보다 작은 경우
        elif result.loc[i,col] < result.loc[i,'lb']:
            if result.shift(1).loc[i,'trade'] == 'buy':
                result.loc[i,'trade'] = 'buy'
            else:
                result.loc[i,'trade'] = 'buy'       
        # 기준이 되는 컬럼이 하단 밴드와 상단밴드 사이에 존재하는 경우
        elif result.loc[i,col] >= result.loc[i,'lb'] and \
             result.loc[i,col] <= result.loc[i,'ub']:
                if result.shift(1).loc[i,'trade'] == 'buy':
                    result.loc[i,'trade'] = 'buy'
                else:
                    result.loc[i,'trade'] = ''
    return result               

# 3번 함수
def third(_df):
    result = _df
    # return 컬럼을 생성 -> 값 1
    result['return'] = 1
    # 기준이 되는 컬럼은 columns[0]
    col = result.columns[0]
    # 수익율, 구매가격, 판매가격 변수 생성
    rtn = 1.0
    buy = 1.0
    sell = 1.0

    # 수익률 계산하는 반복문
    for i in result.index:
        # 구매 가격을 확인
        if result.shift(1).loc[i,'trade'] == '' and\
            result.loc[i,'trade'] == 'buy':
            buy = result.loc[i,col]
            print('구매일자: ', i, '구매가격', buy)
        elif result.shift(1).loc[i,'trade'] == 'buy' and \
            result.loc[i,'trade'] == '':
            sell = result.loc[i, col]
            rtn = (sell - buy) / buy + 1
            result.loc[i, 'return'] = rtn
            print('판매일시:', i, "판매가격:", sell, '수익율: ', round(rtn, 4))

        # buy, sell 값을 초기화
        if result.loc[i, 'trade'] == '':
            buy = 0, 0
            sell = 0, 0
        
    # 누적 수익률 계산
    acc_rtn = 1.0

    for i in result.index:
        rtn = result.loc[i, 'return']
        acc_rtn *= rtn
        result['acc_rtn'] = acc_rtn

    print('누적수익률:', round(acc_rtn, 4))

    return result