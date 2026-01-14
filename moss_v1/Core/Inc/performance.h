#pragma once

#include "stm32g4xx_hal.h"
#include "stm32g474xx.h"

void cycle_counter_init(void);
uint32_t cycle_counter_get(void);