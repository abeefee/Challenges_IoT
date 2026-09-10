from scapy.all import rdpcap, UDP, IP, IPv6
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Caricamento del file A.pcapng in corso...")
packets = rdpcap('A.pcapng')

LOCAL_IPS = ["127.0.0.1", "::1", "0.0.0.0", "::"]

# Fase 1: Raccogliamo tutte le richieste CON POST e CON PUT
requests_info = {}

for pkt in packets:
    if pkt.haslayer(UDP) and pkt[UDP].dport == 5683:
        ip_dst = pkt[IP].dst if pkt.haslayer(IP) else (pkt[IPv6].dst if pkt.haslayer(IPv6) else None)
        
        if ip_dst in LOCAL_IPS:
            payload = bytes(pkt[UDP].payload)
            if len(payload) >= 4:
                version = (payload[0] & 0xC0) >> 6
                msg_type = (payload[0] & 0x30) >> 4 
                code = payload[1]                    
                mid = (payload[2] << 8) | payload[3] 
                
                # Se è CON (0) e POST (2) o PUT (3)
                if version == 1 and msg_type == 0 and code in [2, 3]:
                    method_name = 'POST' if code == 2 else 'PUT'
                    
                    # Estraiamo l'URI-Path
                    tkl = payload[0] & 0x0F
                    opt_offset = 4 + tkl
                    uri_path_parts = []
                    current_opt_num = 0
                    
                    while opt_offset < len(payload) and payload[opt_offset] != 0xFF:
                        opt_delta = (payload[opt_offset] & 0xF0) >> 4
                        opt_len = payload[opt_offset] & 0x0F
                        opt_offset += 1
                        
                        if opt_delta == 13: opt_delta = payload[opt_offset] + 13; opt_offset += 1
                        elif opt_delta == 14: opt_delta = (payload[opt_offset] << 8) | payload[opt_offset+1] + 269; opt_offset += 2
                            
                        if opt_len == 13: opt_len = payload[opt_offset] + 13; opt_offset += 1
                        elif opt_len == 14: opt_len = (payload[opt_offset] << 8) | payload[opt_offset+1] + 269; opt_offset += 2
                            
                        current_opt_num += opt_delta
                        
                        if current_opt_num == 11:
                            val = payload[opt_offset : opt_offset + opt_len]
                            uri_path_parts.append(val.decode('utf-8', errors='ignore'))
                            
                        opt_offset += opt_len
                    
                    full_uri = "/" + "/".join(uri_path_parts) if uri_path_parts else "/"
                    
                    if mid not in requests_info:
                        requests_info[mid] = {'method': method_name, 'uri': full_uri}


# Fase 2: Analizziamo TUTTE le risposte dal server locale
mid_status = {} # Mappa MID -> 'SUCCESS' o 'FAILED'

for pkt in packets:
    if pkt.haslayer(UDP) and pkt[UDP].sport == 5683:
        ip_src = pkt[IP].src if pkt.haslayer(IP) else (pkt[IPv6].src if pkt.haslayer(IPv6) else None)
        
        if ip_src in LOCAL_IPS:
            payload = bytes(pkt[UDP].payload)
            if len(payload) >= 4:
                version = (payload[0] & 0xC0) >> 6
                code = payload[1]                    
                mid = (payload[2] << 8) | payload[3]
                
                if version == 1:
                    if code >= 128:
                        mid_status[mid] = 'FAILED'
                    elif 64 <= code < 128:
                        # Codici 2.xx (da 64 a 127) indicano SUCCESSO
                        mid_status[mid] = 'SUCCESS'

# Fase 3: Conteggio Globale per risorsa
resource_counts = {}

for mid, info in requests_info.items():
    uri = info['uri']
    method = info['method']
    
    if uri not in resource_counts:
        resource_counts[uri] = {
            "POST_failed": 0, "PUT_failed": 0,
            "POST_success": 0, "PUT_success": 0,
            "Timeout": 0
        }
        
    status = mid_status.get(mid)
    
    if status == 'FAILED':
        resource_counts[uri][f"{method}_failed"] += 1
    elif status == 'SUCCESS':
        resource_counts[uri][f"{method}_success"] += 1
    else:
        resource_counts[uri]["Timeout"] += 1

# Fase 4: Stampa dettagliata (Versione ASCII sicura)
matching_resources = 0
print("\n" + "="*50)
print("RADIOGRAFIA RISORSE SERVER LOCALE (POST/PUT)")
print("="*50)

for uri, counts in resource_counts.items():
    X = counts["POST_failed"]
    Y = counts["PUT_failed"]
    post_ok = counts["POST_success"]
    put_ok = counts["PUT_success"]
    timeout = counts["Timeout"]
    
    print(f"\n[Dir] Risorsa: {uri}")
    print(f"  |-- POST: [X] {X} Falliti | [V] {post_ok} Riusciti")
    print(f"  |-- PUT : [X] {Y} Falliti | [V] {put_ok} Riusciti")
    if timeout > 0:
        print(f"  \\-- [!] {timeout} richieste ignorate/perse (Timeout)")
    
    if X == Y and X > 0:
        matching_resources += 1
        print("  *** [MATCH CQ2!] Questa risorsa ha X=Y con X>0 ***")

print("\n" + "="*50)
print(f"RISPOSTA FINALE CQ2:")
print(f"Numero di risorse con POST falliti = PUT falliti (>0): {matching_resources}")
print("="*50)