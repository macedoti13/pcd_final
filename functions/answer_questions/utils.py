non_weather_training_columns_list = [
    'hour', 'day_of_week', 'week_of_year', 'year', 'input_flow_rate_lag_1', 'reservoir_level_percentage_lag_1', 'pressure_lag_1', 'output_flow_rate_lag_1', 'pump_1_lag_1', 'pump_2_lag_1',
    'input_flow_rate_lag_2', 'reservoir_level_percentage_lag_2', 'pressure_lag_2', 'output_flow_rate_lag_2', 'pump_1_lag_2', 'pump_2_lag_2', 'input_flow_rate_lag_3', 'reservoir_level_percentage_lag_3',
    'pressure_lag_3', 'output_flow_rate_lag_3', 'pump_1_lag_3', 'pump_2_lag_3', 'input_flow_rate_lag_6', 'reservoir_level_percentage_lag_6', 'pressure_lag_6', 'output_flow_rate_lag_6', 'pump_1_lag_6',
    'pump_2_lag_6', 'input_flow_rate_lag_12', 'reservoir_level_percentage_lag_12', 'pressure_lag_12', 'output_flow_rate_lag_12', 'pump_1_lag_12', 'pump_2_lag_12', 'input_flow_rate_lag_24', 'reservoir_level_percentage_lag_24',
    'pressure_lag_24', 'output_flow_rate_lag_24', 'pump_1_lag_24', 'pump_2_lag_24', 'input_flow_rate_roll_mean_3', 'reservoir_level_percentage_roll_mean_3', 'pressure_roll_mean_3', 'output_flow_rate_roll_mean_3',
    'pump_1_roll_mean_3', 'pump_2_roll_mean_3', 'input_flow_rate_roll_mean_6', 'reservoir_level_percentage_roll_mean_6', 'pressure_roll_mean_6', 'output_flow_rate_roll_mean_6', 'pump_1_roll_mean_6', 'pump_2_roll_mean_6',
    'input_flow_rate_roll_mean_12', 'reservoir_level_percentage_roll_mean_12', 'pressure_roll_mean_12', 'output_flow_rate_roll_mean_12', 'pump_1_roll_mean_12', 'pump_2_roll_mean_12', 'input_flow_rate_roll_mean_24',
    'reservoir_level_percentage_roll_mean_24', 'pressure_roll_mean_24', 'output_flow_rate_roll_mean_24', 'pump_1_roll_mean_24','pump_2_roll_mean_24'
]

with_weather_training_columns_list = [
    'hour','day_of_week', 'week_of_year', 'year', 'input_flow_rate_lag_1', 'reservoir_level_percentage_lag_1', 'pressure_lag_1', 'output_flow_rate_lag_1', 'pump_1_lag_1', 'pump_2_lag_1', 'input_flow_rate_lag_2',
    'reservoir_level_percentage_lag_2', 'pressure_lag_2', 'output_flow_rate_lag_2', 'pump_1_lag_2', 'pump_2_lag_2', 'input_flow_rate_lag_3', 'reservoir_level_percentage_lag_3', 'pressure_lag_3', 'output_flow_rate_lag_3',
    'pump_1_lag_3', 'pump_2_lag_3', 'input_flow_rate_lag_6', 'reservoir_level_percentage_lag_6', 'pressure_lag_6', 'output_flow_rate_lag_6', 'pump_1_lag_6', 'pump_2_lag_6', 'input_flow_rate_lag_12', 'reservoir_level_percentage_lag_12',
    'pressure_lag_12', 'output_flow_rate_lag_12', 'pump_1_lag_12', 'pump_2_lag_12', 'input_flow_rate_lag_24', 'reservoir_level_percentage_lag_24', 'pressure_lag_24', 'output_flow_rate_lag_24', 'pump_1_lag_24', 'pump_2_lag_24',
    'input_flow_rate_roll_mean_3', 'reservoir_level_percentage_roll_mean_3', 'pressure_roll_mean_3', 'output_flow_rate_roll_mean_3', 'pump_1_roll_mean_3', 'pump_2_roll_mean_3', 'input_flow_rate_roll_mean_6',
    'reservoir_level_percentage_roll_mean_6', 'pressure_roll_mean_6', 'output_flow_rate_roll_mean_6', 'pump_1_roll_mean_6', 'pump_2_roll_mean_6', 'input_flow_rate_roll_mean_12', 'reservoir_level_percentage_roll_mean_12',
    'pressure_roll_mean_12', 'output_flow_rate_roll_mean_12', 'pump_1_roll_mean_12', 'pump_2_roll_mean_12', 'input_flow_rate_roll_mean_24', 'reservoir_level_percentage_roll_mean_24', 'pressure_roll_mean_24',
    'output_flow_rate_roll_mean_24', 'pump_1_roll_mean_24', 'pump_2_roll_mean_24', 'air_temp_c_lag_1', 'total_precip_mm_lag_1', 'relative_humidity_percentage_lag_1', 'air_temp_c_lag_2', 'total_precip_mm_lag_2',
    'relative_humidity_percentage_lag_2', 'air_temp_c_lag_3', 'total_precip_mm_lag_3', 'relative_humidity_percentage_lag_3', 'air_temp_c_lag_6', 'total_precip_mm_lag_6', 'relative_humidity_percentage_lag_6',
    'air_temp_c_lag_12', 'total_precip_mm_lag_12', 'relative_humidity_percentage_lag_12', 'air_temp_c_lag_24', 'total_precip_mm_lag_24', 'relative_humidity_percentage_lag_24', 'air_temp_c_roll_mean_3',
    'total_precip_mm_roll_mean_3', 'relative_humidity_percentage_roll_mean_3', 'air_temp_c_roll_mean_6', 'total_precip_mm_roll_mean_6', 'relative_humidity_percentage_roll_mean_6', 'air_temp_c_roll_mean_12',
    'total_precip_mm_roll_mean_12', 'relative_humidity_percentage_roll_mean_12', 'air_temp_c_roll_mean_24', 'total_precip_mm_roll_mean_24', 'relative_humidity_percentage_roll_mean_24',
]