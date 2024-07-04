import random

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def fazer_login(driver, _usuario, _senha):  # Função para fazer login no site
    print('\nFazendo login...')
    print('Usuario: ', _usuario, 'Senha: ', _senha)
    driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[2]/button').click()   # Clica no obtão de login
    driver.implicitly_wait(2)
    driver.find_element(By.ID, 'cpf').send_keys(_usuario)
    driver.find_element(By.NAME, 'codigo').send_keys(_senha)
    driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[1]/button').click()   # Insere usuario e senha e clica no botão de Efetuar Login

    try:    # Verifica se o usuario e senha estão corretos
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/p/font/strong')))
        print('CPF ou CODIGO incorretos! Para efetuar o cadstro acesse: https://www.pesquisadestaque.com.br/sinop/cadastro.php \n')
        driver.get('https://www.pesquisadestaque.com.br/sinop/index.php')
        return {'status': False, 'msg': 'CPF ou CODIGO incorretos! Para efetuar o cadstro acesse o link', 'link': 'https://www.pesquisadestaque.com.br/sinop/cadastro.php'}

    except TimeoutException:    # Caso não apareça a mensagem de erro
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/form/button').click()
        print("Login efetuado com sucesso!\n")

        verify = verificar_votacao(driver)
        return verify


def verificar_votacao(driver): # Verifica se o questionario já foi respondido, se é a priemira vez ou se está em andamento
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/div[1]/strong')))
        texto = driver.find_element(By.XPATH,'//*[@id="login-block"]/div/div/div/div[3]/div[1]/strong').text

        if texto == 'Você já passou por todas as categorias, agradecemos a sua colaboração!':
            print('Você já passou por todas as categorias, agradecemos a sua colaboração!')
            return {'status': False, 'msg': 'Você já passou por todas as categorias, agradecemos a sua colaboração!'} # Já foi respondido

        elif 'respostas inválidas, se quiser voltar a' in texto or 'respostas inválidas, se quiser voltar a' in texto:    # parcialmente respondido
            driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/form[1]/button').click()
            print('Questionario em andamento não completo!')
            verify = votacao_incompleta(driver)
            return verify

        elif '1/186' in driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/p/font/strong').text :
            print(f"Primeira Votação!")
            verify = primeira_votacao(driver)
            return verify

    except TimeoutException:
        print('Erro timeout')


def primeira_votacao(driver):
    verifica_pagina = driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/p/font/strong')
    numero_ramo = verifica_pagina.text.split("-")[0].strip()
    print(f"Numero do ramo: {numero_ramo}")

    Ambos_numeros = numero_ramo.split("/")
    pagina_atual = int(Ambos_numeros[0])
    pagina_final = int(Ambos_numeros[1])
    print(f"Pagina atual: {pagina_atual}")
    print(f"Pagina final: {pagina_final}\n")

    while pagina_atual <= pagina_final:
        driver.implicitly_wait(3)
        try:
            verificar_ramo = driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/p/font/strong').text
            verificar_ramo = verificar_ramo.split("-")[1].strip()

            verifica_pagina = driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/p/font/strong')
            numero_ramo = verifica_pagina.text.split("-")[0].strip()
            print(f"Numero das paginas: {numero_ramo}")

            Ambos_numeros = numero_ramo.split("/")
            pagina_atual = int(Ambos_numeros[0])
            pagina_final = int(Ambos_numeros[1])

            if verificar_ramo == "Desenvolvimento De Software":
                print(f"RAMO : #{verificar_ramo}##############################################")
                votar_JMJ(driver)
            else:
                assert verificar_ramo != "Desenvolvimento De Software"
                print(f"RAMO : #{verificar_ramo}#")
                votar(driver)

        except IndexError:
            verify = driver.find_element(By.XPATH, '//*[@id="login-block"]/div/div/div/div[3]/div[1]/strong').text
            if verify == 'Você já passou por todas as categorias, agradecemos a sua colaboração!':
                print('Você já passou por todas as categorias, agradecemos a sua colaboração!')
                return {'status': True, 'msg': 'Você já passou por todas as categorias, agradecemos a sua colaboração!'}

def votacao_incompleta(driver):

    for redundancia in range(2):
        elemento_lista = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[1]/select')  # recebe os elementos de cada lista
        lista = Select(elemento_lista)  # Criar um objeto Select com base no elemento de lista suspensa
        tamanho_lista = int(len(lista.options))

        driver.implicitly_wait(3)

        for cont in range(1,tamanho_lista):
            elemento_lista = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[1]/select')  # recebe os elementos de cada lista
            lista = Select(elemento_lista)  # Criar um objeto Select com base no elemento de lista suspensa

            teste_lista = str(lista.options[cont].text)

            if teste_lista == "Desenvolvimento De Software" or teste_lista == "Desenvolvimento De Software (Não Respondeu)":
                lista.options[cont].click()
                driver.find_element(By.XPATH, '//*[@id="btnenviar"]').click()               #envia!
                print(f"Opcao de Ramo selecionada: {teste_lista}\n")
                driver.implicitly_wait(3)
                votar_JMJ(driver)
                driver.implicitly_wait(3)
                driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[3]/form[1]/button').click()  # Clica no botão de voltar

            elif '(Não Respondeu)' in teste_lista:
                lista.options[cont].click()
                driver.find_element(By.XPATH, '//*[@id="btnenviar"]').click()  # envia!
                print(f"Opcao de Ramo selecionada: {teste_lista}")
                driver.implicitly_wait(3)
                votar(driver)
                driver.implicitly_wait(3)
                driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[3]/form[1]/button').click()  # Clica no botão de voltar

            else:
                print(f'Opção já votada:  {teste_lista}')

    print('Votacao concluida com sucesso!')
    return {'status': True, 'msg': 'Votacao concluida com sucesso!'} # Votacao concluida



def votar_JMJ(driver):
    print('Votando em JMJ')
    elemento_lista = driver.find_element(By.XPATH, '//*[@id="empresa"]')  # recebe os elementos de cada lista
    lista = Select(elemento_lista)  # Criar um objeto Select com base no elemento de lista suspensa
    tamanho_lista = int(len(lista.options))
    print("#######################################################")

    for cont in range(tamanho_lista):
        teste_lista = str(lista.options[cont].text)
        if teste_lista == "EMPRESA ESCOLHIDA":
            lista.options[cont].click()
            driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[1]/button').click()  # envia!
            print(f"Opcao selecionada: {teste_lista}\n")
            break

        else:
            print("Opcao nao encontrada")
            debug = lista.options[cont].text
            print(f"Opcao: {debug}\n")


def votar(driver):
    print('Votando em Categoria')
    driver.implicitly_wait(3)
    elemento_lista = driver.find_element(By.XPATH, '//*[@id="empresa"]')  # recebe os elementos de cada lista
    lista = Select(elemento_lista)  # Criar um objeto Select com base no elemento de lista suspensa
    print(f"Quantidade de opcao: {len(lista.options)}")
    tamanho_lista = int(len(lista.options))
    select_random = int((random.randint(3, (tamanho_lista - 2))))
    lista.options[select_random].click()  # seleciona a opção aleatória
    print(f"Opcao selecionada: {select_random}\n")
    driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[3]/form[1]/button').click()  # envia!
    driver.implicitly_wait(3)
