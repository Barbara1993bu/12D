#! /usr/bin/python
"""
  _   _          _            _            ____       _
 | \ | |   ___  | |_   _ __  (_) __  __   / ___|     / \
 |  \| |  / _ \ | __| | '__| | | \ \/ /   \___ \    / _ \
 | |\  | |  __/ | |_  | |    | |  >  <     ___) |  / ___ \
 |_| \_|  \___|  \__| |_|    |_| /_/\_\   |____/  /_/   \_\


  __  __               _   _                       _____    ____   ____
 |  \/  |   ___     __| | | |__    _   _   ___    |_   _|  / ___| |  _ \
 | |\/| |  / _ \   / _` | | '_ \  | | | | / __|     | |   | |     | |_) |
 | |  | | | (_) | | (_| | | |_) | | |_| | \__ \     | |   | |___  |  __/
 |_|  |_|  \___/   \__,_| |_ __/   \__,_| |___/     |_|    \____| |_|


 Autor: SD (szymon.dejnek@netrix.com.pl)
 Ver: 1.0


 Metody do obłusgi sterowika PLC unitronics za pomocą protokołu ModbusTCP z wykorzystaniem biblioteki pyModbusTCP

 Niniejszy softwere jest przystosowany do pracy ze sterownikiem PLC unitronics USC-B10-TR22 za pomocą protokołu ModbusTCP
 Do poprawnego działania wymagana jest biblioteka pyModbusTCP
 INSTALACJA https://pymodbustcp.readthedocs.io/en/latest/quickstart/index.html
"""


