class Wallet:
    def __init__(self, currency_code: str, ratio: float, value: float = 0.0):
        self.currency_code = currency_code
        self.ratio = ratio
        self.value = value


    def __add__(self, wallet2):
        return (self.value * self.ratio + wallet2.value * wallet2.ratio)/self.ratio

    def __str__(self):
        return f"{self.currency_code}, Kurs do PLN: {self.ratio}, Saldo: {self.value:.2f}\n"
    
    def __repr__(self):
        return f"{self.currency_code}, Kurs do PLN: {self.ratio}, Saldo: {self.value:.2f}\n"

    

