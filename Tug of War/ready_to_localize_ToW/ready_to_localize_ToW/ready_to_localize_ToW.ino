// Please read the ready-to-localize tuturial together with this example.
// https://www.pozyx.io/Documentation/Tutorials/ready_to_localize
/**
  The Pozyx ready to localize tutorial (c) Pozyx Labs

  Please read the tutorial that accompanies this sketch: https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Arduino

  This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
  of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
  parameters and upload this sketch. Watch the coordinates change as you move your device around!
*/
#include <Pozyx.h>
#include <Pozyx_definitions.h>
#include <Wire.h>

////////////////////////////////////////////////
////////////////// PARAMETERS //////////////////
////////////////////////////////////////////////

uint16_t remote_id = 0x611d;                            // set this to the ID of the remote device
bool remote = true;                                    // set this to true to use the remote ID

boolean use_processing = false;                         // set this to true to output data for the processing sketch

const uint8_t num_anchors = 4;                                    // the number of anchors
uint16_t anchors[num_anchors] = {0x605d, 0x604f, 0x6129, 0x6020};     // the network id of the anchors: change these to the network ids of your anchors.
int32_t anchors_x[num_anchors] = {1873, 0, 291, 2617};               // anchor x-coorindates in mm
int32_t anchors_y[num_anchors] = {3745, 0, 6183, 2908};                  // anchor y-coordinates in mm
int32_t heights[num_anchors] = {970, 1660, 1731, 1705};              // anchor z-coordinates in mm

uint8_t algorithm = POZYX_POS_ALG_UWB_ONLY;             // positioning algorithm to use. try POZYX_POS_ALG_TRACKING for fast moving objects.
uint8_t dimension = POZYX_3D;                           // positioning dimension
int32_t height = 1000;                                  // height of device, required in 2.5D positioning

uint32_t last_millis;                 // used to compute the measurement interval in milliseconds 


////////////////////////////////////////////////

void setup(){
  Serial.begin(115200);

  if(Pozyx.begin() == POZYX_FAILURE){
    Serial.println(F("ERROR: Unable to connect to POZYX shield"));
    Serial.println(F("Reset required"));
    delay(100);
    abort();
  }

  if(!remote){
    remote_id = NULL;
  }

//  Serial.println(F("----------POZYX POSITIONING V1.1----------"));
//  Serial.println(F("NOTES:"));
//  Serial.println(F("- No parameters required."));
//  Serial.println();
//  Serial.println(F("- System will auto start anchor configuration"));
//  Serial.println();
//  Serial.println(F("- System will auto start positioning"));
//  Serial.println(F("----------POZYX POSITIONING V1.1----------"));
//  Serial.println();
//  Serial.println(F("Performing manual anchor configuration:"));

  // clear all previous devices in the device list
  Pozyx.clearDevices(remote_id);
  // sets the anchor manually
  setAnchorsManual();
  // sets the positioning algorithm
  Pozyx.setPositionAlgorithm(algorithm, dimension, remote_id);

  printCalibrationResult();
  delay(2000);

//  Serial.println(F("Starting positioning: "));
}

void loop(){
  coordinates_t position;
  int status;
  
     

  sensor_raw_t sensor_raw;
  uint8_t calibration_status = 0;
  int dt;
  dt = millis() - last_millis; 
  last_millis += dt; 
  if(remote){
     status = Pozyx.getRawSensorData(&sensor_raw, remote_id);
     status &= Pozyx.getCalibrationStatus(&calibration_status, remote_id);
    if(status != POZYX_SUCCESS){
      return;
    }
  }else{
    if (Pozyx.waitForFlag(POZYX_INT_STATUS_IMU, 10) == POZYX_SUCCESS){
      Pozyx.getRawSensorData(&sensor_raw);
      Pozyx.getCalibrationStatus(&calibration_status);
    }else{
      uint8_t interrupt_status = 0;
      Pozyx.getInterruptStatus(&interrupt_status);
      return;
    }
  }
  
  if(remote){
    status = Pozyx.doRemotePositioning(remote_id, &position, dimension, height, algorithm);
  }else{
    status = Pozyx.doPositioning(&position, dimension, height, algorithm);
  }

  if (status == POZYX_SUCCESS){
    // prints out the result
    printCoordinates(position);

    // print time difference between last measurement in ms, sensor data, and calibration data
    //Serial.print(dt, DEC);
    Serial.print(",");
    printRawSensorData(sensor_raw);
    Serial.println(",");
    // will be zeros for remote devices as unavailable remotely.
    printCalibrationStatus(calibration_status);
//    Serial.print();

  }else{
    // prints out the error code
    printErrorCode("positioning");
  }
  

  
  

  
}

// prints the coordinates for either humans or for processing
void printCoordinates(coordinates_t coor){
  uint16_t network_id = remote_id;
  if (network_id == NULL){
    network_id = 0;
  }
  if(!use_processing){
//    Serial.print("POS ID 0x");
//    Serial.print(network_id, HEX);
    Serial.print(",");
    Serial.print((coor.x));
    Serial.print(", ");
    Serial.print((coor.y));
    Serial.print(",");
    Serial.print((coor.z));
    Serial.print(",");
    float displacement = sqrt(((coor.x)^2)+((coor.y)^2));
    Serial.print(displacement);
    Serial.print(",");
  }else{
    Serial.print("POS,0x");
    Serial.print(network_id,HEX);
    Serial.print(",");
    Serial.print(coor.x);
    Serial.print(",");
    Serial.print(coor.y);
    Serial.print(",");
    Serial.print(coor.z);
  }
}

