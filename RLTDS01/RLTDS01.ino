#include <Arduino.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include <BH1750.h>
#include "Adafruit_Si7021.h"

//TDS METER 
#define TdsSensorPin A4
#define VREF 5.0      // analog reference voltage(Volt) of the ADC
#define SCOUNT  10 
int analogBuffer[SCOUNT];    // store the analog value in the array, read from ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0,copyIndex = 0;
float averageVoltage = 0,tdsValue = 0,temperature = 25;

int value_TDS(){
   static unsigned long analogSampleTimepoint = millis();
   if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
   {
     analogSampleTimepoint = millis();
     analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin);    //read the analog value and store into the buffer
     analogBufferIndex++;
     if(analogBufferIndex == SCOUNT) 
         analogBufferIndex = 0;
   }   
   static unsigned long printTimepoint = millis();
   if(millis()-printTimepoint > 800U)
   {
      printTimepoint = millis();
      for(copyIndex=0;copyIndex<SCOUNT;copyIndex++)
        analogBufferTemp[copyIndex]= analogBuffer[copyIndex];
      averageVoltage = getMedianNum(analogBufferTemp,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
      float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
      float compensationVolatge=averageVoltage/compensationCoefficient;  //temperature compensation
      tdsValue=(133.42*compensationVolatge*compensationVolatge*compensationVolatge - 255.86*compensationVolatge*compensationVolatge + 857.39*compensationVolatge)*0.5; //convert voltage value to tds value
      //Serial.print("voltage:");
      //Serial.print(averageVoltage,2);
      //Serial.print("V   ");
      
   }
   return tdsValue;
}

#if defined(UBRRH) || defined(UBRR0H)
  extern HardwareSerial Serial;
  #define HAVE_HWSERIAL0
#endif

//Not modified
enum node_type {
  RLACS = 0,
  RLTDS = 1,
  THL = 2
};

//Modified
//ID and Type Node
#define ID_NODE             01
#define NODE                RLTDS
//#define DEBUG

//Hardware of RLACS Node
#define PIN_D1              2
#define PIN_D2              3
#define PIN_A1              A2
#define PIN_A2              A3
//Hardware of RLTDS Node
#define PIN_D               4
#define PIN_TDS             A4
//Hardware of THL Node
//None

#define ID_NODE_LENGTH      2

//Length and string of type node
char node_name_str[3][5] = {{'R','L','A','C','S'},
                            {'R','L','T','D','S'},
                            {'T','H','L',' ',' '}};
unsigned char node_name_str_length[3] = {5,5,3};

//Length and String of command
#define TESTCONNECT_LEN     11
char command_testConnect[TESTCONNECT_LEN] = {'T','E','S','T','C','O','N','N','E','C','T'};
#define GETDATA_LEN         7
char command_getData[GETDATA_LEN] = {'G','E','T','D','A','T','A'};
#define UPDATEDATA_LEN      10
char command_updatedata[UPDATEDATA_LEN] = {'U','P','D','A','T','E','D','A','T','A'};

//Variable for rec data from UART
char rec[200];
unsigned int index_rec = 0;

//Create SI7021 Sensor (Humidity and temp sensor)
Adafruit_Si7021 Humidity_Temp_Sensor = Adafruit_Si7021();
//Create BH1750 Sensor (Light meter)
BH1750 Light_Sensor;   

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(TdsSensorPin,INPUT);
  
  //Config Hardware for node
  switch(NODE){
    case RLTDS:{      
      pinMode(PIN_D, OUTPUT);         
      break;
    }
    case RLACS:{
      pinMode(PIN_D1, OUTPUT);
      pinMode(PIN_D2, OUTPUT);
      break;
    }
    case THL:{
      while (Humidity_Temp_Sensor.begin() != true){
        #ifdef DEBUG
          Serial.println("SETUP-Not Init SI7021 - Humidity and Temp Sensor");
        #endif
      } 
      while(Light_Sensor.begin() != true){
        #ifdef DEBUG
          Serial.println("SETUP-Not Init BH1750 - Light Sensor");
        #endif
      }
      break;
    }
  }
}

