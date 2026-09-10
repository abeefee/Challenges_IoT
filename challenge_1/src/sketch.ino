#include <esp_now.h> // Libraries
#include <WiFi.h>

uint8_t broadcastAddr[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // Address of the receiver

esp_now_peer_info_t peerInfo;

#define PIR 4 // PIR sensor pin
#define LDR 34 // LDR sensor pin
#define LDR_POWER 25 // pin used to give power to LDR sensor

#define X 4.6 // Sleep value in seconds
#define C_TIME 1000000 // Conversion value from seconds to microseconds

#define GAMMA 0.7 // Value needed to convert LDR read to lux
#define RL10 50 // Value needed to convert LDR read to lux

int pir_state; // Initialize global variable to be used in getPIRStatus and setup

int getLux(){ // Function to read value from LDR sensor and return value converted to lux
  digitalWrite(LDR_POWER, HIGH); // Turn on the LDR sensor
  int aValue = analogRead(LDR);
  digitalWrite(LDR_POWER, LOW); // Turn off the LDR sensor
  float voltage =  aValue / 4096.0 * 3.3;
  float resistance = 10000.0 * voltage / (3.3 - voltage);
  float lux_f = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1/GAMMA));
  return (int)round(lux_f);
}

String getPIRStatus(){ // Function to read value from PIR and return movement state
  pir_state = digitalRead(PIR);
  if(pir_state == HIGH){
    return "DETECTED";
  } else{
    return "NOT_DETECTED";
  }
}

String getMsgToSend(){ // Function to create message for the SINK
  String msg = "MOTION_";
  msg += getPIRStatus();
  msg += "-LUMINOSITY:";
  msg += getLux();
  return msg;
}

void setup() {
  pinMode(PIR, INPUT); // Set the PIR pin to INPUT
  pinMode(LDR, INPUT); // Set the LDR pin to INPUT
  pinMode(LDR_POWER, OUTPUT); // Set the LDR POWER pin to OUTPUT

  String msg = getMsgToSend(); // Create message to send

  WiFi.mode(WIFI_STA); // Turn on WiFi
  esp_now_init(); // Initialize esp now protocol
  
  memcpy(peerInfo.peer_addr, broadcastAddr, 6); // Set receiver address
  peerInfo.encrypt = false; // Set receiver encryption status
  peerInfo.channel = 0; // Set comunication channel
  esp_now_add_peer(&peerInfo); // Add peer
  
  esp_now_send(broadcastAddr, (uint8_t *)msg.c_str(), msg.length()); // Send message to SINK
  WiFi.mode(WIFI_OFF); // Turn off WiFi
 
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR, !pir_state); // Set the PIR pin as wakeup source
  esp_deep_sleep_start(); // Go to sleep
}

void loop() { // Empty
}