/**
 * \par Copyright (C), 2012-2016, MakeBlock
 * \class   MeBarrierSensor
 * \brief   Driver for MeBarrierSensor module.
 * @file    MeBarrierSensor.h
 * @author  MakeBlock
 * @version V1.0.0
 * @date    2021/03/24
 * @brief   Header for MeBarrierSensor.cpp.
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
 *
 * \par Method List:
 *
 *    1. void MeBarrierSensor::setpin(uint8_t SensorPin)
 *    2. uint8_t MeBarrierSensor::readSensor(void)
 *    3. bool MeBarrierSensor::isBarried(void)
 *
 * \par History:
 * <pre>
 * `<Author>`         `<Time>`        `<Version>`        `<Descr>`
 * huyisi         2021/03/24     1.0.0            build the new.
 * </pre>
 *
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef MeBarrierSensor_H
#define MeBarrierSensor_H

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include <stdbool.h>
#include <Arduino.h>
#include "MeConfig.h"

#ifdef ME_PORT_DEFINED
#include "MePort.h"
#endif // ME_PORT_DEFINED

/* Exported classes ----------------------------------------------------------*/
/**
 * Class: MeBarrierSensor
 * \par Description
 * Declaration of Class MeBarrierSensor.
 */
#ifndef ME_PORT_DEFINED
class MeBarrierSensor
#else // !ME_PORT_DEFINED
class MeBarrierSensor : public MePort
#endif  // !ME_PORT_DEFINED
{
public:

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
 MeBarrierSensor(uint8_t SensorPin);

/**
 * \par Function
 *    setpin
 * \par Description
 *    Reset the limit switch available PIN by its arduino port.
 * \param[in]
 *    switchPin - arduino port for switch detect pin.
 * \par Output
 *    None
 * \par Return
 *    None
 * \par Others
 *    None
 */
  void setpin(uint8_t switchPin);

/**
 * \par Function
 *   readSensor1
 * \par Description
 *   Get the sensors state.
 * \par Output
 *   None
 * \return
 *   0: sensor1 is Barried \n
 *   1: sensor1 is not Barried 
 * \par Others
 *   None
 */
  bool readSensor(void);

/**
 * \par Function
 *   onLine
 * \par Description
 *   Get the sensors state.
 * \par Output
 *   None
 * \return
 *   true: sensor is Barried \n
 *   false: sensor is not Barried
 * \par Others
 *   None
 */
 bool isBarried(void);

private:
  uint8_t _SensorPin;
};
#endif
