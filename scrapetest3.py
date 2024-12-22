from urllib.request import urlopen
from urllib.error import HTTPError
try:
    html = urlopen('http://www.pythonscraping.com/pages/page21.html')
except HTTPError as e:
    print(e)
# devolve null, executa um break ou algum outro "Plano B"
else:
    print("sem erro")
    # o programa continua. Nota: se você retornar ou executar um break no
    # catch da exceção, não será necessário usar a instrução "else"