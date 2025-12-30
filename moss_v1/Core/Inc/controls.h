
// Source - https://stackoverflow.com/a
// Posted by Hemant Gangwar, modified by community. See post 'Timeline' for change history
// Retrieved 2025-12-30, License - CC BY-SA 4.0
#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif

#define G 6.67430e-11
#define M_EARTH 5.9742e24
#define MU (G * M_EARTH)

typedef struct {
    double delta_v1;
    double delta_v2;
    double time_of_flight;
} HohmannBurns_t;

HohmannBurns_t compute_hohmann_burns(double r1, double r2);
void perform_burn(double target_delta_v);
void execute_hohmann_transfer(double current_radius, double target_radius);
