# Challenges e Homework - Progetto IoT 2025/26

*You can read this also in [English](README.md)*

> **Nota Accademica:** Queste challenges sono state sviluppate per il corso di *Internet of Things* presso il Politecnico di Milano (Anno Accademico 2025/26), ottenendo una valutazione finale di **28/28**.

## Challenge 1 - Wokwi e Consumo Energetico

### Descrizione del Progetto
Sviluppo di un sensore di movimento IoT in stile commerciale per smart home utilizzando l'emulazione Wokwi. Il dispositivo rileva il movimento umano e misura l'illuminazione ambientale, trasmettendo stringhe strutturate (MOTION_DETECTED-LUMINOSITY:ZZZ) tramite ESP-NOW a un nodo sink centrale. Per ottimizzare il consumo energetico, il nodo alterna fasi di rilevamento/trasmissione attive a intervalli di deep sleep.

### Caratteristiche Tecnici
Implementato utilizzando un microcontrollore ESP32 con architettura basata su eventi. La durata del deep sleep *X[s]* e l'energia della batteria *Y[J]* sono parametrizzate dinamicamente in base al codice persona del capogruppo (*X = (AB\%50+5)/10*, *Y = ABCD\%5000+15000*). Il consumo energetico è modellato e validato combinando misurazioni temporali empiriche da Wokwi (*microsec()*) con profili di consumo energetico di riferimento nei vari stati (boot, Wi-Fi RX/OFF, deep sleep e letture dei sensori). Inoltre, i compromessi del routing multihop wireless nelle reti di sensori wireless (WSN) vengono valutati analiticamente utilizzando un modello di path-loss del consumo energetico (*E_{tx}(k,d) = k E_c + k \epsilon d^2*).

### Tecnologie  
*	**Linguaggi:** C++, Python
*	**Microcontrollore:** ESP32
*	**Framework:** Arduino
*	**Simulatore:** Wokwi
*	**Protocollo:** ESP-NOW

## Challenge 2 - Packet Sniffing e Analisi dei Protocolli

### Descrizione del Progetto
Analisi approfondita dei pacchetti (*packet sniffing*), del traffico e valutazione del protocollo di standard di messaggistica IoT vincolati (CoAP, MQTT e MQTT-SN) utilizzando file di cattura reali (A.pcapng e B.pcapng).

### Caratteristiche Tecnici
Analisi delle transazioni di messaggi, codici di stato, ritrasmissioni e interazioni con il broker di pubblicazione. Ciò include l'identificazione di richieste DELETE CoAP non confermabili riuscite, il filtraggio delle notifiche di osservazione CoAP e dei comportamenti delle risorse, il tracciamento del traffico MQTT-SN, la valutazione dei messaggi Last Will and Testament (LWT) con caratteri jolly (*wildcard*) e l'analisi della cancellazione dei messaggi conservati (*retained messages*) tra broker pubblici (HiveMQ) e locali. Include inoltre un'analisi statistica della distribuzione della profondità dei topic (rappresentazione ad istogramma dei layer dei messaggi PUBLISH) e una valutazione teorica del consumo energetico che confronta il CoAP diretto rispetto alle comunicazioni MQTT basate su gateway in presenza di specifici vincoli di RTO e QoS 1.

### Tecnologie  
*	**Strumenti:** Wireshark
*	**Linguaggi:** Python
*	**Librerie:** Pyshark, Scapy, Matplotlib
*	**Formati:** PCAPNG (Cattura Pacchetti)

## Challenge 3 - Pipeline Node-RED e LoRaWAN

### Descrizione del Progetto
Implementazione di una pipeline di elaborazione dati e automazione tramite Node-RED, affiancata da un'analisi teorica delle prestazioni della rete LoRaWAN.

### Caratteristiche Tecnici
Il flusso Node-RED genera periodicamente ID e timestamp casuali, pubblicandoli via MQTT su un broker Mosquitto locale e registrandoli in id_log.csv. Un ramo di sottoscrizione legge gli ID, calcola un'operazione di modulo (*N = ID \pmod{5218}*) per mapparli alle righe di un set di dati ZigBee fornito (challenge3.csv) e limita la velocità di elaborazione a 10 msg/min. Per i layer ZBEE_ZCL corrispondenti, struttura e ripubblica gli attributi del dispositivo. Per gli attributi di corrente RMS, tensione e potenza attiva, estrae ed associa le posizioni delle rispettive liste, registra i dati in filtered_elems.csv e li visualizza su dashboard in tempo reale. Per i pacchetti di stato del link (*link status*), calcola il costo di routing in uscita, lo registra in outgoing_cost.csv e invia periodicamente le metriche a un canale cloud ThingSpeak pubblico tramite API HTTP. La seconda parte valuta i parametri LoRaWAN europei (868 MHz, 125 kHz) utilizzando il calcolatore di airtime TTN per trovare lo Spreading Factor (SF) ottimale che garantisca una percentuale di successo dei pacchetti *\ge 75\%* sotto un'intensità di traffico di Poisson.

### Tecnologie  
*	**Piattaforma:** Node-RED
*	**Protocolli:** MQTT, API HTTP
*	**Broker:** Mosquitto
*	**Cloud e Dashboard:** ThingSpeak API, Node-RED Dashboard
*	**Linguaggi:** JavaScript (funzioni Node-RED), Python
*	**Formati Dati:** CSV, JSON

## Elaborati - Esercizi Teorici e Pratici

### Descrizione del Progetto
Raccolta completa di esercizi teorici e assegnazioni pratiche che coprono il networking di base, la modellazione del consumo energetico e i protocolli di comunicazione all'interno dei sistemi IoT.

### Caratteristiche Tecnici
*	**Modellazione Analitica:** Valutazione delle caratteristiche di consumo energetico, dei budget energetici e della vita operativa per dispositivi IoT alimentati a batteria.

*	**Ottimizzazione di Protocolli e Reti:** Valutazione dei compromessi tra comunicazioni dirette nodo-nodo e architetture assistite da gateway, analizzando metriche come tassi di successo dei pacchetti, budget di collegamento e calcoli del tempo di trasmissione (*airtime*).

*	**Risoluzione di Problemi Teorici:** Dettagliate derivazioni analitiche e soluzioni matematiche che affrontano sfide specifiche delle reti di sensori wireless (WSN) e relative efficienze di routing.

## Repository Structure
`challenge_X/src/`: Contiene il codice principale utilizzato per la challenge X.

`challenge_X/docs/`: Include le specifiche/regole per la challenge X.

`challenge_X/deliverables/`: Contiene i file da consegnare per la challenge X.