class ModbusTCP_feedback(object):
    def __init__(self, adres_ip):
        '''Inicjalizacja połączenia ze sterownikiem.
            Adres ip w sterowniku 192.186.0.3 i z takim adresem należy się połączyć.
            Jeżeli nie da się połączyć należy w ustawieniach karty sieciowej sprawdzić jaki adres ip (lokalny) ustawiony jest w komputerze.
            Aby to zrobić należy:
            wejść w ustawienia --> Sieć i internet --> Zmień opcje karty
            Następne należy znaleźć odpowiedną ikonę od karty sieciowej (Ethernet) i wejść w jej właściwości.
            Należy zaznaczyć "Protokół internetowy wersji 4 (TCP/IPv4)" i kliknąć w Właściwości
            Następnie zaznaczyć obszar "Użyj następującego adresu IP:" i w poszczególne pola wspisać.
            Adres IP: 192.168.0.2
            Maska podsieci: 255.255.255.0
            Brama domyślna: 192.168.0.1
            zapisać ustawienia
            '''
        from pyModbusTCP.client import ModbusClient
        from time import sleep
        try:
            self.client = ModbusClient(adres_ip, port=502, timeout=30)

            print('Zinicjalizowano protokół Modbus TCP dla sterownika PLC.\n'
                  'Adres ip: ', adres_ip, '\n'
                  'PORT: 502')
            sleep(0.1)
            print(' ','\n',
                  ' ','\n',
                  ' ')
            print(" __  __               _   _                       _____    ____   ____")
            sleep(0.05)
            print("|  \/  |   ___     __| | | |__    _   _   ___    |_   _|  / ___| |  _ \ ")
            sleep(0.05)
            print("| |\/| |  / _ \   / _` | | '_ \  | | | | / __|     | |   | |     | |_) |")
            sleep(0.05)
            print("| |  | | | (_) | | (_| | | |_) | | |_| | \__ \     | |   | |___  |  __/ ")
            sleep(0.05)
            print("|_|  |_|  \___/   \__,_| |_ __/   \__,_| |___/     |_|    \____| |_|   ")
            sleep(0.2)
            print('\n')
            print("Autor: SD")
            sleep(0.1)
            print("Ver: 1.0")
            sleep(0.1)
            print("Tylko do użytku wewnętrznego.")
            sleep(0.1)
            print(' ')

            if self.connect() == True:
                self.setting()
            else:
                print('Nie udało się połączyć...')
                raise Exception
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def __del__(self):
        self.disconnect()

    def setting(self):
        """Wszystkie bity, które są wykorzystywane należy ustawić na 0"""
        from time import sleep
        try:
            adresy = [0, 1, 10, 11, 20, 21, 30, 31, 40, 41, 50, 51, 52, 53, 60, 61, 70, 71, 80, 81, 90, 91]
            print('Wgrywanie ustawień...')
            print('...')
            for i in adresy:
                    self.client.write_single_coil(bit_value=False, bit_addr=i)
            for i in adresy:
                if self.is_open() == True:
                    if self.client.read_coils(bit_addr=i, bit_nb=1) == True:
                        a = 1
                    else:
                        a = 0
                    print('Adres ', i, ' ustawiony na ', a)
                    sleep(0.1)
                else:
                    raise ConnectionError
            # kod poniżej ustawia zadaną wartość temperatury, ph i poziomu natlenienia.
            # W docelowym programie na PLC sterującym fizycznym obiektem poniższy kod będzie można usunąć
            self.nastawy()
        except ConnectionError:
            print('Połączenie zerwane')
        except:
            print('Wgrywanie ustawień początkowych nie powiodło się')

    #funkcja nastawy tylko do ustwienia wartośći na wyświetlaczu, domyślnie wartości będą odczytywane z czujników
    def nastawy(self):
        self.client.write_single_register(reg_addr=0, reg_value=2500)  # wgranie temp1  25 st.C
        self.client.write_single_register(reg_addr=1, reg_value=3243)  # temp 2 32.43
        self.client.write_single_register(reg_addr=4, reg_value=827)  # ph 8.27
        self.client.write_single_register(reg_addr=6, reg_value=6250)  # 6.25 bar
        print('...')

    def connect(self):
        """Połączenie"""
        try:
            self.client.open()
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')
        return self.client.open()

    def disconnect(self):
        """Rozłączenie"""
        try:
            self.client.close()
            print('Rozłączono')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def is_open(self):
        """:return True jeśli jest połączenie z serwerem
        :rtype bool:"""
        return self.client.is_open

    def start(self):
        """Uruchomienie sterowania"""
        try:
            self.client.write_single_coil(bit_addr=1, bit_value=True)
            print('Wysłano START')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def stop(self):
        """Wyłączenie sterowania"""
        try:
            self.client.write_single_coil(bit_addr=0, bit_value=True)
            print('Wysłano STOP')
            print('Wszystkie maszyny wyłączone')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def is_on(self):
        """Sprawdzanie czy sterowanie jest uruchomione. Na HMI wyświetlane jest jako status."""
        try:
            # print(self.client.read_coils(bit_addr=99))
            if (self.client.read_coils(bit_addr=2)) == [True]:
                return True
            else:
                # print('Najpierw uruchom system')
                return False
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def start_pump(self, pump):
        """Uruchomienie pompy.
        :param pump: Wybór pompy (od 1 do 4)
        :type pump: int"""
        pump_adr = [11, 21, 31, 41]
        try:
            self.client.write_single_coil(bit_value=True, bit_addr=pump_adr[pump - 1])
            print('Pompa numer ', pump, ' uruchomiona')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def stop_pump(self, pump):
        """Wyłączenie pompy.
        :param pump: Wybór pompy (od 1 do 4)
        :type pump: int"""
        pump_adr = [10, 20, 30, 40]
        try:
            self.client.write_single_coil(bit_value=True, bit_addr=pump_adr[pump - 1])
            print('Pompa numer ', pump, ' wyłączona')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def start_mixer(self,mixer):
        """Uruchomienie mieszadła
            :param mixer: wybór mieszadła (1 lub 2)"""
        mix_adr = [51, 52]
        try:
            self.client.write_single_coil(bit_value=True, bit_addr=mix_adr[mixer - 1])
            print('Mieszadło uruchomione')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def stop_mixer(self,mixer):
        """Wyłączenie mieszadła
        :param mixer: wybór mieszadła (1 lub 2)"""
        mix_adr = [50,53]
        try:
            self.client.write_single_coil(bit_value=True, bit_addr=mix_adr[mixer - 1])
            print('Mieszadło zatrzymane')
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    # def start_heat(self):
    #     """Uruchomieni grzałki"""
    #     try:
    #         self.client.write_single_coil(bit_value=True, bit_addr=61)
    #         print('Grzałka uruchomiona')
    #     except:
    #         print('Coś poszło nie tak...','\n'
    #               'Spróbuj ponownie...')
    #
    # def stop_heat(self):
    #     """Wyłączenie grzałki"""
    #     try:
    #         self.client.write_single_coil(bit_value=True, bit_addr=60)
    #         print('Grzałka wyłączona')
    #     except:
    #         print('Coś poszło nie tak...','\n'
    #               'Spróbuj ponownie...')
    #
    # def start_oxygen(self):
    #     """Uruchomienie pompy natleniającej"""
    #     try:
    #         self.client.write_single_coil(bit_value=True, bit_addr=71)
    #         print('Natlenianie uruchomione')
    #     except:
    #         print('Coś poszło nie tak...','\n'
    #               'Spróbuj ponownie...')
    #
    # def stop_oxygen(self):
    #     """Wyłączenie pompy natleniającej"""
    #     try:
    #         self.client.write_single_coil(bit_value=True, bit_addr=70)
    #         print('Natlenianie wyłączone')
    #     except:
    #         print('Coś poszło nie tak...','\n'
    #               'Spróbuj ponownie...')

    def open_valve(self,valve):
        """Otwarcie zaworow
        :param valve: wybor zaworu 1 lub 2"""
        valve_adr = [81,91]
        try:
            self.client.write_single_coil(bit_value=True,bit_addr=valve_adr[valve - 1])
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def close_valve(self,valve):
        """Zamkniecie zaworow
        :param valve: wybor zaworu 1 lub 2"""
        valve_adr = [80,90]
        try:
            self.client.write_single_coil(bit_value=True,bit_addr=valve_adr[valve - 1])
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')


    def read_temp(self,temp):
        """Odczyt temperatury w st. C.
        :param temp: wybierz odczyt temperatury 1 lub 2
        :return Wartość temperatury"""
        temp_adr = [0,1]
        try:
            str_temp = ('')
            temp = self.conv_temp(int(self.client.read_input_registers(reg_addr=temp_adr[temp - 1], reg_nb=1)[0]))
            #print(temp[0])
            if temp[0] == 1:
                str_temp = '-' + str(temp[1])
            if temp[0] == 0:
                str_temp = str(temp[1])
            return str_temp
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def read_ph(self):
        """Odczyt wartosci pH.
        :return Wartość pH"""
        try:
            read = self.client.read_input_registers(reg_addr=4, reg_nb=1)
            ph = int(read[0])
            return ph
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def read_oxygen(self):
        """Odczyt wartości tlenu w %
        :return Wartość % tlenu w zbiorniku"""
        try:
            read = self.client.read_input_registers(reg_addr=5, reg_nb=1)
            oxy = int(read[0])
            return oxy
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')

    def read_pressure(self):
        """Odczyt wartosci cisnienia w barach
        :return Wartosc ciesnienia w barach"""
        try:
            read = self.client.read_input_registers(reg_addr=6,reg_nb=1)
            psi = int(read[0])
            return psi
        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')


    # Poniżej znajdują się funkcje do wysyłania wartości temperatury, poziomu tlenu i pH. Tylko do testow
    def send_temp(self, value, temp):
        temp_adr = [0,1]
        try:
            if value < 32768 and value >= 0:
                send = value
            if value > - 32767 and value < 0:
                #print('wartos ujemna')
                send = 65536 - abs(value)
            self.client.write_single_register(reg_addr=temp_adr[temp - 1], reg_value=send)
        except:
            print('Coś poszło nie tak...','\n'
                  'Spóbuj ponownie...')

    def send_oxygen(self, value):
        try:
            self.client.write_single_register(reg_addr=5, reg_value=value)
        except:
            print('Coś poszło nie tak...','\n'
                  'Spóbuj ponownie...')

    def send_ph(self, value):
        try:
            self.client.write_single_register(reg_addr=4, reg_value=value)
        except:
            print('Coś poszło nie tak...','\n'
                  'Spóbuj ponownie...')

    def send_psi(self, value):
        try:
            self.client.write_single_register(reg_addr=6,reg_value=value)
        except:
            print('Coś poszło nie tak...','\n'
                  'Spóbuj ponownie...')

    #funkcja ktora konwertuja podana wartosc temepratury na wartosc liczbową do rejestru
    def conv_temp(self,temp):
        try:
            temp_bin = bin(temp)[2:]
            if len(temp_bin) == 16:
                return 1, float(((int(temp) ^ 65535) +1)/100)
            else:
                return 0, float(int(temp)/100)

        except:
            print('Coś poszło nie tak...','\n'
                  'Spróbuj ponownie...')


