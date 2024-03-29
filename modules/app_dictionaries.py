
class Dictionaries():
    _AppVars = {
        'Language': 1,  # 0-English, 1-Polish,
        'Device active': 0,
        'recon_dane': False,
        'live': 0,
        'message': '',
        'start_recon': False,
    }

    _AppModel = {
        'Model': 0,
        'U1': [],
        'U2': [],
        'Wx': [],
        'Wy': [],
        'Wz': [],
        'value_x': [],
        'value_y': [],
        'value_z': [],
        'fig_slices': [],
        'stim_pattern': [],
        'raw_data': [],
    }

    _AppLang = {
        'Do you want to close the application?': ['Do you want to close the application?', 'Czy chcesz zamknąć aplikację?'],
        'Do you want to restart the application?': ['Do you want to restart the application?', 'Czy chcesz ponownie uruchomić aplikację?'],
        'Do you want to reboot the device?': ['Do you want to reboot the device?', 'Czy chcesz zrestartować urządzenie?'],
        'Do you want to turn off the device?': ['Do you want to turn off the device?', 'Czy chcesz wyłączyć urządzenie?'],
        'Electrical Impedance Tomography Device': ['Electrical Impedance Tomography Device', 'Urządzenie do Tomografii Impedancyjnej'],
        'Hide': ['Hide', 'Ukryj'],
        'Home': ['Home', 'Start'],
        'Widgets': ['Widgets', 'Widżety'],
        'Language': ['Language', 'Język'],
        'Tryb': ['Type', 'Tryb'],
        'Stim': ['Stim pattern', 'Wzorzec stymulacji'],
        'Freq': ['Frequency', 'Częstotliwość'],
        'Interval frame': ['Interval frame', 'Interwał między ramkami'],
        'Amp': ['Amp', 'Amp'],
        'Int frame': ['No. frame', 'Liczba ramek'],
        'Live': ['Live', 'Live'],
        'Send param': ['Send param', 'Wyślij parametry'],

        'EIT 3D': ['EIT 3D', 'EIT 3D'],
        'Visualisation': ['Vis. slices', 'Wiz. przekrojów'],
        'Measurment': ['Measurment', 'Pomiary'],
        'Reconstruction': ['Reconstruction', 'Rekonstrukcja'],
        'Save': ['Save', 'Zapisz'],
        'Exit': ['Exit', 'Wyjdź'],
        'Settings': ['Settings', 'Ustawienia'],
        'More Options': ['More Options', 'Więcej Opcji'],
        'Close Application': ['Close Application', 'Zamknij Aplikację'],
        'Restart Application': ['Restart Application', 'Uruchom Ponownie aplikację'],
        'Reboot Device': ['Reboot Device', 'Uruchom Ponownie Urządzenie'],
        'Shut Down': ['Shut Down', 'Zamknięcie'],
        'TEST': ['TEST', 'TEST'],
        'Method of reconstruction': ['Method of reconstruction', 'Metody rekonsrukcji'],
        'Model EIT': ['Model EIT', 'Model EIT'],
        'Voltages EIT': ['Voltages EIT', 'Pomiary EIT'],
        'Number of iteration': ['Number of iteration', 'Liczba iteracji'],
        'Reconstruction EIT': ['Reconstruction EIT', 'Rekonstrucja EIT'],
        'Reconstruction EIT from device': ['Reconstruction EIT from device', 'Rekonstrucja EIT z urządzenia'],
        'Regularyzation Parameter': ['Regularyzation Parameter', ' Parametr regualryzacji'],
        'Slice plane x = ': ['Slice plane x = ', 'Przekrój płaszczyzną x = '],
        'Slice plane y = ': ['Slice plane y = ', 'Przekrój płaszczyzną y = '],
        'Slice plane z = ': ['Slice plane z = ', 'Przekrój płaszczyzną z = '],
        'Visualization voltages': ['Visualization voltages', 'Wizualizacja pomiarów'],
        'Save Visualization': ['Save Vis', 'Zapisz wiz'],
        'Color map': ['Color map', 'Mapa kolorów']

    }
    _AppNotifications = {
        'LanguageChange': ['Language changed to English.', 'Język zmieniono na Polski.'],
        'Save Visualization': ['Visualization saved to ', 'Wizualizację zapisano do pliku '],
        'Active Device': ['Davice is conected', 'Użądzenie zostało podłączone'],
        'Send param device': ['Send param device', 'Wysyłam parametry urządzenia'],
        'Send param frames': ['Send param frames', 'Wysyłam parametry ramki'],
        'Recive frame': ['Recive frame', 'Odbieram ramkę danych'],
        'Recon': ['Do reconstruction', 'Przystępuję do rekocstrukcji'],
        'Recon dane': ['Reconstruction done', 'Rekonstrukcja wykonana'],
        'Recon n done': ['All frames reconstruction', 'Wszystkie ramki zrekonstruowane'],
        'Connection field': ['Connection field', 'Nieudane połączenie'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
        'TEST': ['TEST', 'TEST'],
    }
