# ESPHome external components
## [ggreg20_v3] - GGreg20_V3 Geiger counter ready to use ESPHome external component
This is an **external ESPHome component** for the DIY Geiger Counter Module **GGreg20_V3** by **IoT-devices LLC**.

The component simplifies the integration of the GGreg20\_V3 module with any ESP-based device running ESPHome. It moves complex logic—including pulse counting, dead time filtering, dose calculation, and status determination—from YAML into reliable C++.

---
<img width="1105" height="359" alt="image" src="https://github.com/user-attachments/assets/0668fc14-00b6-4000-8b41-ed88c4dfc68e" />

### Local external component config

<img width="1174" height="612" alt="image" src="https://github.com/user-attachments/assets/4247279d-252e-4596-9a03-440f4941e018" />

#### YAML-config for local setup
```yaml
esphome:
  name: sensor-node

external_components:
  - source:
      type: local
      path: ./my_components/
    components: [ggreg20_v3]

ggreg20_v3:
  id: ggreg
  
  # Pin configuration for Active-Low operation (default)
  pin:
    number: GPIO4
    mode: INPUT      # No pullup - GGreg20_V3 manages output
    inverted: true   # Read LOW as logical "1" (active state)
  
  # Interrupt logic: 0 = Active-Low (default), 1 = Active-High
  int_logic: 0
  
  # Measurement settings
  measurement_period: 60    # seconds (minimum 10)
  dead_time_us: 190        # microseconds (0-1000)
  
  # Calibration factors (adjust for your specific sensor)
  dose_power_factor: 0.00378     # CPM to µSv/h conversion for J305
  equivalent_dose_factor: 0.00332 # CPM to equivalent µSv/h conversion for J305

  # Sensor definitions (REQUIRED)
  radiation_power:
    name: "Radiation Power"
  equivalent_dose:
    name: "Radiation Equivalent Dose"
  total_dose:
    name: "Total Accumulated Dose"
  cpm:
    name: "Radiation CPM"
  count:
    name: "Pulse Count"
  status:
    name: "Sensor Status"
```


### Git external component config
#### YAML for GitHub setup
```yaml
esphome:
  name: sensor-node

external_components:
  - source:
      type: git
      url: https://github.com/iotdevicesdev/esphome_external_components 
      ref: main 
    components: [ggreg20_v3] 

ggreg20_v3:
  id: ggreg
  
  # Pin configuration for Active-Low operation (default)
  pin:
    number: GPIO4
    mode: INPUT      # No pullup - GGreg20_V3 manages output
    inverted: true   # Read LOW as logical "1" (active state)
  
  # Interrupt logic: 0 = Active-Low (default), 1 = Active-High
  int_logic: 0
  
  # Measurement settings
  measurement_period: 60    # seconds (minimum 10)
  dead_time_us: 190        # microseconds (0-1000)
  
  # Calibration factors (adjust for your specific sensor)
  dose_power_factor: 0.00378     # CPM to µSv/h conversion for J305
  equivalent_dose_factor: 0.00332 # CPM to equivalent µSv/h conversion for J305

  # Sensor definitions (REQUIRED)
  radiation_power:
    name: "Radiation Power"
  equivalent_dose:
    name: "Radiation Equivalent Dose"
  total_dose:
    name: "Total Accumulated Dose"
  cpm:
    name: "Radiation CPM"
  count:
    name: "Pulse Count"
  status:
    name: "Sensor Status"
```
### Resulting GGreg20_V3 entities in HA 
<img width="1242" height="665" alt="image" src="https://github.com/user-attachments/assets/f67d3c14-e21e-4359-b65f-ef996bd53259" />
