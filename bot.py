import requests
from bs4 import BeautifulSoup
import telebot
import io
import json
import mysql.connector


dir_credenciais = 'credenciais.json'
with open(dir_credenciais, 'r') as arquivo:
    credenciais = json.load(arquivo)

token = credenciais['token']
bot = telebot.TeleBot(str(token))

id_arthur = credenciais['id_arthur']
id_nuvem = -1001632970767 #backup de videoaulas e outros

global banco
global c

def db():
    try:
        banco = mysql.connector.connect(
            host = credenciais['database']['host'],
            user = credenciais['database']['user'],
            password = credenciais['database']['password'],
            database = credenciais['database']['database']
        )
        return banco
    except Exception as e:
        print('Oooops, mysql error:', e)

banco = db()
c = banco.cursor()



bot = telebot.TeleBot(token)
id_nuvem = -1001632970767

url = 'https://aimore.net/placas/placa_S-1.html'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
}



def next_page(soup):
    next_page_img = soup.find('img', alt='Next')
    if next_page_img:
        next_page = next_page_img.parent['href']
        return next_page
    else:
        return None

while True:
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    try:
        img_url = f"https:{soup.find('img', class_ = 'aimore')['src']}"
        print(img_url)

        img_desc = soup.find('span', class_ = 'cc').text
    

        if img_desc == 'Rua de uso local':
            break

        img_significado = img_desc.split(' — ')[1]
        print(img_significado)

        codigo_placa = img_desc.split(' — ')[0]
        print(codigo_placa)

        try:
            msg_id = bot.send_photo(id_nuvem, requests.get(img_url, headers=headers).content, caption=f"Código da placa: \n   -> <b> <code> {codigo_placa} </code> </b>", parse_mode='HTML').message_id
        except Exception as e:
            print('Oooops, image url error:', e)
            new_img_url = f'https://aimore.net/placas/{codigo_placa}.jpg'
            msg_id = bot.send_photo(id_nuvem, requests.get(new_img_url, headers=headers).content, caption=f"Código da placa: \n   -> <b> <code> {codigo_placa} </code> </b>", parse_mode='HTML').message_id

        c.execute(f"INSERT INTO imagens (atalho, descricao, msg_id) VALUES ('{codigo_placa}', '{img_significado}', '{msg_id}')")
        banco.commit()

    except Exception as e:
        print('Oooops, acho que não é esse hein:', e)
        


    url = f"https:{next_page(soup)}"

bot.infinity_polling()