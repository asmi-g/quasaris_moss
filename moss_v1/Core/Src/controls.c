#include <math.h>
#include "controls.h"
#include "performance.h"
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

    print_double("Computed Δv1", burns.delta_v1, "m/s \n");
    print_double("Computed Δv2", burns.delta_v2, "m/s \n");
    print_double("Time of flight", burns.time_of_flight, "s \n");

    return burns;
}

double simulated_accelerometer(void)
{
    // m/s^2, constant thrust model for now
    return 0.005;   // static small satellite acceleration for simplicity of this prototype
}

void perform_burn(double target_delta_v) {
    double measured_delta_v = 0.0;
    double dt = 0.1;

    print_double("Starting burn for target delta-v", target_delta_v, "m/s \n");

    uint32_t initial_cycles_per_iteration = cycle_counter_get();
    while (measured_delta_v < target_delta_v) {
        double measured_accel = simulated_accelerometer(); // m/s^2
        measured_delta_v += measured_accel * dt; // Uncomment for real time simulation
        //measured_delta_v = target_delta_v; // Uncomment to test to check loop performance
        //HAL_Delay((int)(dt * 1000)/SIM_TIME_SCALE); // Scale delay to speed up simulation, Uncomment for real time simulation
        //uint32_t cycles = cycle_counter_get() - initial_cycles_per_iteration; // Uncomment to test to check loop performance
        //printf("cycles per loop iteration = %lu\r\n", cycles); // Uncomment to test to check loop performance
        print_double("Measured delta v", measured_delta_v, "m/s \n");
    }

    print_double("Burn complete for delta-v", measured_delta_v, "m/s \n");
}

double compute_burn_time(double target_delta_v){
    double accel = simulated_accelerometer(); // m/s^2
    return target_delta_v / accel;             // seconds
}

void execute_hohmann_transfer(double current_radius, double target_radius) {
    HohmannBurns_t burns = compute_hohmann_burns(current_radius, target_radius);

    print_double("Delta-v1", burns.delta_v1, "m/s \n");
    print_double("Delta-v2", burns.delta_v2, "m/s \n");
    print_double("Time of flight", burns.time_of_flight, "s \n");

    //perform_burn(burns.delta_v1);
    double burn1_time = compute_burn_time(burns.delta_v1);
    print_double("Burn 1 Time", burn1_time, "s \n");
    print_double("Number of loop iterations required for Burn 1", burns.delta_v1 / (simulated_accelerometer() * 0.1), " \n"); //where 0.1 is dt in perform_burn
    double burn2_time = compute_burn_time(burns.delta_v2);
    print_double("Burn 2 Time", burn2_time, "s \n");
    print_double("Number of loop iterations required for Burn 2", burns.delta_v2 / (simulated_accelerometer() * 0.1), " \n"); //where 0.1 is dt in perform_burn
    print_double("Total Loop Iterations for both Transfer Burns", (burns.delta_v1 + burns.delta_v2) / (simulated_accelerometer() * 0.1), " \n");
    print_double("Total Transfer Time", burn1_time + burns.time_of_flight + burn2_time, "s \n");
    //HAL_Delay((int)(burns.time_of_flight * 1000));
    perform_burn(burns.delta_v1);
    //perform_burn(burns.delta_v2);
}

