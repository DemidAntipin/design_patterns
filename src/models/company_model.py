import re

class Company_model():
    __name:str = ""
    __inn:str = ""
    __account:str = ""
    __correspondent_account:str = ""
    __bic:str = ""
    __ownership:str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value:str) -> str:
        if isinstance(value, str):
            if value.strip() != "":
                self.__name = value
            else:
                raise ValueError("Поле name не может быть пустым!")
        else:
            raise TypeError(f"Ожидается str, получено {value.__class__.__name__}")

    @property
    def inn(self) -> str:
        return self.__inn
    
    @inn.setter
    def inn(self, value:str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            correct_pattern = r'^\d{12}$'
            if re.match(correct_pattern, value):
                self.__inn=value
            else:
                raise ValueError("ИНН должен содержать 12 цифр")
        else:
            raise TypeError(f"Ожидается str или int, получено {value.__class__.__name__}")
    
    @property
    def account(self) -> str:
        return self.__account
    
    @account.setter
    def account(self, value:str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            correct_pattern = r'^\d{11}$'
            if re.match(correct_pattern, value):
                self.__account=value
            else:
                raise ValueError("Счёт должен содержать 11 цифр")
        else:
            raise TypeError(f"Ожидается str или int, получено {value.__class__.__name__}")

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value:str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            correct_pattern = r'^\d{11}$'
            if re.match(correct_pattern, value):
                self.__correspondent_account=value
            else:
                raise ValueError("Корреспондентский счёт должен содержать 11 цифр")
        else:
            raise TypeError(f"Ожидается str или int, получено {value.__class__.__name__}")
    
    @property
    def bic(self) -> str:
        return self.__bic
    
    @bic.setter
    def bic(self, value:str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            correct_pattern = r'^\d{9}$'
            if re.match(correct_pattern, value):
                self.__bic=value
            else:
                raise ValueError("БИК должен содержать 9 цифр")
        else:
            raise TypeError(f"Ожидается str или int, получено {value.__class__.__name__}")
    
    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value:str) -> str:
        if isinstance(value, str):
            correct_pattern = r'^\w{0,5}$'
            if re.match(correct_pattern, value):
                self.__ownership=value
            else:
                raise ValueError("Вид собственности должен содержать не более 5 символов")
        else:
            raise TypeError(f"Ожидается str, получено {value.__class__.__name__}")