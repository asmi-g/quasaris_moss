#include "stm32g4xx_hal.h"
#include <stdio.h>
#include <string.h>

extern FILE* imu_file;
#define REG_ACCEL 0x00   // Placeholder until IMU conversion further defined
#define REG_GYRO  0x01


HAL_StatusTypeDef HAL_I2C_Mem_Read_Fake(
    I2C_HandleTypeDef *hi2c,
    uint16_t DevAddress,
    uint16_t MemAddress,
    uint16_t MemAddSize,
    uint8_t *pData,
    uint16_t Size,
    uint32_t Timeout)
{
    // Example IMU row: ax, ay, az, gx, gy, gz
    static float ax, ay, az, gx, gy, gz;

    fscanf(imu_file, "%f,%f,%f,%f,%f,%f",
       &ax,&ay,&az,&gx,&gy,&gz);

    // Fill buffer based on what register the code is asking for
    if (MemAddress == REG_ACCEL) {
        memcpy(pData, &ax, sizeof(float)*3);
    }
    else if (MemAddress == REG_GYRO) {
        memcpy(pData, &gx, sizeof(float)*3);
    }

    return HAL_OK;
}
