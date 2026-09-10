def conta_slash_nel_file(percorso_file):
    # Numero di slash, quante righe lo hanno
    distribuzione_slash = {}
    
    try:        
        with open(percorso_file, 'r') as file:
            for riga in file:
                riga = riga.strip()
                if riga:
                    numero_slash = riga.count('/')
                    if numero_slash in distribuzione_slash:
                        distribuzione_slash[numero_slash] += 1
                    else:
                        distribuzione_slash[numero_slash] = 1
                    
        print(f"--- {percorso_file} ---")
        for slash in sorted(distribuzione_slash.keys()):
            # Se ho 1 slash -> 2 livelli, 2 slash -> 3 livelli etc.
            livelli = slash + 1
            print(f"N. Livelli: {livelli}: {distribuzione_slash[slash]} messaggi")
            
    except FileNotFoundError:
        print(f"Errore")

# Esecuzione

nome_del_tuo_file = 'topics_A.txt' 
conta_slash_nel_file(nome_del_tuo_file)

nome_secondo_file = 'topics_B.txt'
conta_slash_nel_file(nome_secondo_file)