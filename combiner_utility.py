import os
from datetime import datetime, timedelta
import pytz
import sys
import struct
import fnmatch
import psutil
import tempfile
import threading

saver_path = str(input('Enter the location to save:\t'))
PI = 3.14159265358979323846


def source_log():
    source_path = str(
        input('Enter the path of log file source folder:\t')).strip()
    return log_checker(source_path)


def files_to_save():
    files = [
        'SATB_IRNSS_L5_DATA', 'SATB_IRNSS_S1_DATA', 'SATB_GPS_L1_DATA',
        'SBSATB_DATA', 'SBASCORR_DATA', 'POSB_DATA', 'TIDB_DATA', 'CLKB_DATA',
        'DOPB_DATA', 'RNBB_IRNSS_L5_DATA', 'RNBB_IRNSS_S1_DATA',
        'RNBB_GPS_L1_DATA', 'IMB_DATA', 'ACKB_DATA', 'CONB_DATA'
    ]

    file_save = []

    for file in files:
        if input('Do you want to save %s file? (y/n)\t' % (file)) == 'y':
            file_save.append(file)

    return file_save


def current_time():
    """
    A function to print current time to the console
    """
    print(str(datetime.now())+'\n')


def get_path(towc, week_no, gnss_def='IRNSS'):
    """
    It creates a path string based on stock IRNSS decoder application for 
    saving the dictionaries created
    
    Parameters:
        towc -- the initial towc based on which the path is created for 
            that prahara (three hour batch)
        week_no -- the week number since the initial_date (IRNSS/GPS) as
            defined in ICD
        gnss_def -- type of GNSS system being used (IRNSS/GPS) to initialize
            initial date

    Returns:
        path -- the directory path for saving the dictionaries, based on 
            stock IRNSS decoder

        final_towc -- the time at which the directory needs to change
    """

    #initialize initial time based on the gnss_system being used
    if gnss_def == 'IRNSS':
        initial_date = datetime(
            year=1999, month=8, day=22, hour=0, minute=0, second=0, tzinfo=pytz.UTC)

    elif gnss_def == 'GPS':
        initial_date = datetime(year=1980, month=1, day=6,
                                hour=0, minute=0, second=0, tzinfo=pytz.UTC)

    #finds the logged time of data in local time system (Kolkata UTC+5:30)
    this_prahara = initial_date + timedelta(days=7 * week_no, seconds=towc)
    # this_prahara = this_prahara.replace(tzinfo=pytz.utc).astimezone(tz = pytz.timezone('Asia/Kolkata'))

    #creates path similar to that of the stock IRNSS decoder application
    path = os.path.join(saver_path, 'Extracted_Files', this_prahara.strftime(
        '%d_%m_%Y'), (this_prahara.strftime('%A')).upper(), str((this_prahara.hour // 3) * 3))

    #this part finds the time of next prahara as a datetime object
    if this_prahara.hour > 20:
        next_prahara = this_prahara.replace(day=this_prahara.day + 1,
                                            hour=((this_prahara.hour // 3)
                                                  * 3 + 3) % 24,
                                            minute=0, second=0, microsecond=0)
    else:
        next_prahara = this_prahara.replace(hour=((this_prahara.hour // 3) * 3 + 3) % 24,
                                            minute=0, second=0, microsecond=0)

    #calculation of time for the next towc before updating file_path,
    final_towc = (towc + (next_prahara - this_prahara).total_seconds()
                  ) + timedelta(days=7 * week_no).total_seconds()

    return path, final_towc


def create_path(path):
    """
    A function to check if a path exists and if not, create the path

    Parameters:
        path -- the path which has to be created

    Returns:
        None
    """

    try:
        #confirms that the path does not exist
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        sys.exit('Could not create directory for saving files')


# The next few functions decode data based on the ICD for the receiver module
# They take three parameters, 1. File to decode, 2. the data dictionary,
# 3. message header
def SATB_IRNSS(file, satb_irnss_data, message_header):
    no_of_channels = struct.unpack('<I', file.read(4))[0]
    file.read(4)
    acq_status_1 = struct.unpack('<I', file.read(4))[0]
    acq_status_2 = struct.unpack('<I', file.read(4))[0]

    for key, value in message_header.items():
        satb_irnss_data[key].append(value)

    satb_irnss_data['No_of_channels'].append(no_of_channels)
    satb_irnss_data['Acq_status_1'].append(acq_status_1)
    satb_irnss_data['Acq_status_2'].append(acq_status_2)

    for i in range(1, 12, 1):
        prn = struct.unpack('<I', file.read(4))[0]
        if prn == 255:
            file.read(4*27)
            satb_irnss_data['PRN_'+str(i)].append(0)
            satb_irnss_data['Channel_stat_'+str(i)].append(0)
            satb_irnss_data['Doppler_'+str(i)].append(0)
            satb_irnss_data['C/N0_'+str(i)].append(0)
            satb_irnss_data['Azimuth_'+str(i)].append(0)
            satb_irnss_data['Elevation_'+str(i)].append(0)
            satb_irnss_data['PR_'+str(i)].append(0)
            satb_irnss_data['DR_'+str(i)].append(0)
            satb_irnss_data['Reject_code_'+str(i)].append(0)
            satb_irnss_data['Lock_time_'+str(i)].append(0)
            satb_irnss_data['Iono_delay_'+str(i)].append(0)
            satb_irnss_data['Tropo_delay_'+str(i)].append(0)
            satb_irnss_data['Carrier_cycles_'+str(i)].append(0)
            satb_irnss_data['Sat_X_'+str(i)].append(0)
            satb_irnss_data['Sat_Y_'+str(i)].append(0)
            satb_irnss_data['Sat_Z_'+str(i)].append(0)
            satb_irnss_data['Sat_vel_X_'+str(i)].append(0)
            satb_irnss_data['Sat_vel_Y_'+str(i)].append(0)
            satb_irnss_data['Sat_vel_Z_'+str(i)].append(0)
            satb_irnss_data['Range_res_'+str(i)].append(0)
            satb_irnss_data['Sat_clk_correc_'+str(i)].append(0)

        else:
            satb_irnss_data['PRN_'+str(i)].append(prn)
            satb_irnss_data['Channel_stat_' +
                            str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_irnss_data['Doppler_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['C/N0_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Azimuth_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Elevation_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['PR_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['DR_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['Reject_code_' +
                            str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_irnss_data['Lock_time_' +
                            str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_irnss_data['Iono_delay_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Tropo_delay_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Carrier_cycles_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['Sat_X_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['Sat_Y_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['Sat_Z_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_irnss_data['Sat_vel_X_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Sat_vel_Y_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Sat_vel_Z_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Range_res_' +
                            str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_irnss_data['Sat_clk_correc_' +
                            str(i)].append(struct.unpack('<d', file.read(8))[0])

    return satb_irnss_data


def SATB_GPS(file, satb_gps_data, message_header):
    no_of_channels = struct.unpack('<I', file.read(4))[0]
    file.read(4)
    acq_status_1 = struct.unpack('<I', file.read(4))[0]
    acq_status_2 = struct.unpack('<I', file.read(4))[0]

    for key, value in message_header.items():
        satb_gps_data[key].append(value)

    satb_gps_data['No_of_channels'].append(no_of_channels)
    satb_gps_data['Acq_status_1'].append(acq_status_1)
    satb_gps_data['Acq_status_2'].append(acq_status_2)

    for i in range(1, 13, 1):
        prn = struct.unpack('<I', file.read(4))[0]
        if prn == 255:
            file.read(4*27)
            satb_gps_data['PRN_'+str(i)].append(0)
            satb_gps_data['Channel_stat_'+str(i)].append(0)
            satb_gps_data['Doppler_'+str(i)].append(0)
            satb_gps_data['C/N0_'+str(i)].append(0)
            satb_gps_data['Azimuth_'+str(i)].append(0)
            satb_gps_data['Elevation_'+str(i)].append(0)
            satb_gps_data['PR_'+str(i)].append(0)
            satb_gps_data['DR_'+str(i)].append(0)
            satb_gps_data['Reject_code_'+str(i)].append(0)
            satb_gps_data['Lock_time_'+str(i)].append(0)
            satb_gps_data['Iono_delay_'+str(i)].append(0)
            satb_gps_data['Tropo_delay_'+str(i)].append(0)
            satb_gps_data['Carrier_cycles_'+str(i)].append(0)
            satb_gps_data['Sat_X_'+str(i)].append(0)
            satb_gps_data['Sat_Y_'+str(i)].append(0)
            satb_gps_data['Sat_Z_'+str(i)].append(0)
            satb_gps_data['Sat_vel_X_'+str(i)].append(0)
            satb_gps_data['Sat_vel_Y_'+str(i)].append(0)
            satb_gps_data['Sat_vel_Z_'+str(i)].append(0)
            satb_gps_data['Range_res_'+str(i)].append(0)
            satb_gps_data['Sat_clk_correc_'+str(i)].append(0)

        else:
            satb_gps_data['PRN_'+str(i)].append(prn)
            satb_gps_data['Channel_stat_' +
                          str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_gps_data['Doppler_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['C/N0_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Azimuth_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Elevation_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['PR_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['DR_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['Reject_code_' +
                          str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_gps_data['Lock_time_' +
                          str(i)].append(struct.unpack('<I', file.read(4))[0])
            satb_gps_data['Iono_delay_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Tropo_delay_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Carrier_cycles_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['Sat_X_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['Sat_Y_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['Sat_Z_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])
            satb_gps_data['Sat_vel_X_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Sat_vel_Y_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Sat_vel_Z_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Range_res_' +
                          str(i)].append(struct.unpack('<f', file.read(4))[0])
            satb_gps_data['Sat_clk_correc_' +
                          str(i)].append(struct.unpack('<d', file.read(8))[0])

    return satb_gps_data


def SBSATB(file, sbsatb_data, message_header):
    for key, value in message_header.items():
        sbsatb_data[key].append(value)

    no_of_channels = struct.unpack('<I', file.read(4))[0]
    file.read(4)

    sbsatb_data['No_of_channels'].append(no_of_channels)

    for i in range(1, 3, 1):
        sbsatb_data['PRN_'+str(i)].append(struct.unpack('<I', file.read(4))[0])
        sbsatb_data['Msg_type_' +
                    str(i)].append(struct.unpack('<I', file.read(4))[0])
        sbsatb_data['Channel_stat_' +
                    str(i)].append(struct.unpack('<I', file.read(4))[0])
        sbsatb_data['C/N0_' +
                    str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbsatb_data['Azimuth_' +
                    str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbsatb_data['Elevation_' +
                    str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbsatb_data['Lock_time_' +
                    str(i)].append(struct.unpack('<I', file.read(4))[0])
        sbsatb_data['Doppler_' +
                    str(i)].append(struct.unpack('<f', file.read(4))[0])

    return sbsatb_data


def SBASCORR(file, sbascorr_data, message_header):
    for key, value in message_header.items():
        sbascorr_data[key].append(value)

    no_of_channels = struct.unpack('<I', file.read(4))[0]
    sbas_corr_flag = struct.unpack('<I', file.read(4))[0]
    sbascorr_data['No_of_channels'].append(no_of_channels)
    sbascorr_data['SBAS_corr'].append(sbas_corr_flag)

    for i in range(1, 13, 1):
        sbascorr_data['PRN_' +
                      str(i)].append(struct.unpack('<I', file.read(4))[0])
        sbascorr_data['Fast_corr_1_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['Fast_corr_2_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_1_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_2_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_3_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_4_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_5_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_6_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_7_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['LT_corr_8_' +
                      str(i)].append(struct.unpack('<f', file.read(4))[0])
        sbascorr_data['Reserved_' +
                      str(i)].append(struct.unpack('<I', file.read(4))[0])

    return sbascorr_data


def POSB(file, posb_data, message_header):
    for key, value in message_header.items():
        posb_data[key].append(value)
    posb_data['X_POS'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Y_POS'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Z_POS'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Undulation'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['X_VEL'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Y_VEL'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Z_VEL'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Pos_stat'].append(struct.unpack('<I', file.read(4))[0])
    posb_data['Speed'].append(struct.unpack('<f', file.read(4))[0])
    posb_data['Std_dev_east'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Std_dev_north'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Std_dev_up'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Pos_est_time'].append(struct.unpack('<I', file.read(4))[0])
    posb_data['Reserved'].append(struct.unpack('<I', file.read(4))[0])
    posb_data['TTFF'].append(struct.unpack('<I', file.read(4))[0])
    posb_data['Pos_mode'].append(struct.unpack('<I', file.read(4))[0])
    posb_data['Lat'].append(struct.unpack('<d', file.read(8))[0]*360/(2*PI))
    posb_data['Long'].append(struct.unpack('<d', file.read(8))[0]*360/(2*PI))
    posb_data['Alt'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Pos_err_east'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Pos_err_north'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Pos_err_up'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Lat_fix'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Long_fix'].append(struct.unpack('<d', file.read(8))[0])
    posb_data['Alt_fix'].append(struct.unpack('<d', file.read(8))[0])

    return posb_data


def TIDB(file, tidb_data, message_header):
    for key, value in message_header.items():
        tidb_data[key].append(value)
    tidb_data['Recv_day'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Recv_mth'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Recv_hr'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Recv_min'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Recv_sec'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Ext_clk_val'].append(struct.unpack('<B', file.read(1))[0])
    tidb_data['Recv_yr'].append(struct.unpack('<H', file.read(2))[0])
    tidb_data['Ext_clk_freq'].append(struct.unpack('<I', file.read(4))[0])
    tidb_data['Reserved'].append(struct.unpack('<f', file.read(4))[0])

    return tidb_data


def CLKB(file, clkb_data, message_header):
    for key, value in message_header.items():
        clkb_data[key].append(value)
    clkb_data['Clk_bias'].append(struct.unpack('<d', file.read(8))[0])
    clkb_data['Clk_drift'].append(struct.unpack('<d', file.read(8))[0])
    clkb_data['Inter_sys_bias'].append(struct.unpack('<d', file.read(8))[0])
    clkb_data['UTC_offset'].append(struct.unpack('<f', file.read(4))[0])
    clkb_data['Pos_mode'].append(struct.unpack('<I', file.read(4))[0])

    return clkb_data


def DOPB(file, dopb_data, message_header):
    for key, value in message_header.items():
        dopb_data[key].append(value)
    dopb_data['GDOP'].append(struct.unpack('<f', file.read(4))[0])
    dopb_data['PDOP'].append(struct.unpack('<f', file.read(4))[0])
    dopb_data['HDOP'].append(struct.unpack('<f', file.read(4))[0])
    dopb_data['VDOP'].append(struct.unpack('<f', file.read(4))[0])
    dopb_data['TDOP'].append(struct.unpack('<f', file.read(4))[0])
    dopb_data['No_tot_sat'].append(struct.unpack('<B', file.read(1))[0])
    dopb_data['No_irnss_sat'].append(struct.unpack('<B', file.read(1))[0])
    dopb_data['No_gps_sat'].append(struct.unpack('<B', file.read(1))[0])
    dopb_data['Reserved'].append(struct.unpack('<B', file.read(1))[0])
    dopb_data['Pos_mode'].append(struct.unpack('<I', file.read(4))[0])
    dopb_data['Reserved2'].append(struct.unpack('<I', file.read(4))[0])

    return dopb_data


def CONB(file, conb_data, message_header):
    for key, value in message_header.items():
        conb_data[key].append(value)
    conb_data['Host_ip_add'].append(
        [struct.unpack('<B', file.read(1))[0] for _ in range(4)])
    conb_data['Sub_net_mask'].append(
        [struct.unpack('<B', file.read(1))[0] for _ in range(4)])
    conb_data['Gateway'].append(
        [struct.unpack('<B', file.read(1))[0] for _ in range(4)])
    conb_data['Receiver_ip'].append(
        [struct.unpack('<B', file.read(1))[0] for _ in range(4)])
    conb_data['Hardware_ver'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['Software'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['Check_sum'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['Mask_angle_irnss'].append(struct.unpack('<f', file.read(4))[0])
    conb_data['Mask_angle_gps'].append(struct.unpack('<f', file.read(4))[0])
    conb_data['AGC_ct_irnss_l5'].append(struct.unpack('<B', file.read(1))[0])
    conb_data['AGC_ct_irnss_s1'].append(struct.unpack('<B', file.read(1))[0])
    conb_data['AGC_ct_gps_l1'].append(struct.unpack('<B', file.read(1))[0])
    conb_data['SBAS_sat'].append(struct.unpack('<B', file.read(1))[0])
    conb_data['Port'].append(struct.unpack('<H', file.read(2))[0])
    conb_data['Reserved'].append(struct.unpack('<H', file.read(2))[0])
    conb_data['Blackfin_vheck_sum'].append(
        struct.unpack('<I', file.read(4))[0])
    conb_data['SHARC_check_sum'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['FPGA_check_sum'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['Prod_info_SNo_word_1'].append(
        struct.unpack('<I', file.read(4))[0])
    conb_data['Prod_info_SNo_word_2'].append(
        struct.unpack('<I', file.read(4))[0])
    conb_data['Cable_delay_irnss_l5'].append(
        struct.unpack('<f', file.read(4))[0])
    conb_data['Cable_delay_irnss_s1'].append(
        struct.unpack('<f', file.read(4))[0])
    conb_data['Cable_delay_gps_l1'].append(
        struct.unpack('<f', file.read(4))[0])
    conb_data['LNA_delay_irnss_l5'].append(
        struct.unpack('<f', file.read(4))[0])
    conb_data['LNA_delay_irnss_s1'].append(
        struct.unpack('<f', file.read(4))[0])
    conb_data['LNA_delay_gps_l1'].append(struct.unpack('<f', file.read(4))[0])
    conb_data['Reserved_1'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['Reserved_2'].append(struct.unpack('<I', file.read(4))[0])
    conb_data['RF_delay_irnss_l5'].append(struct.unpack('<f', file.read(4))[0])
    conb_data['RF_delay_irnss_s1'].append(struct.unpack('<f', file.read(4))[0])
    conb_data['RF_delay_gps_l1'].append(struct.unpack('<f', file.read(4))[0])

    return conb_data


def ACKB(file, ackb_data, message_header):
    assert isinstance(ackb_data, dict)
    for key, value in message_header.items():
        ackb_data[key].append(value)
    ackb_data['Mes_ID'].append(struct.unpack('<H', file.read(2))[0])
    ackb_data['Ack'].append(struct.unpack('<H', file.read(2))[0])
    ackb_data['Reserved'].append(struct.unpack('<I', file.read(4))[0])

    return ackb_data


def RNBB(file, rnbb_data, message_header):
    for key, value in message_header.items():
        rnbb_data[key].append(value)
    rnbb_data['WN'].append(struct.unpack('<H', file.read(2))[0])
    rnbb_data['PRN'].append(struct.unpack('<B', file.read(1))[0])
    rnbb_data['Sub_frame'].append(struct.unpack('<B', file.read(1))[0])
    rnbb_data['TOWC_1'].append(struct.unpack('<I', file.read(4))[0])
    temp = [struct.unpack('<B', file.read(1))[0] for _ in range(37)]
    rnbb_data['Raw_nav'].append(temp)
    rnbb_data['Reserved'].append(
        [struct.unpack('<B', file.read(1))[0] for _ in range(3)])

    return rnbb_data


def IMB(file, imb_data, message_header):
    for key, value in message_header.items():
        imb_data[key].append(value)
    for i in range(1, 257, 1):
        imb_data['Bin_' +
                 str(i)+'_freq'].append(struct.unpack('<H', file.read(2))[0])
    imb_data['Inter_sig_freq_l5'].append(struct.unpack('<f', file.read(4))[0])
    imb_data['FLI_l5'].append(struct.unpack('<I', file.read(4))[0])
    imb_data['Inter_sig_freq_s1'].append(struct.unpack('<f', file.read(4))[0])
    imb_data['FLI_s1'].append(struct.unpack('<I', file.read(4))[0])
    imb_data['Inter_sig_freq_l1'].append(struct.unpack('<f', file.read(4))[0])
    imb_data['FLI_l1'].append(struct.unpack('<I', file.read(4))[0])

    return imb_data


def reset_dict(to_reset):
    """
    A function to clear all the lists in the given dictionary

    Parameters:
        to_reset -- the dictionary which has to be reset
    
    Returns:
        after_reset -- dictionary containing the variables after reset
    """

    # confirms that the variable passed is a dictionary object
    assert(isinstance(to_reset, dict))

    # creates a new dictionary which will store the reset object
    after_reset = {}

    # extracts all the keys in the input dictionary and creates empty lists
    # for those keys in the new dictionary
    for key in to_reset:
        if isinstance(to_reset[key], list):
            after_reset[key] = []
        else:
            after_reset[key] = 0

    return after_reset


def initializer(names):
    """
    Function to initialise all the dictionaries to be used for the main program

    Returns:
        Dictionaries corresponding to all the data fields
    """

    SATB_IRNSS_L5_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [], 'No_of_channels': [],
        'Acq_status_1': [], 'Acq_status_2': []
    }

    for_irnss_gps = [
        'PRN', 'Channel_stat', 'Doppler', 'C/N0', 'Azimuth',
        'Elevation', 'PR', 'DR', 'Reject_code', 'Lock_time',
        'Iono_delay', 'Tropo_delay', 'Carrier_cycles',
        'Sat_X', 'Sat_Y', 'Sat_Z', 'Sat_vel_X',
        'Sat_vel_Y', 'Sat_vel_Z', 'Range_res', 'Sat_clk_correc'
    ]

    for i in range(1, 12, 1):
        for key in for_irnss_gps:
            SATB_IRNSS_L5_DATA[key+'_'+str(i)] = []

    SATB_IRNSS_S1_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [], 'No_of_channels': [],
        'Acq_status_1': [], 'Acq_status_2': []
    }

    for i in range(1, 12, 1):
        for key in for_irnss_gps:
            SATB_IRNSS_S1_DATA[key+'_'+str(i)] = []

    SATB_GPS_L1_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [], 'No_of_channels': [],
        'Acq_status_1': [], 'Acq_status_2': []
    }

    for i in range(1, 13, 1):
        for key in for_irnss_gps:
            SATB_GPS_L1_DATA[key+'_'+str(i)] = []

    SBSATB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'No_of_channels': []
    }

    for_sbas = [
        'PRN', 'Msg_type', 'Channel_stat', 'C/N0',
        'Azimuth', 'Elevation', 'Lock_time', 'Doppler'
    ]

    for i in range(1, 3, 1):
        for item in for_sbas:
            SBSATB_DATA[item+'_'+str(i)] = []

    SBASCORR_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'No_of_channels': [], 'SBAS_corr': []
    }

    for_sbascorr = [
        'PRN', 'Fast_corr_1', 'Fast_corr_2', 'LT_corr_1',
        'LT_corr_2', 'LT_corr_3', 'LT_corr_4',
        'LT_corr_5', 'LT_corr_6', 'LT_corr_7', 'LT_corr_8', 'Reserved'
    ]

    for i in range(1, 13, 1):
        for item in for_sbascorr:
            SBASCORR_DATA[item+'_'+str(i)] = []

    POSB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'X_POS': [], 'Y_POS': [], 'Z_POS': [], 'Undulation': [],
        'X_VEL': [], 'Y_VEL': [], 'Z_VEL': [], 'Pos_stat': [],
        'Speed': [], 'Std_dev_east': [], 'Std_dev_north': [],
        'Std_dev_up': [], 'Pos_est_time': [], 'Reserved': [],
        'TTFF': [], 'Lat': [], 'Long': [], 'Alt': [], 'Pos_err_east': [],
        'Pos_err_north': [], 'Pos_err_up': [], 'Lat_fix': [],
        'Long_fix': [], 'Alt_fix': [], 'Pos_mode': []
    }

    TIDB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'Recv_day': [], 'Recv_mth': [], 'Recv_hr': [], 'Recv_min': [],
        'Recv_sec': [], 'Ext_clk_val': [], 'Recv_yr': [], 'Ext_clk_freq': [],
        'Reserved': []
    }

    CLKB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'Clk_bias': [], 'Clk_drift': [], 'Inter_sys_bias': [],
        'UTC_offset': [], 'Pos_mode': []
    }

    DOPB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'GDOP': [], 'PDOP': [], 'HDOP': [], 'VDOP': [], 'TDOP': [],
        'No_tot_sat': [], 'No_irnss_sat': [], 'No_gps_sat': [],
        'Reserved': [], 'Pos_mode': [], 'Reserved2': []
    }

    CONB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'Host_ip_add': [], 'Receiver_ip': [], 'Sub_net_mask': [],
        'Gateway': [], 'Hardware_ver': [], 'Software': [], 'Check_sum': [],
        'Mask_angle_irnss': [], 'Mask_angle_gps': [], 'AGC_ct_irnss_l5': [],
        'AGC_ct_irnss_s1': [], 'AGC_ct_gps_l1': [], 'Port': [], 'Reserved': [],
        'Blackfin_vheck_sum': [], 'SHARC_check_sum': [], 'FPGA_check_sum': [],
        'Prod_info_SNo_word_1': [], 'Prod_info_SNo_word_2': [],
        'Cable_delay_irnss_l5': [], 'Cable_delay_irnss_s1': [], 'Cable_delay_gps_l1': [],
        'LNA_delay_irnss_l5': [], 'LNA_delay_irnss_s1': [], 'LNA_delay_gps_l1': [],
        'SBAS_sat': [], 'Reserved_1': [], 'Reserved_2': [], 'RF_delay_irnss_l5': [],
        'RF_delay_irnss_s1': [], 'RF_delay_gps_l1': []
    }

    ACKB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'Mes_ID': [], 'Ack': [], 'Reserved': []
    }

    RNBB_IRNSS_L5_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'WN': [], 'PRN': [], 'Sub_frame': [], 'TOWC_1': [],
        'Raw_nav': [], 'Reserved': []
    }

    RNBB_IRNSS_S1_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'WN': [], 'PRN': [], 'Sub_frame': [], 'TOWC_1': [],
        'Raw_nav': [], 'Reserved': []
    }

    RNBB_GPS_L1_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
        'WN': [], 'PRN': [], 'Sub_frame': [], 'TOWC_1': [],
        'Raw_nav': [], 'Reserved': []
    }

    IMB_DATA = {
        'TOWC': [], 'Week_no': [], 'Rec_ns': [], 'Sys_stat_1': [],
        'Sys_stat_2': [], 'Sys_stat_3': [], 'Block_ct': [],
    }

    for i in range(1, 257, 1):
        IMB_DATA['Bin_'+str(i)+'_freq'] = []

    for item in ['Inter_sig_freq_l5', 'FLI_l5', 'Inter_sig_freq_s1', 'FLI_s1', 'Inter_sig_freq_l1', 'FLI_l1']:
        IMB_DATA[item] = []

    dictionaries = {
        'SATB_IRNSS_L5_DATA': SATB_IRNSS_L5_DATA,
        'SATB_IRNSS_S1_DATA': SATB_IRNSS_S1_DATA,
        'SATB_GPS_L1_DATA': SATB_GPS_L1_DATA,
        'SBSATB_DATA': SBSATB_DATA,
        'SBASCORR_DATA': SBASCORR_DATA,
        'POSB_DATA': POSB_DATA,
        'TIDB_DATA': TIDB_DATA,
        'CLKB_DATA': CLKB_DATA,
        'DOPB_DATA': DOPB_DATA,
        'RNBB_IRNSS_L5_DATA': RNBB_IRNSS_L5_DATA,
        'RNBB_IRNSS_S1_DATA': RNBB_IRNSS_S1_DATA,
        'RNBB_GPS_L1_DATA': RNBB_GPS_L1_DATA,
        'IMB_DATA': IMB_DATA,
        'ACKB_DATA': ACKB_DATA,
        'CONB_DATA': CONB_DATA
    }

    dict_of_dict = {}

    for name, dictionary in dictionaries.items():
        if name in names:
            dict_of_dict[name] = dictionary

    return dict_of_dict


def log_checker(source_folder):
    """
    Given the source folder, it finds out the log files available
    """
    valid_files = []

    if os.path.isfile(source_folder):
        ext = os.path.splitext(source_folder)[-1].lower()
        if ext == '.log':
            return source_folder
        else:
            raise FileNotFoundError

    for file in os.listdir(source_folder):
        ext = os.path.splitext(os.path.join(source_folder, file))[-1].lower()
        if ext == '.log':
            valid_files.append(os.path.join(source_folder, file))

    print('Which file do you want to extract?\n')

    if len(valid_files) == 0:
        raise FileNotFoundError

    for i, valid_file in zip(range(1, len(valid_files) + 1), valid_files):
        print(str(i) + '    ' + valid_file)

    file_no = int(input('\n\nEnter file number to extract\t')) - 1

    while file_no >= len(valid_files) or file_no < 0:
        file_no = int(input(
            'Invalid input, enter a number between 1 and ' + str(len(valid_files))) + '\n') - 1

    return valid_files[file_no]


def buff_size_calc():
    tot_RAM = psutil.virtual_memory()[0]
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB

    if tot_RAM < 500 * MB:
        buff_size = 2500
    elif tot_RAM < GB:
        buff_size = 5000
    elif tot_RAM < 2 * GB:
        buff_size = 10000
    elif tot_RAM < 4 * GB:
        buff_size = 20000
    else:
        buff_size = tot_RAM // GB * 5000

    return buff_size

# def writer (dict_of_dicts, initial_towc_path, is_first_time):
#     assert isinstance(dict_of_dicts, dict)

#     if is_first_time:
#         mode = 'w'
#         header = True
#     else:
#         mode = 'a'
#         header = False

#     try:
#         create_path(initial_towc_path)
#         for name, lists in dict_of_dicts.items():
#             df = pd.DataFrame(data = lists)
#             df.to_csv(os.path.join(initial_towc_path, name + '.csv'), mode=mode, index=False, header=header)

#     except FileNotFoundError:
#         for name, lists in dict_of_dicts.items():
#             df = pd.DataFrame(data = lists)
#             df.to_csv(os.path.join(initial_towc_path, name + '.csv'), mode='w', index=False, header=True)


def using_temp_file(temp_file, text, method, dictionary, to_pass, thread_lock):
    # def using_temp_file(temp_file, text, method, dictionary, to_pass):
    with thread_lock:
        temp_file.seek(0)
        temp_file.write(text)
        temp_file.seek(0)
        method(temp_file, dictionary, to_pass)


def create_temp_file():
    temp = tempfile.TemporaryFile()
    return temp


def create_all_temp_files(names):
    files = {}
    assert isinstance(names, list)
    for name in names:
        files[name] = create_temp_file()
    files['header'] = create_temp_file()
    return files


def delete_all_temp_files(files):
    assert isinstance(files, dict)
    for file_name in files:
        files[file_name].close()


def thread_safe(names):
    assert isinstance(names, list)

    file_locks = {}

    for name in names:
        file_locks[name] = threading.Lock()

    return file_locks


def extract_header(file, text):
    file.seek(0)
    file.write(text)
    file.seek(0)
    chk_sum = struct.unpack('<B', file.read(1))[0]
    mes_iden = file.read(1)
    gnss_id = struct.unpack('<B', file.read(1))[0]
    mes_length = struct.unpack('<H', file.read(2))[0]
    towc = struct.unpack('<I', file.read(4))[0]
    rec_ns = struct.unpack('<I', file.read(4))[0]
    blk_ct = struct.unpack('<I', file.read(4))[0]
    sys_word_1 = struct.unpack('<I', file.read(4))[0]
    sys_word_2 = struct.unpack('<I', file.read(4))[0]
    sys_word_3 = struct.unpack('<H', file.read(2))[0]
    week_no = struct.unpack('<H', file.read(2))[0]

    to_pass = {
        'TOWC': towc,
        'Week_no': week_no,
        'Rec_ns': rec_ns,
        'Sys_stat_1': sys_word_1,
        'Sys_stat_2': sys_word_2,
        'Sys_stat_3': sys_word_3,
        'Block_ct': blk_ct
    }

    return to_pass, mes_iden, gnss_id, chk_sum, mes_length

# def reset_all_dicts(dict_of_dicts):
#     for dictionary_name in dict_of_dicts:
#         dict_of_dicts[dictionary_name] = reset_dict(dict_of_dicts[dictionary_name])

#     return dict_of_dicts


def find_dict_method(mes_iden, gnss_id):
    if mes_iden == b'\x01':
        assert gnss_id in (2, 3, 6)

        if gnss_id == 2:
            dict_key = 'SATB_IRNSS_L5_DATA'
            method = SATB_IRNSS

        if gnss_id == 3:
            dict_key = 'SATB_IRNSS_S1_DATA'
            method = SATB_IRNSS

        if gnss_id == 6:
            dict_key = 'SATB_GPS_L1_DATA'
            method = SATB_GPS

    elif mes_iden == b'\x02':
        assert gnss_id == 8
        dict_key = 'SBSATB_DATA'
        method = SBSATB

    elif mes_iden == b'\x03':
        assert gnss_id == 6
        dict_key = 'SBASCORR_DATA'
        method = SBASCORR

    elif mes_iden == b'\x04':
        assert gnss_id == 0
        dict_key = 'TIDB_DATA'
        method = TIDB

    elif mes_iden == b'\x06':
        assert gnss_id == 0
        dict_key = 'POSB_DATA'
        method = POSB

    elif mes_iden == b'\x07':
        assert gnss_id == 0
        dict_key = 'CLKB_DATA'
        method = CLKB

    elif mes_iden == b'\x08':
        assert gnss_id == 0
        dict_key = 'DOPB_DATA'
        method = DOPB

    elif mes_iden == b'\x0a':
        assert gnss_id in (2, 3, 6)
        if gnss_id == 2:
            dict_key = 'RNBB_IRNSS_L5_DATA'
        elif gnss_id == 3:
            dict_key = 'RNBB_IRNSS_S1_DATA'
        elif gnss_id == 6:
            dict_key = 'RNBB_GPS_L1_DATA'
        method = RNBB

    elif mes_iden == b'\x0b':
        assert gnss_id == 0
        dict_key = 'CONB_DATA'
        method = CONB

    elif mes_iden == b'\x0c':
        assert gnss_id == 0
        dict_key = 'IMB_DATA'
        method = IMB

    elif mes_iden == b'\x0f':
        assert gnss_id == 0
        dict_key = 'ACKB_DATA'
        method = ACKB

    return dict_key, method


def writer(dict_of_dicts, initial_towc_path, is_first_time, chk_sums):
    create_path(initial_towc_path)

    for file_name, dictionary in dict_of_dicts.items():
        if is_first_time:
            with open(os.path.join(initial_towc_path, file_name + '.csv'), 'w') as file_to_write:
                for header in dictionary:
                    file_to_write.write(header+', ')
                file_to_write.write('\b\b\n')
        with open(os.path.join(initial_towc_path, file_name + '.csv'), 'a') as file_to_write:
            for header in dictionary:
                length_of_list = len(dictionary[header])
                break
            for i in range(0, length_of_list):
                for header in dictionary:
                    file_to_write.write(str(dictionary[header][i])+', ')
                file_to_write.seek(file_to_write.tell(), 0)
                file_to_write.write('\n')

    with open(os.path.join(initial_towc_path, 'checksum.csv'), 'w') as file_to_write:
        for chk_sum in chk_sums:
            for i in chk_sum:
                file_to_write.write(str(i) + ', ')
            file_to_write.write('\n')
