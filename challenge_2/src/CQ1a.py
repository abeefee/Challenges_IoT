from scapy.all import rdpcap, UDP, IP, IPv6
import binascii

print("Caricamento del file A.pcapng in corso...")
packets = rdpcap('A.pcapng') 

COAP_ME_IP = "134.102.218.18"

# STEP 1: Raccogliamo le richieste (CQ1a)
requests_found = {} # Dizionario: {Token_Hex : MID_Richiesta}

for pkt in packets:
    if pkt.haslayer(UDP) and pkt[UDP].dport == 5683:
        ip_dst = pkt[IP].dst if pkt.haslayer(IP) else (pkt[IPv6].dst if pkt.haslayer(IPv6) else None)
            
        if ip_dst == COAP_ME_IP:
            payload = bytes(pkt[UDP].payload)
            if len(payload) >= 4:
                version = (payload[0] & 0xC0) >> 6
                msg_type = (payload[0] & 0x30) >> 4 
                tkl = payload[0] & 0x0F
                code = payload[1]                    
                mid = (payload[2] << 8) | payload[3] 
                
                # DELETE (4), NON (1)
                if version == 1 and msg_type == 1 and code == 4:
                    token_bytes = payload[4 : 4 + tkl]
                    token_hex = binascii.hexlify(token_bytes).decode('utf-8')
                    # Gestiamo Token vuoti per chiarezza
                    if token_hex == "": token_hex = "[Vuoto]"
                    requests_found[token_hex] = mid

# STEP 2: Raccogliamo le risposte (CQ1b)
success_responses = {} # Dizionario: {Token_Hex : MID_Risposta}

for pkt in packets:
    if pkt.haslayer(UDP) and pkt[UDP].sport == 5683: 
        ip_src = pkt[IP].src if pkt.haslayer(IP) else (pkt[IPv6].src if pkt.haslayer(IPv6) else None)
            
        if ip_src == COAP_ME_IP:
            payload = bytes(pkt[UDP].payload)
            if len(payload) >= 4:
                version = (payload[0] & 0xC0) >> 6
                tkl = payload[0] & 0x0F
                code = payload[1]                    
                mid = (payload[2] << 8) | payload[3]
                
                # 2.02 Deleted (66)
                if version == 1 and code == 66:
                    token_bytes = payload[4 : 4 + tkl]
                    token_hex = binascii.hexlify(token_bytes).decode('utf-8')
                    if token_hex == "": token_hex = "[Vuoto]"
                    
                    if token_hex in requests_found:
                        success_responses[token_hex] = mid


# --- STAMPA DEI RISULTATI ---
print(f"\n{'='*40}")
print(f"RISULTATI CQ1 (A.pcapng)")
print(f"{'='*40}")

print(f"\n[CQ1a] Richieste DELETE NON verso coap.me trovate: {len(requests_found)}")
print("-" * 50)
for token, req_mid in sorted(requests_found.items(), key=lambda x: x[1]):
    # Controlliamo se questa richiesta ha avuto una risposta di successo
    if token in success_responses:
        resp_mid = success_responses[token]
        status = f"✅ SUCCESSO! -> Risposta ricevuta (MID: {resp_mid})"
    else:
        status = "❌ FALLITA/NESSUNA RISPOSTA"
        
    print(f"Richiesta (MID: {req_mid:5} | Token: {token:8}) ---> {status}")

print(f"\n[CQ1b] Totale richieste andate a buon fine: {len(success_responses)}")