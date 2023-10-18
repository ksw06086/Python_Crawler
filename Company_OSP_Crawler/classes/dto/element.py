class Element:
    def __init__(self, how, what, many=False):
        self.how = how
        self.what = what
        self.many = many

        if not self.how:
            raise ValueError("how 없음!")
        elif self.how != 'xpath' and self.how != 'selector':
            raise ValueError('xpath나 selector 중에 골라주세요')
        if not isinstance(self.how, str):
            raise TypeError("how should be of type str")
        if not self.what:
            raise ValueError("what 없음!")
        if not isinstance(self.what, list):
            raise TypeError("what should be of type list")
        for w in self.what:
            if not isinstance(w, list):
                raise TypeError("what inner element should be of type list")
            select, attr = w
            if not select or not attr:
                raise TypeError("[select, attr] 형태로 존재해야 합니다.")
