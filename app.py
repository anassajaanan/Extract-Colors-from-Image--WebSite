from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from helpers import exact_color
import smtplib
import os

app = Flask(__name__)

app.config['UPLOAD_PATH'] = 'static/uploads'  
@app.route('/', methods=['GET', 'POST'])
def home():
    global color_palette
    dir = 'static/uploads'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if name and email and message:
            send_mail(name, email, message)


        pic = request.files['file']
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        color_palette = exact_color(f'static/uploads/{filename}', 900, 12, 1.5)
        return render_template('image-colors.html', img=filename, color_palette=color_palette)
    return render_template('Home.html')

@app.route('/download')
def download():
    return send_file(os.path.join(app.config['UPLOAD_PATH'], color_palette), as_attachment=True)

MY_EMAIL = os.environ.get('EMAIL')
MY_PASSWORD = os.environ.get('PASSWORD')


def send_mail(name, email, message):
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs="anasajaanan.official@gmail.com",
        msg=f"Subject:Contact from Extract Colors from Image\n\nName: {name}\nEmail: {email}\nMessage: {message}.".encode(
            'UTF-8')
    )


if __name__ == '__main__':
    app.run(debug=True)
