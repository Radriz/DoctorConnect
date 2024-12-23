import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values
config = dotenv_values() # {'LOGIN' : 123}


def send_email_conformation(user_email):
    # Generate a random confirmation code
    confirmation_code = random.randint(100000, 999999)

    # Send an email with the confirmation code
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "DrLink - Подтверждение почты"
    msg['From'] = "dr-link@mail.ru"
    msg['To'] = user_email

    # text = f"Привет! Для завершения регистрации введите следующий код подтверждения: {confirmation_code}"
    html = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 50px auto;
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    text-align: center;
                }
                .logo {
                    margin-bottom: 20px;
                }
                .logo img {
                    max-width: 300px; /* Уменьшенный размер логотипа */
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }
                h1 {
                    color: #4CAF50;
                    text-align: center;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 10px 0;
                }
                .code {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    text-align: center;
                    margin: 20px 0;
                    padding: 10px;
                    border: 1px dashed #4CAF50;
                    background: #f9fff9;
                    border-radius: 4px;
                }
                .footer {
                    text-align: center;
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Логотип -->
                <div class="logo">
                    <img src="https://drlink.ru/images/logo.png" alt="DrLink Logo">
                </div>
                <h1>DrLink - Подтверждение почты</h1>
                <p>Привет!</p>
                <p>Для завершения регистрации введите следующий код подтверждения:</p>
                <div class="code">"""+str(confirmation_code)+"""</div>
                <p>Если вы не запрашивали этот код, просто проигнорируйте это сообщение.</p>
                <div class="footer">Спасибо за использование DrLink!</div>
            </div>
        </body>
        </html>


    """

    body = MIMEText(html, 'html')
    msg.attach(body)

    s = smtplib.SMTP('smtp.mail.ru', 587)
    s.starttls()
    s.login(config["EMAIL_LOGIN"], config["EMAIL_PASSWORD"])
    s.send_message(msg)
    s.quit()

    print("Сообщение успешно отправлено")
    return confirmation_code


def forgot_password(user_email):
    # Generate a random confirmation code
    confirmation_code = random.randint(100000, 999999)

    # Send an email with the confirmation code
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "DrLink - Подтверждение почты"
    msg['From'] = "dr-link@mail.ru"
    msg['To'] = user_email

    # text = f"Привет! Для завершения регистрации введите следующий код подтверждения: {confirmation_code}"
    html = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 50px auto;
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    text-align: center;
                }
                .logo {
                    margin-bottom: 20px;
                }
                .logo img {
                    max-width: 300px; /* Уменьшенный размер логотипа */
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }
                h1 {
                    color: #4CAF50;
                    text-align: center;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 10px 0;
                }
                .code {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    text-align: center;
                    margin: 20px 0;
                    padding: 10px;
                    border: 1px dashed #4CAF50;
                    background: #f9fff9;
                    border-radius: 4px;
                }
                .footer {
                    text-align: center;
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Логотип -->
                <div class="logo">
                    <img src="https://drlink.ru/images/logo.png" alt="DrLink Logo">
                </div>
                <h1>DrLink - Восстановление пароля</h1>
                <p>Привет!</p>
                <p>Код подтверждения для восстановления пароля:</p>
                <div class="code">"""+str(confirmation_code)+"""</div>
                <p>Если вы не запрашивали этот код, просто проигнорируйте это сообщение.</p>
                <div class="footer">Спасибо за использование DrLink!</div>
            </div>
        </body>
        </html>


    """

    body = MIMEText(html, 'html')
    msg.attach(body)

    s = smtplib.SMTP('smtp.mail.ru', 587)
    s.starttls()
    s.login(config["EMAIL_LOGIN"], config["EMAIL_PASSWORD"])
    s.send_message(msg)
    s.quit()

    print("Сообщение успешно отправлено")
    return forgot_password


