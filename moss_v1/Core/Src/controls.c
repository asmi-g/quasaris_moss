#include <math.h>
#include "controls.h"
#include <string.h>
#include <stdio.h>
#include "stm32g4xx_hal.h"
#include "stm32g474xx.h"


void print_double(const char* label, double value, const char* units) {
    char buffer[32];
    sprintf(buffer, "%.3f", value);  // 3 decimal places
    printf("%s: %s %s\n", label, buffer, units);
}

HohmannBurns_t compute_hohmann_burns(double r1, double r2) {
    HohmannBurns_t burns;
    
    double a_t = (r1 + r2) / 2.0;
    burns.time_of_flight = M_PI * sqrt(pow(a_t, 3) / MU);

    double v_circ1 = sqrt(MU / r1);
    double v_trans1 = sqrt(MU * ((2.0 / r1) - (1.0 / a_t)));
    burns.delta_v1 = v_trans1 - v_circ1;

    double v_circ2 = sqrt(MU / r2);
    double v_trans2 = sqrt(MU * ((2.0 / r2) - (1.0 / a_t)));
    burns.delta_v2 = v_circ2 - v_trans2;

    print_double("Computed Δv1", burns.delta_v1, "m/s");
    print_double("Computed Δv2", burns.delta_v2, "m/s");
    print_double("Time of flight", burns.time_of_flight, "s");

    return burns;
}

void perform_burn(double target_delta_v) {
    double measured_delta_v = 0.0;
    double dt = 0.1;

    print_double("Starting burn for target delta-v", target_delta_v, "m/s");

    while (measured_delta_v < target_delta_v) {
        measured_delta_v += 0.01;
        HAL_Delay((int)(dt * 1000));
    }

    print_double("Burn complete for delta-v", target_delta_v, "m/s");
}

void execute_hohmann_transfer(double current_radius, double target_radius) {
    HohmannBurns_t burns = compute_hohmann_burns(current_radius, target_radius);

    print_double("Delta-v1", burns.delta_v1, "m/s");
    print_double("Delta-v2", burns.delta_v2, "m/s");
    print_double("Time of flight", burns.time_of_flight, "s");

    perform_burn(burns.delta_v1);
    HAL_Delay((int)(burns.time_of_flight * 1000));
    perform_burn(burns.delta_v2);
}

