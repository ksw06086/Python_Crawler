from requests import get
from boto3 import Session
from os import getenv
from dotenv import load_dotenv


def get_api_request_result(api_url, header):
    api_data = get(api_url, headers=header).json()
    return api_data


def get_sentiment_by_aws(text):
    load_dotenv()
    session = Session(
        aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='ap-northeast-2'
    )
    comprehend_client = session.client('comprehend')

    # 감정 분석 요청
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='ko'  # 텍스트의 언어 코드 (예: en, ko)
    )

    #* Neutral (중립): 텍스트에 특별한 감정 표현이 없거나 감정이 중립적인 경우입니다. 예를 들어 "이것은 책입니다."와 같은 문장은 감정이 포함되지 않았기 때문에 중립으로 분류됩니다.
    #* Positive (긍정): 텍스트가 긍정적인 감정이나 반응을 표현하는 경우입니다. 예를 들어 "이 제품은 정말 훌륭해요!"와 같은 문장은 긍정적인 감정을 표현하므로 긍정으로 분류됩니다.
    #* Negative (부정): 텍스트가 부정적인 감정이나 반응을 표현하는 경우입니다. 예를 들어 "이 서비스는 매우 불만족스럽습니다."와 같은 문장은 부정적인 감정을 표현하므로 부정으로 분류됩니다.
    #* Mixed (혼합): 텍스트가 여러 감정을 동시에 포함하고 있어, 단순히 긍정 또는 부정으로만 분류하기 어려운 경우입니다. 예를 들어 "이 제품의 디자인은 훌륭한데 가격이 너무 비싸요."와 같은 문장은 긍정적인 감정과 부정적인 감정이 동시에 포함되어 있으므로 혼합으로 분류될 수 있습니다.
    # 결과 출력
    sentiment = response['Sentiment'] if response['Sentiment'] != 'MIXED' else 'NEUTRAL'
    return sentiment


