from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from starlette.responses import RedirectResponse
from webdriver_manager.chrome import ChromeDriverManager

from operacao_site import fazer_login

app = FastAPI()

@app.post("/Votacao")
async def votar(CPF, SENHA):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.pesquisadestaque.com.br/sinop/index.php')

    driver.implicitly_wait(5)
    verify = fazer_login(driver, CPF, SENHA)
    return verify


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')