"""
This file was created and tested by Erwin - PA3EFR
"""


import socket
import re
import winsound  # Voor Windows; gebruik 'playsound' voor andere systemen.

# Configuratie: pas deze waarden aan
HOST = "www.db0erf.de"  # Vervang door de host-IP van het DXCluster van lijst https://www.dxcluster.info/telnet/dxcluster_up.htm
PORT = 41113                    # Vervang door de poort van het DXCluster
CALLSIGN = "PA3EFR"     # Vervang door je callsign of gebruikersnaam
#patterns = [r"B/", r"WWFF", r"POTA", r"COTA", r"SOTA", r"BOTA"]
patterns = [r"B/", r"BOTA"]

def play_alarm():
    """Speelt een alarmsignaal af met vijf tonen."""
    frequencies = [1500, 1600, 1700, 1800, 1900, 2000, 2200, 2400, 2600, 2800]  # Frequenties in Hertz
    duration = 100  # Duur van elke toon in milliseconden

    for frequency in frequencies:
        winsound.Beep(frequency, duration)

def main():
    # Maak verbinding met het DXCluster
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Verbinden met {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("Verbonden. Verstuur login...")

        # Verstuur logincommando
        login_command = f"{CALLSIGN}\n"  # Vaak is het gewoon de callsign gevolgd door een newline
        s.sendall(login_command.encode("utf-8"))
        print(f"Ingelogd als: {CALLSIGN}")
        printnr = 0
        try:
            while True:
                # Ontvang data van de socket
                data = s.recv(1024).decode("utf-8")
                data = data.upper()
                if not data:
                    break  # Verbinding is gesloten door de server

                # Toon ontvangen data (optioneel)
                #print(data)


                # Controleer op "B/" in de ontvangen tekst
                for pattern in patterns:
                    if re.search(pattern, data):
                        print(f"Alarm: '{pattern}'")
                        print (data)
                        play_alarm()

                #if re.search(r"\bSOTA\b", data):
                #    print("Alarm: 'B/' gevonden!")
                #    play_alarm()

        except KeyboardInterrupt:
            print("Script gestopt door gebruiker.")
        except Exception as e:
            print(f"Fout opgetreden: {e}")

if __name__ == "__main__":
    main()