void loop() {
  
  
}

//Process Check-Connect command from sever
//Format data: NODEID-CHECKCONNECT
void CheckConnect(){
  int j;
  //Calculate Length of String Receive 
  int len = TESTCONNECT_LEN + ID_NODE_LENGTH + node_name_str_length[NODE] + 1;  //1 space '_' in str receive

  #ifdef DEBUG
    Serial.println("CHECK_CONNECT");
  #endif

  int index_temp;
  //Check String "TestConnect" command of string receive
  for(j = TESTCONNECT_LEN; j > 0; j--){        
    index_temp = index_rec - TESTCONNECT_LEN + j - 1;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    if(rec[index_temp] != command_testConnect[j - 1]){ //Compare
      #ifdef DEBUG 
        Serial.println("CHECK_CONNECT-ERROR-Command Incorect");
      #endif
      return;
    }
  }
  
  //Check Name of Node on string receive, if different then return
  for(j = node_name_str_length[NODE]; j > 0; j--){    
    index_temp = index_rec - len + j - 1;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    if(rec[index_temp] != node_name_str[NODE][j - 1]){   //Check character of string receive vs node name string
      #ifdef DEBUG 
        Serial.println("CHECK_CONNECT-ERROR-Node Name Incorect");
      #endif
      return;
    } 
  }

  //Check ID Node Number of node
  int node_index_temp = 0;    //init id node index data  
  //Calculate id Node number from string
  for(j = 0; j < ID_NODE_LENGTH > 0; j++){
    index_temp = index_rec - len + node_name_str_length[NODE] + j;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    node_index_temp = node_index_temp*10 + rec[index_temp] - 48;    
  }    
  //Compare ID Number from String receive vs ID Node(Setup)
  if(node_index_temp != ID_NODE){
    #ifdef DEBUG 
      Serial.println("CHECK_CONNECT-ERROR-IDNode Incorect");
    #endif
    return;
  }

  //OK, GetData Command correct. Now get data and Transfer data to sever  
  //Transfer String response 
  /*Format:
      NODEID_DATA_D1_(ON/OFF)_D2_(ON/OFF)_A1_(int)_A2_(int)     
  */
  //Transfer Node name
  for(j = 0; j < 5; j++){
    if(node_name_str[NODE][j] == ' '){            //Break when array is null
      break;
    }
    Serial.print(node_name_str[NODE][j]);    
  }
  String IDN = "";
  if(ID_NODE < 10){
    //Serial.print("0");
    IDN = "0";
  }
  String response =  IDN + String(ID_NODE) + "_" + "CONNECT" + "_" + "OK";
  Serial.println(response);
  #ifdef DEBUG
    Serial.println("CHECK_CONNECT OK - End Function");
  #endif

  
  
  
}

