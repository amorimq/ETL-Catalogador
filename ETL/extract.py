from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def iniciar_navegador():
    opcoes = webdriver.ChromeOptions()
    
    opcoes.add_argument('--headless=new')
    opcoes.add_argument('--window-size=1920,1080')
    opcoes.add_argument('--disable-gpu')
    opcoes.add_argument('--no-sandbox')
    opcoes.add_argument('--disable-dev-shm-usage') 
    opcoes.add_argument('--disable-extensions')    
    opcoes.page_load_strategy = 'eager'
    
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2
    }
    opcoes.add_experimental_option("prefs", prefs)
    
    print("Iniciando extração de dados...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
    driver.set_page_load_timeout(30)
    return driver

def extrair_catalogo_profundo(url_principal):
    driver = iniciar_navegador()
    dados_finais = []
    
    try:
        print(f"\n[INICIANDO VARREDURA COMPLETA] Acessando catálogo: {url_principal}")
        driver.get(url_principal)
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.calloutList a')))
        
        qtd_sistemas = len(driver.find_elements(By.CSS_SELECTOR, 'div.calloutList a'))
        print(f"-> Total de Sistemas identificados: {qtd_sistemas}\n")
        
        for i in range(qtd_sistemas):
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.calloutList a')))
            sistemas = driver.find_elements(By.CSS_SELECTOR, 'div.calloutList a')
            
            texto_sistema = sistemas[i].text.strip()
            print(f"\n[{i+1}/{qtd_sistemas}] Acessando Sistema: {texto_sistema}")
            
            driver.execute_script("arguments[0].click();", sistemas[i])
            time.sleep(1.0) 
            
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.calloutList a')))
            qtd_subsistemas = len(driver.find_elements(By.CSS_SELECTOR, 'div.calloutList a'))
            
            for j in range(qtd_subsistemas):
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.calloutList a')))
                subsistemas = driver.find_elements(By.CSS_SELECTOR, 'div.calloutList a')
                
                texto_sub = subsistemas[j].text.strip()
                print(f"  -> [{j+1}/{qtd_subsistemas}] Extraindo: {texto_sub}")
                
                driver.execute_script("arguments[0].click();", subsistemas[j])
                time.sleep(2) 
                
                try:
                    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.partresultsection')))
                    caixas_pecas = driver.find_elements(By.CSS_SELECTOR, '.partresultsection')
                    
                    pecas_nesta_pagina = 0
                    for caixa in caixas_pecas:
                        try:
                            descricao = caixa.find_element(By.CSS_SELECTOR, '.partDesc').text.strip()
                            codigo = caixa.find_element(By.CSS_SELECTOR, '.partNo').text.strip()
                            
                            if codigo:
                                dados_finais.append({
                                    'sistema': texto_sistema,
                                    'subsistema': texto_sub,
                                    'codigo_peca': codigo,
                                    'descricao': descricao
                                })
                                pecas_nesta_pagina += 1
                        except:
                            continue
                    
                    total_acumulado = len(dados_finais)
                    print(f"Registros nesta seção: {pecas_nesta_pagina}. Total extraído até o momento: {total_acumulado} peças.")
                    
                except:
                    print("Nenhuma registro rastreável encontrado nesta página.")
                    
                driver.execute_script("window.history.go(-1)")
                time.sleep(1.5)
                
            driver.execute_script("window.history.go(-1)")
            time.sleep(1.5)

    except Exception as e:
        print(f"\nErro Crítico durante a raspagem: {e}")
        
    finally:
        driver.quit()
                
        print(f"\n")
        print(f"Extração catálogo CH570")
        print(f"Total peças catalogadas: {len(dados_finais)} peças.")
        print(f"\n")
        
    return pd.DataFrame(dados_finais)