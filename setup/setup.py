import os

#Instalacja podstawowych pakietów do uruchomienia aplikacji napisanych w pythconie
os.system('sudo apt install python3-pip python3-dev python3-venv build-essential\
          libssl-dev libffi-dev python3-setuptools --yes')

# Deinstalacja apache2 oraz instalacja nginx
os.system('sudo apt remove apache2 --yes')
os.system('sudo apt install nginx --yes')

# Uruchomienie usługi nginx
os.system('sudo systemctl enable nginx')
os.system('sudo systemctl start nginx')

# stworzenie katalogu do przechowywania projektu
os.system('sudo rm -r /var/www/html')
os.system('sudo chown -R www-data:www-data /var/www')
os.system('sudo chmod -R 775 /var/www')

