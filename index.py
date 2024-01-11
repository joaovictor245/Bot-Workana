import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import schedule
import time

load_dotenv()

def enviar_email(destinatario, assunto, mensagem):
    remetente = os.getenv('REMETENTE_EMAIL')
    senha = os.getenv('SENHA_EMAIL')

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remetente, senha)
    server.send_message(msg)
    server.quit()

def verificar_vagas():
    url = 'https://www.workana.com/jobs?ref=home_menu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vagas = soup.find_all('div', class_='project-item')

    for vaga in vagas:
        titulo = vaga.find('h2').text.strip()
        link = vaga.find('a')['href']
        if 'Fazer um Site' in titulo.lower():
            destinatario = os.getenv('DESTINATARIO_EMAIL')
            enviar_email(destinatario, 'Nova Vaga de Emprego', f'Uma nova vaga de emprego foi encontrada no Workana!\n\nTítulo: {titulo}\nLink: {link}')
            print(f'E-mail enviado para {destinatario}')

if __name__ == "__main__":
    print("Bot Workana ligado!")
    
    
    schedule.every().hour.do(verificar_vagas)

    
    while True:
        schedule.run_pending()
        time.sleep(1)