// error printing function for debugging
void printErrorCode(String operation){
  uint8_t error_code;
  if (remote_id == NULL){
    Pozyx.getErrorCode(&error_code);
    Serial.print("ERROR ");
    Serial.print(operation);
    Serial.print(", local error code: 0x");
    Serial.println(error_code, HEX);
    return;
  }
  int status = Pozyx.getErrorCode(&error_code, remote_id);
  if(status == POZYX_SUCCESS){
    //Serial.print("ERROR ");
    //Serial.print(operation);
    //Serial.print(" on ID 0x");
    //Serial.print(remote_id, HEX);
    //Serial.print(", error code: 0x");
    //Serial.println(error_code, HEX);
  }else{
    Pozyx.getErrorCode(&error_code);
    //Serial.print("ERROR ");
    //Serial.print(operation);
    //Serial.print(", couldn't retrieve remote error code, local error: 0x");
    //Serial.println(error_code, HEX);
  }
}

// print out the anchor coordinates (also required for the processing sketch)
void printCalibrationResult(){
  uint8_t list_size;
  int status;

  status = Pozyx.getDeviceListSize(&list_size, remote_id);
//  Serial.print("list size: ");
//  Serial.println(status*list_size);

  if(list_size == 0){
    printErrorCode("configuration");
    return;
  }

  uint16_t device_ids[list_size];
  status &= Pozyx.getDeviceIds(device_ids, list_size, remote_id);

//  Serial.println(F("Calibration result:"));
//  Serial.print(F("Anchors found: "));
//  Serial.println(list_size);

  coordinates_t anchor_coor;
  for(int i = 0; i < list_size; i++)
  {
//    Serial.print("ANCHOR,");
//    Serial.print("0x");
//    Serial.print(device_ids[i], HEX);
//    Serial.print(",");
//    Pozyx.getDeviceCoordinates(device_ids[i], &anchor_coor, remote_id);
//    Serial.print(anchor_coor.x);
//    Serial.print(",");
//    Serial.print(anchor_coor.y);
//    Serial.print(",");
//    Serial.println(anchor_coor.z);
  }
}

// function to manually set the anchor coordinates
void setAnchorsManual(){
  for(int i = 0; i < num_anchors; i++){
    device_coordinates_t anchor;
    anchor.network_id = anchors[i];
    anchor.flag = 0x1;
    anchor.pos.x = anchors_x[i];
    anchor.pos.y = anchors_y[i];
    anchor.pos.z = heights[i];
    Pozyx.addDevice(anchor, remote_id);
  }
  if (num_anchors > 4){
    Pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, num_anchors, remote_id);
  }
}





////////
void printRawSensorData(sensor_raw_t sensor_raw){
//  Serial.print(sensor_raw.pressure);
//  Serial.print(",");
  Serial.print(sensor_raw.acceleration[0]);
  Serial.print(",");
  Serial.print(sensor_raw.acceleration[1]);
  Serial.print(",");
  Serial.print(sensor_raw.acceleration[2]);
  Serial.print(",");
  Serial.print(sensor_raw.magnetic[0]);
  Serial.print(",");
  Serial.print(sensor_raw.magnetic[1]);
  Serial.print(",");
  Serial.print(sensor_raw.magnetic[2]);
  Serial.print(",");
  Serial.print(sensor_raw.angular_vel[0]);
  Serial.print(",");
  Serial.print(sensor_raw.angular_vel[1]);
  Serial.print(",");
  Serial.print(sensor_raw.angular_vel[2]);
  Serial.print(",");

  //Euler angles
  float heading= sensor_raw.euler_angles[0]/16.f;
  Serial.print(heading);
  Serial.print(",");
  float roll= (sensor_raw.euler_angles[1]/16.f);
  Serial.print(roll);
  Serial.print(",");
  float pitch=(sensor_raw.euler_angles[2]/16.f);
  Serial.print(pitch);
  Serial.print(", ");
  Serial.print(sensor_raw.quaternion[0]);
  Serial.print(",");
  Serial.print(sensor_raw.quaternion[1]);
  Serial.print(",");
  Serial.print(sensor_raw.quaternion[2]);
  Serial.print(",");
  Serial.print(sensor_raw.quaternion[3]);
  Serial.print(",");
  Serial.print((sensor_raw.linear_acceleration[0]));
  Serial.print(",");
  Serial.print((sensor_raw.linear_acceleration[1]));
  Serial.print(",");
  Serial.print((sensor_raw.linear_acceleration[2]));
  Serial.print(",");
  Serial.print(sensor_raw.gravity_vector[0]);
  Serial.print(",");
  Serial.print(sensor_raw.gravity_vector[1]);
  Serial.print(",");
  Serial.print(sensor_raw.gravity_vector[2]);
  Serial.print(",");
//  Serial.print(sensor_raw.temperature);
//  Serial.print(",");
}

void printCalibrationStatus(uint8_t calibration_status){
//  Serial.print(calibration_status & 0x03);
//  Serial.print(",");
//  Serial.print((calibration_status & 0x0C) >> 2);
//  Serial.print(",");
//  Serial.print((calibration_status & 0x30) >> 4);
//  Serial.print(",");
//  Serial.print((calibration_status & 0xC0) >> 6);  
}
