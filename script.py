from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from os.path import exists
import json

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    website = 'https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/NCO/FrmNCOListado.cpe'
    path = '/snap/bin/chromium.chromedriver'
    driver = webdriver.Chrome(
        path,
        options=chrome_options)
    driver.get(website)
    driver.implicitly_wait(5.00)
    keyword = 'hosting'

    inputDescripcionCompra = driver.find_element(by=By.XPATH,
                                                 value='//input[@placeholder="Buscar Descripción del Objeto de compra"]')

    inputDescripcionCompra.send_keys(keyword)
    time.sleep(5.00)
    driver.implicitly_wait(1.00)

    botonOrdenarPorEstado = driver.find_element(
        by=By.XPATH, value="//th[text()='Estado de la Necesidad']")
    botonOrdenarPorEstado.click()
    botonOrdenarPorEstado.click()

    time.sleep(5.00)
    driver.implicitly_wait(1.00)

    contratacionesDisponibles = driver.find_elements(
        by=By.TAG_NAME, value='tr')

    tipoNecesidad = []
    nic = []
    fechaPublicacion = []
    descripcion = []
    estado = []
    fechaLimite = []
    entidadContratante = []
    direccionEntrega = []
    contacto = []

    datos = []

    for contratacion in contratacionesDisponibles:
        if (contratacion.text.find('En Curso') == -1):
            contratacionesDisponibles.remove(contratacion)
        else:
            nic.append(contratacion.find_element(
                by=By.XPATH, value='./td[2]').text)
            datos.append({
                'nic': contratacion.find_element(
                    by=By.XPATH, value='./td[2]').text,
                'texto': contratacion.text,
                'link': contratacion.find_element(
                    by=By.XPATH, value='./td[8]/a').get_attribute('href')
            }
            )
    driver.quit()

    nuevasContrataciones = []

    if len(datos) > 0:

        if (exists('./registro.csv')):
            df = pd.read_csv('./registro.csv', index_col=0)
            for item in datos:
                if not (item.get('nic') in df.values):
                    new_index = len(df.index)
                    df.loc[new_index] = [item.get('nic')]
                    nuevasContrataciones.append(item)
            df.to_csv('./registro.csv')
        else:
            df = pd.DataFrame({'NIC': nic})
            df.to_csv('./registro.csv')

            nuevasContrataciones = datos

        f = open('./datos.json', 'w')
        json.dump(nuevasContrataciones, f, indent=2, ensure_ascii=False)
        f.close()
        print(1)
    else:
        print(0)
except Exception as e:
    print(e)
    print(e.with_traceback)
