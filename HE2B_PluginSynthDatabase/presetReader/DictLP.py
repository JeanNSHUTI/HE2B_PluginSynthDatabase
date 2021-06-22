
lokomotive_set = {
    0: b'\xff\xff',                        # pkey
    1: b'\xff\xff',                        # pname
    2: 0.1,                         # bpm_sync
    3: 0.1,                         # lfo_type_select
    4: 0.1,                         # lfo_speed
    5: 0.1,                         # lfo_target_select
    6: 0.1,                         # lfo_amount
    7: 0.1,                         # osc_hardsync_amount
    8: 0.1,                         # osc_pw_amount
    9: 0.1,                         # osc_saw_detune_amount
    10: 0.1,                        # sub_osc_waveform
    11: 0.1,                        # osc_noise_amount
    12: 0.1,                        # osc_saw_amount
    13: 0.1,                        # osc_pulse_amount
    14: 0.1,                        # sub_osc_amount
    15: 0.1,                        # env_attack
    16: 0.1,                        # env_decay
    17: 0.1,                        # env_sustain
    18: 0.1,                        # env_release
    19: 0.1,                        # phonic_type
    20: 0.1,                        # filter_type_select
    21: 0.1,                        # cutoff_amount
    22: 0.1,                        # resonance_amount
    23: 0.1,                        # kb_tracking_amount
    24: 0.1,                        # envelope_amount
    25: 0.1,                        # drive_pre_post_switch
    26: 0.1,                        # drive_amount
    27: 0.1,                        # amp_env_gate_select
    28: 0.1,                        # amp_volume
    29: 0.1,                        # pitch_bend_range
    30: 0.1,                        # mod_wheel_target_select
    31: 0.1,                        # velocity_target_select
    32: 0.1                         # portamento_speed
}


def display_preset_name():
    # bytes_object = bytes.fromhex(lokomotive_set[1])
    # bytes_object = lokomotive_set[1]
    # ascii_string = bytes_object.decode("ASCII")
    return lokomotive_set[1]
