from playwright.sync_api import sync_playwright
import os
import time
import zipfile
import shutil

#convertion xlsx in json
import  jpype
import  asposecells

def download_mortes_violentas():
    url = "https://ssp.ba.gov.br/informacoes-criminais/estatistica/?ano=2024"
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto(url)

        # Rolar a página para garantir o carregamento do conteúdo
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 4)")
        time.sleep(2)

        # Esperar e iniciar o download
        with page.expect_download() as download_info:
            page.click("xpath=//*[@id='wp--skip-link--target']/div/div[2]/div/div[2]/div[1]/div[1]/h4[1]/a")
        
        download = download_info.value
        download_path = os.path.join(download_dir, "mortes_violentas.zip")
        download.save_as(download_path)
        print(f"Arquivo baixado para: {download_path}")

        # Extrair e organizar os arquivos
        extract_and_organize_files(download_path)

        browser.close()

def extract_and_organize_files(zip_path):
    # Diretórios de destino
    pdf_dir = os.path.join(os.getcwd(), "pdf")
    data_dir = os.path.join(os.getcwd(), "data")
    
    # Criar os diretórios se não existirem
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Extrair o conteúdo do arquivo zip em uma pasta temporária
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("temp_extracted")

    # Organizar arquivos extraídos
    for root, dirs, files in os.walk("temp_extracted"):
        for file in files:
            if file.endswith(".pdf"):
                shutil.move(os.path.join(root, file), os.path.join(pdf_dir, file))
            elif file.endswith(".csv"):
                shutil.move(os.path.join(root, file), os.path.join(data_dir, file))
            elif file.endswith(".xlsx"):
                shutil.move(os.path.join(root, file), os.path.join(data_dir, file))
    
    # Remover a pasta temporária após a organização
    shutil.rmtree("temp_extracted")
    print("Arquivos organizados com sucesso.")

def convert_xlsxInjson():
    jpype.startJVM()
    from asposecells.api import Workbook
    workbook = Workbook("data/01_MORTES_VIOLENTAS_ESTADO.xlsx")
    workbook.save("json/Output.json")
    jpype.shutdownJVM()

download_mortes_violentas()
convert_xlsxInjson()
