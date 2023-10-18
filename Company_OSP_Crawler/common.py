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

    # 결과 출력
    sentiment = response['Sentiment'] if response['Sentiment'] != 'MIXED' else 'NEUTRAL'
    return sentiment


