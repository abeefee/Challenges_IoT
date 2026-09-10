from scapy.all import rdpcap, UDP

print("Caricamento del file A.pcapng in corso...")
try:
    packets = rdpcap('A.pcapng')
except Exception as e:
    print(f"Errore: {e}")
    exit()

messaggi_da_broker = 0

for pkt in packets:
    # Cerchiamo pacchetti UDP dove la porta SORGENTE (sport) è 1885
    # Questo indica che il mittente è il broker locale in ascolto su quella porta
    if pkt.haslayer(UDP) and pkt[UDP].sport == 1885:
        messaggi_da_broker += 1

print("\n" + "="*50)
print(f"RISPOSTA CQ4:")
print(f"Totale messaggi MQTT-SN inviati dal broker ai client: {messaggi_da_broker}")
print("="*50)