from interaction_package import *
paramters = {
    "rho": 0.3,
    "dt": 0.01,
    "ngrx": 1000,
    "temperatura": 0.6,
    "pasos": 20,
    "print": 1,
}
system = gas(paramters["ngrx"],
             paramters["temperatura"],
             paramters["rho"],
             paramters["dt"],
             paramters["pasos"],
             paramters["print"])
system.init_system()
system.simulation()