# ponieżej kod do testowania

server = ModbusTCP_feedback('192.168.0.3')
import os

clear = lambda: os.system('cls')
a = input('Wciśnij przycisk...')
clear()

comands = ['1', '0', 'mix_off', 'mix_on', 'pump_on', 'pump_off', 'exit', 'heat_on', 'heat_off', 'psi', 'temp', 'ph', 'oxygen',
           'oxygen_on', 'oxygen_off', 's_temp', 's_ph', 's_oxygen', 'valve_on', 'valve_off', 's_psi']

pumps = ['1', '2', '3', '4']

valves = ['1','2']

menu = '\n'\
       '----------------\n' \
       ' Lista poleceń:\n' \
       '----------------\n' \
       ' 1 - Start systemu\n' \
       ' 0 - Stop systemu\n\n' \
       '-- Sterowanie --\n' \
       ' mix_on/off - włącz/wyłącz mieszadło\n' \
       ' pump_on/off - włącz/wyłącz pompe\n' \
       ' valve_on/off - włącz/wyłącz zawor\n\n' \
       '-- Odczyty --\n' \
       ' temp - temperatura\n' \
       ' ph - pH\n' \
       ' psi - ciśnienie\n\n' \
       '---------------\n' \
       ' exit - wyłącz\n' \
       '---------------'  \