//Process Get-Data command from sever
//Format data: NODEID-GETDATA
void GetData(){
  int j;
  //Calculate Length of String Receive 
  int len = GETDATA_LEN + ID_NODE_LENGTH + node_name_str_length[NODE] + 1;  //1 space '_'  in str receive

  #ifdef DEBUG
    Serial.println("GETDATA");
  #endif

  //Check String "GetData" command of string receive
  int index_temp;
  for(j = GETDATA_LEN; j > 0; j--){    
    index_temp = index_rec - GETDATA_LEN + j - 1;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    if(rec[index_temp] != command_getData[j - 1]){ //Compare
      #ifdef DEBUG 
        Serial.println("Error-GetData-Command Incorect");
      #endif
      return;
    }
  }
  
  //Check Name of Node on string receive, if different then return
  for(j = node_name_str_length[NODE]; j > 0; j--){    
    index_temp = index_rec - len + j - 1;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    if(rec[index_temp] != node_name_str[NODE][j - 1]){   //Check character of string receive vs node name string
      #ifdef DEBUG 
        Serial.println("Error-GetData-Node Name Incorect");
      #endif
      return;
    }   
  }

  //Check ID Node Number of node
  int node_index_temp = 0;    //init id node index data  
  //Calculate id Node number from string
  for(j = 0; j < ID_NODE_LENGTH > 0; j++){
    index_temp = index_rec - len + node_name_str_length[NODE] + j;
    if(index_temp < 0){
      index_temp = index_temp + 200;
    }
    node_index_temp = node_index_temp*10 + rec[index_temp] - 48;    
  }  
  
  //Compare ID Number from String receive vs ID Node(Setup)
  if(node_index_temp != ID_NODE){
    #ifdef DEBUG 
      Serial.println("Error-GetData-IDNode Incorect");
    #endif
    return;
  }

  //OK, GetData Command correct. Now get data and Transfer data to sever  
  //Transfer String response 
  /*Format:
      RLACS: NODEID_DATA_D1_(ON/OFF)_D2_(ON/OFF)_A1_(int)_A2_(int)
      RLTDS: NODEID_DATA_D_(ON/OFF)_TDS_(int)
      THL:   NODEID_DATA_T_(int)_H_(int)_L_(int)
  */
  //Transfer Node name
  String data_send = "";
  for(j = 0; j < 5; j++){
    if(node_name_str[NODE][j] == ' '){        //Break when array is null
      break;
    }
    //Serial.print(node_name_str[NODE][j]);    
    data_send += node_name_str[NODE][j];
  }
  
  if(ID_NODE < 10){
    //Serial.print("0"); 
    data_send += "0"; 
  }
  data_send += String(ID_NODE);
  data_send += "_DATA_";
  //Transfer data of each node
  switch(NODE){
    case RLACS:{                              //RLACS Node Type
      //Get and transfer D1 data
      data_send += "D1_";
      if(digitalRead(PIN_D1) == HIGH){
        data_send += "ON_";  
      }
      else{
        data_send += "OFF_";
      }
      //Get and transfer D2 data
      data_send += "D2_";
      if(digitalRead(PIN_D2) == HIGH){
        data_send += "ON_";
      }
      else{
        data_send += "OFF_";
      }
      //Get and transfer A1, A2 data
 
      data_send += "A1_";
      data_send += String(analogRead(PIN_A1));
      data_send += "_A2_";
      data_send += String(analogRead(PIN_A2));
      break;
    }
    case RLTDS:{                              //RLTDS Node Type
      //Get and transfer D data
      data_send += "D_";
      if(digitalRead(PIN_D) == HIGH){

        data_send += "ON_";
      }
      else{

        data_send += "OFF_";
      }
      //Get and transfer TDS data
      data_send += "TDS_";
      //data_send += String(analogRead(PIN_TDS));
      data_send += String(value_TDS());
      break;
    }    
    case THL:{                              //THL Node Type
      //Get and transfer Temp data
      data_send += "T_";
      data_send += String(int(Humidity_Temp_Sensor.readTemperature()));
      data_send += "_H_";
      data_send += String(int(Humidity_Temp_Sensor.readHumidity()));
      data_send += "_L_";
      data_send += String(int(Light_Sensor.readLightLevel()));
      break;
    }    
  }
  Serial.println(data_send);                   //End of transfer

  #ifdef DEBUG
    Serial.println("GETDATA OK - End Function");
  #endif
}

