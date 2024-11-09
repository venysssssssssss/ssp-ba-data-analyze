import requests

# URL do endpoint
url = "https://ssp.ba.gov.br/v1/api/boletim/uploads/estatistica/estatistica-Estado-03-04-2024-1712169098.zip"

# Realizando a requisição GET
response = requests.get(url)

# Verificando o status da resposta
if response.status_code == 200:
    # Exibindo o conteúdo da resposta
    print(response.text)
else:
    print(f"Erro ao acessar o endpoint: {response.status_code}")
