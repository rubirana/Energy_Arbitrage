# Energy Arbitrage

## Overview
This Python script implements an optimization model for an Energy Management System (EMS), focusing on maximizing economic benefits from battery storage and photovoltaic (PV) energy generation. Utilizing the Pyomo library, the script models daily energy storage, generation, and consumption decisions based on electricity price signals and PV output.

## Features
- **Optimization of Battery Usage:** Determines the optimal charging and discharging schedules of a battery storage system to maximize cost savings.
- **PV Energy Allocation:** Allocates PV energy generation between direct consumption, battery storage, and selling back to the grid.
- **Economic Analysis:** Calculates the net economic benefit of the day’s energy management strategy under varying electricity prices.

## Prerequisites
To run this script, ensure you have the following installed:
- **Python 3.x**
- **Pandas:** For data manipulation and analysis.
- **Numpy:** For numerical calculations.
- **Pyomo:** An open-source software package for formulating and solving optimization problems.
- **Matplotlib:** For plotting results.
- **GLPK (GNU Linear Programming Kit):** As the linear solver.

Install all the required Python packages using the following command:
pip install pandas numpy pyomo matplotlib


## Usage
1. Prepare a CSV file named `sheet.csv` with three columns: `Load`, `Price`, and `PV`, representing the hourly load demand, electricity price, and PV generation.
2. Run the script using the command below:
python energy_management_system.py


### The script outputs:
- Optimal battery charging and discharging schedules.
- Allocation of PV energy.
- Economic analysis of the energy management strategy.
- A PDF file named `industry.pdf` with a graphical representation of the results.

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details [here](https://www.gnu.org/licenses/).


## Contact
For any questions or suggestions, please contact [rubi.rana@sintef.no](mailto:rubi.rana@sintef.no).
