from flask import Flask, render_template, url_for, request, redirect, flash
import smtplib
from config import EMAIL, SENHA
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def chave():
    return os.urandom(24)

app = Flask(__name__)
app.secret_key = chave()

@app.route('/')
def pagina_inicial():
    return render_template('inicio.html')

@app.route('/sites')
def sites():
    return render_template('sites.html')

@app.route('/bots')
def bots():
  return render_template('bots.html')

@app.route('/manutencao')
def manutencao():
    return render_template('manutencao.html')

@app.route('/interfaces')
def interfaces():
    return render_template('interfaces.html')

@app.route('/internet')
def internet():
    return render_template('internet.html')

@app.route('/portifolio')
def portifolio():
    return render_template('meu_portifolio/portifolio.html')

# rota sem template, apenas para enviar os dados do form pro email.
@app.route('/enviar_formulario', methods=['POST'])
def enviar_formulario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('tel')
    servico = request.form.get('servico')
    mensagem = request.form.get('mensagem')

    # carregaar dados

    # email com os dados do cliente, para mim
    email_recebido = MIMEMultipart()
    email_recebido['Subject'] = servico
    email_recebido['From'] = EMAIL
    email_recebido['To'] = EMAIL
    email_recebido.attach(MIMEText(f'''Nome: {nome.title()}
Email: {email}
Contato: {telefone}\n
{mensagem}\n''', 'plain'))
    
    # email de confirmação para o cliente
    email_enviado = MIMEMultipart()
    email_enviado['To'] = EMAIL
    email_enviado['From'] = email
    email_enviado['Subject'] = '✅Confirmação de orçamento!✅'
    email_enviado.attach(MIMEText(f'''Olá {nome.title()}, tudo bem? Obrigado por nos escolher!😄\n
Gostariamos de informar a confirmação do seu orçamento😃! Fique atento na sua caixa de entrada e não deixe de verificar a caixa de spam, pois entraremos em contato. Lembramos que este orçamento é uma estimativa inicial e pode estar sujeito a ajustes após uma análise mais aprofundada das especificações do projeto. Estamos comprometidos em trabalhar em estreita colaboração com você para garantir que o projeto seja um sucesso✅\n
- 🌐Serviço: {servico.title()}\n
⚠️ATENÇÃO!!!⚠️
Nós não solicitamos códigos enviados por SMS ou Whatsapp, fique atento!🚨\n
Atenciosamente,
alencar.st''', 'plain'))

    # enviar mensagem por email
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(EMAIL, SENHA)
        
        # Envie o email
        servidor.sendmail(EMAIL, EMAIL, email_recebido.as_string()) # envia o email com o orçamento desejado, para mim.
        servidor.sendmail(EMAIL, email, email_enviado.as_string()) # envia um email de confirmação para o endereço de email preenchido no formulario
        flash('Orçamento enviado com sucesso!', "message")
    except Exception as e:
        print(f"Erro: {e}")
        flash('Não foi possível enviar seu orçamento', 'error')

    finally:
        servidor.quit()
    return redirect(url_for('pagina_inicial'))

if __name__ == '__main__':
    app.run(debug=True)
