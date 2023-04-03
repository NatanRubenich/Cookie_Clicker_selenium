from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Iniciar o navegador
driver = webdriver.Chrome()

# Abrir o jogo
driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[12]/div/div[1]/div[1]/div[10]").click()
time.sleep(2)

# Esperar carregar a página
wait = WebDriverWait(driver, 10)
cookie = wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
time.sleep(2)

# Loop para clicar no cookie continuamente
while True:
    cookie.click()

    # Encontrar o número de cookies que já foram ganhos
    cookies = driver.find_element(By.ID, "cookies")
    cookies = cookies.text.split(" ")[0]
    cookies = cookies.replace(",", "")

    # Encontrar o preço do próximo item
    upgrade = driver.find_elements(By.CSS_SELECTOR, "#store .product.unlocked")
    if upgrade:
        upgrade_prices = []
        for u in upgrade:
            price = u.find_element(By.CLASS_NAME, "price").text
            if price != "":
                upgrade_prices.append(int(price.replace(",", "")))
        upgrade_price = min(upgrade_prices)

        # Encontrar o próximo item a ser comprado
        upgrade = driver.find_elements(By.CSS_SELECTOR, "#store .product.unlocked")
        for u in upgrade:
            price = u.find_element(By.CLASS_NAME, "price").text
            if price != "":
                if int(price.replace(",", "")) == upgrade_price:
                    buy_id = u.get_attribute("id")
                    buy = driver.find_element(By.ID, buy_id)
                    buy.click()
                    print(f"Comprado {u.find_element(By.CLASS_NAME, 'title').text} por {price}.")
                    break
    else:
        print("Todos os itens de upgrade estão bloqueados.")

    # Esperar um pouco antes de clicar novamente
    time.sleep(0.1)

    # Atualizar o elemento do cookie
    cookie = driver.find_element(By.ID, "bigCookie")

# Fechar o navegador
driver.quit()