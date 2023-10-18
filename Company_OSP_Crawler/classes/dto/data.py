from dataclasses import dataclass
from datetime import datetime
from typing import Optional

#* DTO, Entity 같은 개념 -> 데이터를 저장해줄 객체
#* setter로 각 들어오는 값에 대해 유효성 검사 해줌
@dataclass
class Data:
    _cp_id: Optional[str] = None
    _platform: Optional[str] = None
    _osp: Optional[str] = None
    _company: Optional[str] = None
    _keyword: Optional[str] = None
    _contents: Optional[str] = None
    _title: Optional[str] = None
    _write_date: Optional[datetime] = None
    _writer: Optional[str] = None
    _url: Optional[str] = None
    _createdAt: Optional[datetime] = None

    @property
    def created_at(self):
        return self._createdAt

    @created_at.setter
    def created_at(self, created_at):
        self._createdAt = created_at
        # createdAt validation
        if not self._createdAt:
            raise ValueError("createdAt 없음!")
        if not isinstance(self._createdAt, datetime):
            raise TypeError("createdAt should be of type str")

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, movie):
        self._company = movie
        # movie validation
        if not self._company:
            raise ValueError("movie 없음!")
        if not isinstance(self._company, str):
            raise TypeError("movie should be of type str")

    @property
    def osp(self):
        return self._osp

    @osp.setter
    def osp(self, osp):
        self._osp = osp
        # contents validation
        if not self._osp:
            raise ValueError("osp 없음!")
        if not isinstance(self._osp, str):
            raise TypeError("osp should be of type str")

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform):
        self._platform = platform
        # platform validation
        if not self._platform:
            raise ValueError("platform 없음!")
        if not isinstance(self._platform, str):
            raise TypeError("platform should be of type str")

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword
        # keyword validation
        if not self._keyword:
            raise ValueError("keyword 없음!")
        if not isinstance(self._keyword, str):
            raise TypeError("keyword should be of type str")

    @property
    def cp_id(self):
        return self._cp_id

    @cp_id.setter
    def cp_id(self, cp_id):
        self._cp_id = cp_id
        # cp_id validation
        if not self._cp_id:
            raise ValueError("cp_id 없음!")
        if not isinstance(self._cp_id, str):
            raise TypeError("cp_id should be of type str")

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, contents):
        self._contents = contents

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        # title validation
        if not self._title:
            raise ValueError("title 없음!")
        if not isinstance(self._title, str):
            raise TypeError("title should be of type str")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        # url validation
        if not self._url:
            raise ValueError("url 없음!")
        if not isinstance(self._url, str):
            raise TypeError("url should be of type str")

    @property
    def write_date(self):
        return self._write_date

    @write_date.setter
    def write_date(self, write_date):
        self._write_date = write_date
        # write_date validation
        if not self._write_date:
            raise ValueError("write_date 없음!")

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, writer):
        self._writer = writer
        # writer validation
        if not self._writer:
            raise ValueError("writer 없음!")
        if not isinstance(self._writer, str):
            raise TypeError("writer should be of type str")

    def to_dict(self):
        return {
            'cp_id': self._cp_id,
            'company': self._company,
            'keyword': self._keyword,
            'platform': self._platform,
            'osp': self._osp,
            'url': self._url,
            'title': self._title,
            'writer': self._writer,
            'contents': self._contents,
            'write_date': self._write_date,
            'created_at': self._createdAt,
        }
