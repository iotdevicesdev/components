from esphome import pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, text_sensor
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_NAME,
    ICON_GAUGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

AUTO_LOAD = ["sensor", "text_sensor"]
MULTI_CONF = True

# Custom units and icons
UNIT_MICROSIEVERT_PER_HOUR = "µSv/h"
UNIT_MICROSIEVERT = "µSv"
UNIT_COUNTS_PER_MINUTE = "cpm"
ICON_RADIATION = "mdi:radioactive"

# Define the C++ namespace/classes
ggreg20_v3_ns = cg.esphome_ns.namespace("ggreg20_v3")
GGreg20V3Component = ggreg20_v3_ns.class_("GGreg20V3Component", cg.Component)

# Sensor classes
DosePowerSensor = ggreg20_v3_ns.class_("DosePowerSensor", sensor.Sensor)
EquivDoseSensor = ggreg20_v3_ns.class_("EquivDoseSensor", sensor.Sensor)
TotalDoseSensor = ggreg20_v3_ns.class_("TotalDoseSensor", sensor.Sensor)
CPMSensor = ggreg20_v3_ns.class_("CPMSensor", sensor.Sensor)
CountSensor = ggreg20_v3_ns.class_("CountSensor", sensor.Sensor)
StatusSensor = ggreg20_v3_ns.class_("StatusSensor", text_sensor.TextSensor)


# Custom constants
CONF_RADIATION_POWER = "radiation_power"
CONF_EQUIVALENT_DOSE = "equivalent_dose"
CONF_TOTAL_DOSE = "total_dose"
CONF_CPM = "cpm"
CONF_COUNT = "count"
CONF_STATUS = "status"
CONF_DOSE_POWER_FACTOR = "dose_power_factor"
CONF_EQUIV_DOSE_FACTOR = "equivalent_dose_factor"
CONF_DEAD_TIME_US = "dead_time_us"
CONF_MEASUREMENT_PERIOD = "measurement_period"
CONF_INT_LOGIC = "int_logic"


# Schemas for individual sensors
DOSE_POWER_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_MICROSIEVERT_PER_HOUR,
    icon=ICON_GAUGE,
    accuracy_decimals=3,
    state_class=STATE_CLASS_MEASUREMENT,
).extend({cv.GenerateID(): cv.declare_id(DosePowerSensor), cv.Required(CONF_NAME): cv.string})

EQUIV_DOSE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_MICROSIEVERT_PER_HOUR,
    icon=ICON_RADIATION,
    accuracy_decimals=3,
    state_class=STATE_CLASS_MEASUREMENT,
).extend({cv.GenerateID(): cv.declare_id(EquivDoseSensor), cv.Required(CONF_NAME): cv.string})

TOTAL_DOSE_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_MICROSIEVERT,
    icon=ICON_RADIATION,
    accuracy_decimals=3,
    state_class=STATE_CLASS_TOTAL_INCREASING,
).extend({cv.GenerateID(): cv.declare_id(TotalDoseSensor), cv.Required(CONF_NAME): cv.string})

CPM_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_COUNTS_PER_MINUTE,
    icon="mdi:pulse",
    accuracy_decimals=2,
    state_class=STATE_CLASS_MEASUREMENT,
).extend({cv.GenerateID(): cv.declare_id(CPMSensor), cv.Required(CONF_NAME): cv.string})

COUNT_SCHEMA = sensor.sensor_schema(
    unit_of_measurement="pulses",
    icon="mdi:counter",
    accuracy_decimals=0,
    state_class=STATE_CLASS_MEASUREMENT,
).extend({cv.GenerateID(): cv.declare_id(CountSensor), cv.Required(CONF_NAME): cv.string})

STATUS_SCHEMA = text_sensor.text_sensor_schema(
    icon="mdi:check-circle-outline",
).extend({cv.GenerateID(): cv.declare_id(StatusSensor), cv.Required(CONF_NAME): cv.string})


# General YAML Configuration Schema for GGreg20_V3
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(GGreg20V3Component),

    cv.Required(CONF_PIN): pins.internal_gpio_input_pin_schema,

    cv.Optional(CONF_MEASUREMENT_PERIOD, default=60): cv.int_range(min=10),
    cv.Optional(CONF_DEAD_TIME_US, default=190): cv.int_range(min=0, max=1000),
    cv.Optional(CONF_INT_LOGIC, default=0): cv.int_range(min=0, max=1),

    cv.Required(CONF_RADIATION_POWER): DOSE_POWER_SCHEMA,
    cv.Optional(CONF_DOSE_POWER_FACTOR, default=0.00378): cv.float_,

    cv.Required(CONF_EQUIVALENT_DOSE): EQUIV_DOSE_SCHEMA,
    cv.Optional(CONF_EQUIV_DOSE_FACTOR, default=0.00332): cv.float_,

    cv.Required(CONF_TOTAL_DOSE): TOTAL_DOSE_SCHEMA,

    cv.Required(CONF_CPM): CPM_SCHEMA,
    cv.Required(CONF_COUNT): COUNT_SCHEMA,
    cv.Required(CONF_STATUS): STATUS_SCHEMA,

}).extend(cv.COMPONENT_SCHEMA)


# Function to generate C++ code
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))

    cg.add(var.set_measurement_period_sec(config[CONF_MEASUREMENT_PERIOD]))
    cg.add(var.set_dead_time_us(config[CONF_DEAD_TIME_US]))
    cg.add(var.set_int_logic(config[CONF_INT_LOGIC]))

    cg.add(var.set_dose_power_factor(config[CONF_DOSE_POWER_FACTOR]))
    cg.add(var.set_equiv_dose_factor(config[CONF_EQUIV_DOSE_FACTOR]))

    # 1. Radiation Power
    conf_power = config[CONF_RADIATION_POWER]
    sens_power = await sensor.new_sensor(conf_power)
    cg.add(var.set_dose_power_sensor(sens_power))

    # 2. Equivalent Dose
    conf_equiv = config[CONF_EQUIVALENT_DOSE]
    sens_equiv = await sensor.new_sensor(conf_equiv)
    cg.add(var.set_equiv_dose_sensor(sens_equiv))

    # 3. Total Dose
    conf_total = config[CONF_TOTAL_DOSE]
    sens_total = await sensor.new_sensor(conf_total)
    cg.add(var.set_total_dose_sensor(sens_total))

    # 4. CPM
    conf_cpm = config[CONF_CPM]
    sens_cpm = await sensor.new_sensor(conf_cpm)
    cg.add(var.set_cpm_sensor(sens_cpm))

    # 5. Count
    conf_count = config[CONF_COUNT]
    sens_count = await sensor.new_sensor(conf_count)
    cg.add(var.set_count_sensor(sens_count))

    # 6. Status
    conf_status = config[CONF_STATUS]
    sens_status = await text_sensor.new_text_sensor(conf_status)
    cg.add(var.set_status_sensor(sens_status))