while server.is_open() == True:
    print(menu)

    key = input()

    clear()

    if key in comands:
        if key == '1':
            server.start()
        if key == '0' and server.is_on() == True:
            server.stop()
        if key == 'exit':
            server.stop()
            break
        if key == 's_temp' and server.is_on() == True:
            value = input('Podaj wartość temperatury ')
            temp = input('TEMP 1 czy 2? ')
            try:
                value = float(value)
                value = value * 100
                value = int(value)
                server.send_temp(value,int(temp))
            except:
                print('blad')
        if key == 's_oxygen' and server.is_on() == True:
            value = input('Podaj wartosc % tlenu ')
            try:
                value = int(value)
                server.send_oxygen(value)
            except:
                print('blad')
        if key == 's_ph' and server.is_on() == True:
            value = input('Podaj wartosc pH ')
            try:
                value = int(value)
                server.send_ph(value)
            except:
                print('blad')

        if key == 's_psi' and server.is_on() == True:
            value = input('Podaj wartosc cisnienia ')
            try:
                value = int(value)
                server.send_psi(value)
            except:
                print('blad')

        if (key == 'mix_on') and server.is_on() == True:
            server.start_mixer(1)
            server.start_mixer(2)
        if key == 'mix_off' and server.is_on() == True:
            server.stop_mixer(1)
            server.stop_mixer(2)
        if key == 'pump_on' and server.is_on() == True:
            server.start_pump(1)
            # while True:
            #     print(' ')
            #     print('Podaj numer pompy którą chce uruchomić (1-4): ')
            #     print('Aby włączyć wszystkie wpisz all')
            #     print('Aby wrócić wpisz back')
            #     numer = input('Numer: ')
            #     if numer == 'back':
            #         break
            #     if numer == 'all':
            #         for i in range(1, 5):
            #             server.start_pump(i)
            #         break
            #     if numer in pumps:
            #         server.start_pump(int(numer))
            #         break
            #     else:
            #         print('Nie ma takiej pompy')
            #         print('-------------------')

        if key == 'pump_off' and server.is_on() == True:
            server.stop_pump(1)
            # while True:
            #     print(' ')
            #     print('Podaj numer pompy którą chce uruchomić (1-4): ')
            #     print('Aby włączyć wszystkie wpisz all')
            #     print('Aby wrócić wpisz back')
            #     numer = input('Numer: ')
            #     if numer == 'back':
            #         break
            #     if numer == 'all':
            #         for i in range(1, 5):
            #             server.stop_pump(i)
            #         break
            #     if numer in pumps:
            #         server.stop_pump(int(numer))
            #         break
            #     else:
            #         print('Nie ma takiej pompy')
            #         print('-------------------')

        if key == 'valve_on' and server.is_on() ==True:
            while True:
                print('\n')
                print('Podaj numer zaworu, ktory chcesz otworzyć (1 lub 2): \n')
                print('Aby włączyć dwa wpisz all\n')
                print('Aby wrocić wpisz back\n')
                numer = input('Numer: ')
                if numer == 'back':
                    break
                if numer == 'all':
                    server.open_valve(1)
                    server.open_valve(2)
                    break
                if numer in valves:
                    server.open_valve(int(numer))
                    break
                else:
                    print('Nie ma takiego zaworu\n')

        if key == 'valve_off' and server.is_on() ==True:
            while True:
                print('\n')
                print('Podaj numer zaworu, ktory chcesz zamknąć (1 lub 2): \n')
                print('Aby zamknąć dwa wpisz all\n')
                print('Aby wrocić wpisz back\n')
                numer = input('Numer: ')
                if numer == 'back':
                    break
                if numer == 'all':
                    server.close_valve(1)
                    server.close_valve(2)
                    break
                if numer in valves:
                    server.close_valve(int(numer))
                    break
                else:
                    print('Nie ma takiego zaworu\n')

        # if key == 'heat_on' and server.is_on() == True:
        #     server.start_heat()
        # if key == 'heat_off' and server.is_on() == True:
        #     server.stop_heat()
        # if key == 'oxygen_on' and server.is_on() == True:
        #     server.start_oxygen()
        # if key == 'oxygen_off' and server.is_on() == True:
        #     server.stop_oxygen()
        if key == 'temp':
            print('Temperatura 1 wynosi ', server.read_temp(1), ' st. C')
            print('Temperatura 2 wynosi ',server.read_temp(2),' st. C')
        if key == 'ph':
            print('pH wynosi ', server.read_ph())
        if key == 'oxygen':
            print('Poziom tlenu wynosi ', server.read_oxygen(), ' %')
        if key == 'psi':
            print('Cisnienie wynosi ',server.read_pressure(), ' bar')
        if server.is_on() == False and (key != '1' or key == '0') and key != 'temp' and key != 'oxygen' and key != 'ph':
            print('Najpierw wyślij 1')


    else:
        print('Podałeś złą komendę ')
