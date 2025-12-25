#include "stm32g4xx_hal.h"
#include <stdio.h>
#include <string.h>   

extern FILE* torque_file;

HAL_StatusTypeDef HAL_CAN_AddTxMessage(
    FDCAN_HandleTypeDef *hcan,
    FDCAN_TxHeaderTypeDef *pHeader,
    uint8_t aData[],
    uint32_t *pTxMailbox)
{
    float tx;
    memcpy(&tx, aData, sizeof(float));   // wheel torque command

    fprintf(torque_file, "%f\n", tx);
    fflush(torque_file);

    // pretend message sent
    *pTxMailbox = 0;
    return HAL_OK;
}
