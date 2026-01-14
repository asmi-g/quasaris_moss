#pragma once
#include "performance.h"
#include "stm32g4xx_hal.h"
#include "stm32g474xx.h"

void cycle_counter_init(void)
{
    /* Enable trace and debug blocks */
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;

    /* Reset the cycle counter */
    DWT->CYCCNT = 0;

    /* Enable the cycle counter */
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

uint32_t cycle_counter_get(void)
{
    return DWT->CYCCNT;
}


//Result for test: 376090 cycles
//Results after calculating w/o loop: 493962 cycles