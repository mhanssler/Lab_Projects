import pvlib
from pvlib import location, solarposition, irradiance
from pvlib.location import Location
from pvlib.pvsystem import PVSystem #type: ignore
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt


# to simulate the sun's position at a specific location and time, it is critical to compute the solar zenith and azimuth angles
my_location = Location(latitude=37.68778985250586,longitude=-122.08102280311628, tz ='America/Los_Angeles',altitude=10, name='Castro Valley')

#create a time range for the simulation
time_range = pd.date_range(start='2024-09-28', end='2024-09-30', freq='1h', tz=my_location.tz)

#Get the solar position data
solar_position = my_location.get_solarposition(time_range)

#clear sky apparent GHI (Global Horizontal Irradiance) data, dni (Direct Normal Irradiance) and dhi (Diffuse Horizontal Irradiance) data
clear_sky = my_location.get_clearsky(time_range)
clear_sky = clear_sky.where(solar_position['apparent_zenith'] <= 90, 0)

print(solar_position[['apparent_zenith', 'azimuth']], clear_sky[['ghi', 'dni', 'dhi']])

#model my system 15 panels total
system = PVSystem(module_parameters = {'pac0': 240},
                    inverter_parameters= {'pac0': 240},
                    temperature_model_parameters= TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass'])

model_chain = ModelChain(system, location=my_location)
model_chain.run_model(times=time_range, weather=clear_sky)

#Plot the solar position data
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
axs[0].plot(solar_position.index, solar_position['apparent_zenith'], label='Solar Zenith Angle', color='r')
axs[0].set_ylabel('Solar Zenith Angle [degrees]')
axs[0].set_title('Solar Apparent Zenith')
axs[0].legend()
axs[1].plot(solar_position.index, solar_position['azimuth'], label='Solar Azimuth Angle', color='b')
axs[1].set_ylabel('Solar Azimuth Angle [degrees]')
axs[1].set_title('Solar Azimuth')
axs[1].legend()
axs[2].plot(clear_sky.index, clear_sky['ghi'], label='Clear Sky GHI', color='g')
axs[2].set_ylabel('Irradiance [W/m^2]')
axs[2].set_title('Clear Sky GHI')
axs[2].legend()
plt.show()

fig2, axs2 = plt.subplots(3, 1, figsize=(10, 8))
axs2[0].model_chain.ac.plot()
axs2[0].set_ylabel('AC Power [W]')
axs2[0].set_title('AC Power')
axs2[0].legend()
plt.show()