//Process Update-Data command from sever
//Format data: NODEID-UPDATEDATA-PIN-STATUS
void UpdateData(){
  int j, len, len_status_str, len_pin_str;
  #ifdef DEBUG
    Serial.println("UPDATEDATA");
  #endif

  //Get Status Data Update to calculate length of status from string receive
  int index_temp1, index_temp2, index_temp3;
  index_temp1 = index_rec - 1;
  index_temp2 = index_rec - 2;
  index_temp3 = index_rec - 3;
  if(index_temp1 < 0){
    index_temp1 = 200 + index_temp1;
  }
  if(index_temp2 < 0){
    index_temp2 = 200 + index_temp2;
  }
  if(index_temp3 < 0){
    index_temp3 = 200 + index_temp3;
  }
  if((rec[index_temp2] == 'O')&&(rec[index_temp1] == 'N')){
    //Calculate Length of String Receive
    len_status_str = 2;     //Length of 'ON' string     
  }
  else{
    if((rec[index_temp3] == 'O')&&(rec[index_temp2] == 'F')&&(rec[index_temp1] == 'F')){
      //Calculate Length of String Receive
      len_status_str = 3;     //Length of status 'OFF' string        
    }
    else{
      #ifdef DEBUG 
        Serial.println("UPDATEDATA-ERROR-Not Detect Status PIN");
      #endif
      return;
    }
  }

  //Get length of pin str on string receive
  index_temp1 = index_rec - 4 - len_status_str;
  index_temp2 = index_rec - 3 - len_status_str;
  if(index_temp1 < 0){                            //Calib index data if over array index
    index_temp1 = index_temp1 + 200;
  }
  if(index_temp2 < 0){                            //Calib index data if over array index
    index_temp2 = index_temp2 + 200;
  }

  if(rec[index_temp1] == '_'){
    len_pin_str = 2;
  }
  else{
    if(rec[index_temp2] == '_'){
      len_pin_str = 1;
    }
    else{
      #ifdef DEBUG 
        Serial.println("UPDATEDATA-ERROR-Not Detect PIN");
      #endif
      return;
    }
  }

  //Check fomated of pin
  index_temp1 = index_rec - len_status_str - 1 - len_pin_str;
  if(index_temp1 < 0){                            //Calib index data if over array index
    index_temp1 = index_temp1 + 200;
  }
  if(rec[index_temp1] != 'D'){
    #ifdef DEBUG 
      Serial.println("UPDATEDATA-ERROR-PIN unformatted");
    #endif
    return;
  }

  //Calculate length of string receive from uart
  len = UPDATEDATA_LEN + ID_NODE_LENGTH + node_name_str_length[NODE] + 3 + len_pin_str + len_status_str;  //3 space '_'  in str receive

  

  //Check String "UpdateData" command of string receive
  for(j = UPDATEDATA_LEN; j > 0; j--){ 
    index_temp1 = index_rec - UPDATEDATA_LEN + j - 1 - len_pin_str - len_status_str - 2;
    if(index_temp1 < 0){                          //Calib index data if over array index
      index_temp1 = index_temp1 + 200;
    }     
    if(rec[index_temp1] != command_updatedata[j - 1]){ //Compare     //2 space '_' in str receive
      #ifdef DEBUG 
        Serial.println("UPDATEDATA-ERROR-Command Incorect");
      #endif
      return;
    }
  }

  //Check Name of Node on string receive, if different then return
  for(j = node_name_str_length[NODE]; j > 0; j--){
    index_temp1 = index_rec - len + j - 1;
    if(index_temp1 < 0){                          //Calib index data if over array index
      index_temp1 = index_temp1 + 200;
    } 
    if(rec[index_temp1] != node_name_str[NODE][j - 1]){   //Check character of string receive vs node name string
      #ifdef DEBUG 
        Serial.println("UPDATEDATA-ERROR-Node Name Incorect");
      #endif
      return;
    }
  }

  //Check ID Node Number of node
  int node_index_temp = 0;    //init id node index data  
  //Calculate id Node number from string
  for(j = 0; j < ID_NODE_LENGTH > 0; j++){
    index_temp1 = index_rec - len + node_name_str_length[NODE] + j;
    if(index_temp1 < 0){
      index_temp1 = index_temp1 + 200;
    }
    node_index_temp = node_index_temp*10 + rec[index_temp1] - 48;    
  }  
  
  //Compare ID Number from String receive vs ID Node(Setup)
  if(node_index_temp != ID_NODE){
    #ifdef DEBUG 
      Serial.println("UPDATEDATA-ERROR-IDNode Incorect");
    #endif
    return;
  }
  String data_send = "";
  //OK, UpdateData Command correct. Now update data and Transfer data to sever  
  //Update Data
  switch(NODE){
    case RLACS:{
      if(len_pin_str != 2){
        #ifdef DEBUG
          Serial.println("UPDATEDATA-ERROR-Pin in node unformatted 1");
        #endif
        return;
      }
      index_temp1 = index_rec - len_status_str - 1 - 1;
      if(index_temp1 < 0){
        index_temp1 = index_temp1 + 200;
      }
      if(rec[index_temp1] == '1'){
        if(len_status_str == 3){
          digitalWrite(PIN_D1, LOW);          
        }
        else{
          digitalWrite(PIN_D1, HIGH);
        }
      }
      else{
        if(rec[index_temp1] == '2'){
          if(len_status_str == 3){
            digitalWrite(PIN_D2, LOW);          
          }
          else{
            digitalWrite(PIN_D2, HIGH);
          }
        }
        else{
          #ifdef DEBUG
            Serial.println("UPDATEDATA-ERROR-Pin in node unformatted 2 ");
          #endif
          return;
        }
      }
      break;
    }
    case RLTDS:{
      //Serial.println(len_pin_str);
      if(len_pin_str != 1){
        #ifdef DEBUG
          Serial.println("UPDATEDATA-ERROR-Pin in node unformatted 3");
        #endif
        return;
      }
      
        if(len_status_str == 3){
          digitalWrite(PIN_D, LOW);          
        }
        else{
          digitalWrite(PIN_D, HIGH);
        }
        
      

      break;
    }
    case THL:{
      #ifdef DEBUG
        Serial.println("UPDATEDATA-ERROR-THL Node not update Data");
      #endif
      return;
      break;
    }
  }
  //Transfer String response 
  /*Format:
      NODEID_UPDATE_PIN_STATUS
  */
  //Transfer Node name
  for(j = 0; j < 5; j++){
    if(node_name_str[NODE][j] == ' '){          //Break when array is null
      break;
    }
    data_send += node_name_str[NODE][j];
     
  }
  if(ID_NODE < 10){
    data_send += "0";
  }
  data_send += String(ID_NODE);
  data_send += "_UPDATE_";

  index_temp1 = index_rec - len_status_str - 1 - len_pin_str;
  if(index_temp1 < 0){
    index_temp1 = index_temp1 + 200;
  }
  data_send += (rec[index_temp1]);    //1 space '_' on string         
  if(len_pin_str == 2){     //If pin = D2,D1 and not if pin = D
    index_temp1 = index_rec - len_status_str - 1 - len_pin_str + 1;
    if(index_temp1 >= 200){
      index_temp1 = index_temp1 - 200;
    }
  data_send += (rec[index_temp1]);    //1 space '_' on string     //Transfer digit of pin
  }
  data_send += "_OK";
  Serial.println(data_send);                           //End of transfer
  //Transfer data of each node
  #ifdef DEBUG
    Serial.println("UPDATEDATA-OK-End Function");
  #endif

 
}
void serialEvent() {
  while (Serial.available()) {    
    char inChar = (char)Serial.read();
    rec[index_rec] = inChar;
    if(rec[index_rec] == '\n'){
      CheckConnect();
      GetData();
      UpdateData();
    }
    index_rec++;    
    if(index_rec == 200) index_rec = 0;
    //Serial.print(inChar);
  }
}

int getMedianNum(int bArray[], int iFilterLen) 
{
      int bTab[iFilterLen];
      for (byte i = 0; i<iFilterLen; i++)
    bTab[i] = bArray[i];
      int i, j, bTemp;
      for (j = 0; j < iFilterLen - 1; j++) 
      {
    for (i = 0; i < iFilterLen - j - 1; i++) 
          {
      if (bTab[i] > bTab[i + 1]) 
            {
    bTemp = bTab[i];
          bTab[i] = bTab[i + 1];
    bTab[i + 1] = bTemp;
       }
    }
      }
      if ((iFilterLen & 1) > 0)
  bTemp = bTab[(iFilterLen - 1) / 2];
      else
  bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
      return bTemp;
}
