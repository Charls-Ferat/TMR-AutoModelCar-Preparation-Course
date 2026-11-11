/**
 * \par Copyright (C), 2012-2016, MakeBlock
 * \class MeCollisionSensor
 * \brief   Driver for Me line follwer device.
 * @file    MeCollisionSensor.cpp
 * @author  MakeBlock
 * @version V1.0.0
 * @date    2021/03/24
 * @brief   Driver for Me line follwer device.
 *
 * \par Copyright
 * This software is Copyright (C), 2012-2016, MakeBlock. Use is subject to license \n
 * conditions. The main licensing options available are GPL V2 or Commercial: \n
 *
 * \par Open Source Licensing GPL V2
 * This is the appropriate option if you want to share the source code of your \n
 * application with everyone you distribute it to, and you also want to give them \n
 * the right to share who uses it. If you wish to use this software under Open \n
 * Source Licensing, you must contribute all your source code to the open source \n
 * community in accordance with the GPL Version 2 when your application is \n
 * distributed. See http://www.gnu.org/copyleft/gpl.html
 *
 * \par Description
 * This file is a drive for Me line follwer device, It supports line follwer device
 * V2.2 provided by the MakeBlock. The line follwer used Infrared Tube to Use infrared
 * receiver and transmitter to detect the black line.
 *
 * \par Method List:
 *
 *    1. void MeCollisionSensor::setpin(uint8_t SensorPin)
 *    2. uint8_t MeCollisionSensor::readSensor(void)
 *    3. bool MeCollisionSensor::isCollision(void)
 *
 * \par History:
 * <pre>
 * `<Author>`         `<Time>`        `<Version>`        `<Descr>`
 * huyisi         2021/03/24     1.0.0            build the new.
 * </pre>
 *
 * @example LineFollowerTest.ino
 */

#include "MeCollisionSensor.h"


/**
 * \par Function
 *   setpin
 * \par Description
 *   Reset the line follwer device available PIN by its arduino port.
 * \param[in]
 *   SensorPin - arduino port(should digital pin)
 * \par Output
 *   None
 * \return
 *   None
 * \par Others
 *   None
 */
MeCollisionSensor::MeCollisionSensor(uint8_t SensorPin)
{
  _SensorPin = SensorPin;
  pinMode(_SensorPin,INPUT);
}


/**
 * \par Function
 *   setpin
 * \par Description
 *   Reset the line follwer device available PIN by its arduino port.
 * \param[in]
 *   SensorPin - arduino port(should digital pin)
 * \par Output
 *   None
 * \return
 *   None
 * \par Others
 *   None
 */
void MeCollisionSensor::setpin(uint8_t SensorPin)
{
  _SensorPin = SensorPin;
  pinMode(_SensorPin,INPUT);
}

/**
 * \par Function
 *   readSensor1
 * \par Description
 *   Get the sensors state.
 * \par Output
 *   None
 * \return
 *   0: sensor is Collision \n
 *   1: sensor is not Collision
 * \par Others
 *   None
 */
bool MeCollisionSensor::readSensor(void)
{
  return digitalRead(_SensorPin);
}

/**
 * \par Function
 *   onLine
 * \par Description
 *   Get the sensors state.
 * \par Output
 *   None
 * \return
 *   true: sensor is Collision \n
 *   false: sensor is not Collision
 * \par Others
 *   None
 */
bool MeCollisionSensor::isCollision(void)
{
  if(digitalRead(_SensorPin))
  {
    return false;
  }
  else
  {
    return true;
  }
}


