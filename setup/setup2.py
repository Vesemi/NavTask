import os
import sys


def create_nginx_and_gunicorn_files(domena, projekt):

    # Wczytanie plików nginx oraz gunicorn
    plik_nginxa = ''
    plik_nginxa_template = open('/var/www/' + projekt + '/setup/nginx_file').readlines()

    plik_gunicorn = ''
    plik_gunicorn_template = open('/var/www/' + projekt + '/setup/gunicorn_file').readlines()

    for l in plik_nginxa_template:
        l = l.replace('NAZWA_STRONY', domena)
        l = l.replace('NAZWA_PROJEKTU', projekt)
        plik_nginxa += l

    # Zapis edytowanego szablonu nginx:
    with open(f"/etc/nginx/sites-available/{domena}", "w") as plik1:
        plik1.write(plik_nginxa)

    # Stworzenie linku do kopii pliku nginx:
    os.system(f'sudo ln -s /etc/nginx/sites-available/{domena} /etc/nginx/sites-enabled/')

    for l in plik_gunicorn_template:
        l = l.replace('NAZWA_PROJEKTU', projekt)
        plik_gunicorn +=l

    # Zapis edytowanego szablonu pliku gunicorn
    with open("/etc/systemd/system/" + projekt + '.service', "w") as plik2:
        plik2.write(plik_gunicorn)

    # Restart serwisu,oraz restart WSGI Nginx.
    os.system('sudo systemctl start ' + projekt + '.service')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl restart nginx')
    os.system('sudo systemctl restart ' + projekt + '.service')


if __name__ == '__main__':
        domena = sys.argv[1]
        projekt = sys.argv[2]
        create_nginx_and_gunicorn_files(domena, projekt)
