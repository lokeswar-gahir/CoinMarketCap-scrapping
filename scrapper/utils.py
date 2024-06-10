from django.conf import settings
# def get_allowed_coins(file: str=settings.BASE_DIR+'scrapper\\resources\\crypto_symbols.txt'):
def get_allowed_coins(file: str=settings.BASE_DIR/'scrapper' / 'resources' / 'crypto_symbols.txt'):
    with open(file) as f:
        data = f.read()
    data = data.split('\n')
    data.pop()
    return data
# print(settings.BASE_DIR)