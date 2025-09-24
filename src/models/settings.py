from src.models.company_model import Company_model

class Settings():
    __company:Company_model = None

    @property
    def company(self) -> Company_model:
        return self.__company

    @company.setter
    def company(self, company_instance: Company_model):
        if isinstance(company_instance, Company_model):
            self.__company = company_instance
        else:
            raise ValueError(f"Ожидается объект company_model, получен {company_instance.__class__.__name__}")
        
    def __init__(self):
        self.default()

    def default(self):
        self.company = Company_model()