import struct

def message_hdr(command_type, gnss_type, set_default=0):
    """
    To create the message header from the command, gnss_type, and set_default token
    Parameters:
        command_type -- String specifying the command type (Ref ICD-A14SACIRNSUR)
        gnss_type -- String (one of 'IRNSS_L5', 'IRNSS_S1', 'GPS_L1', 'SBAS') naming the
            constellation of satellites
        set_default -- To save or not to save as the default setting (0 for false and 1 for true)
    Returns:
        message_identifier -- binary string with command type
        mes_length -- length of the message
        gnss_id -- gnss id corresponding to the gnss_type
        set_default -- same as parameter
    """

    if command_type == 'SETSTATE':
        message_identifier = b'\x50'
        gnss_id = 0
        mes_length = 10

    elif command_type == 'ADDPRN':
        message_identifier = b'\x51'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        mes_length = 12

    elif command_type == 'NMEAN':
        message_identifier = b'\x52'
        if gnss_type in ('IRNSS_L5', 'IRNSS_S1', 'GPS_L1'):
            gnss_id = 0
        mes_length = 13

    elif command_type == 'ASSIGN':
        message_identifier = b'\x53'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 11

    elif command_type == 'EXCSAT':
        message_identifier = b'\x54'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 11

    elif command_type == 'IONMODEL':
        message_identifier = b'\x55'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 10

    elif command_type == 'TROPOMODEL':
        message_identifier = b'\x56'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 10

    elif command_type == 'POSFIX':
        message_identifier = b'\x66'
        if gnss_type in ('IRNSS_L5', 'IRNSS_S1', 'GPS_L1'):
            gnss_id = 0
        mes_length = 33

    elif command_type == 'SRESET':
        message_identifier = b'\x57'
        gnss_id = 0
        mes_length = 10

    elif command_type == 'POSSEL':
        message_identifier = b'\x58'
        if gnss_type in ('IRNSS_L5', 'IRNSS_S1', 'GPS_L1'):
            gnss_id = 0
        mes_length = 12

    elif command_type == 'DPBNEB':
        message_identifier = b'\x5a'
        if gnss_type in ('IRNSS_L5', 'IRNSS_S1'):
            gnss_id = 1
        mes_length = 10

    elif command_type == 'SBASEN':
        message_identifier = b'\x5b'
        if gnss_type == 'SBAS':
            gnss_id = 8
        mes_length = 10

    elif command_type == 'ETHPRT':
        message_identifier = b'\x5e'
        gnss_id = 0
        mes_length = 27

    elif command_type == 'CWMEN':
        message_identifier = b'\x5f'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 10

    elif command_type == 'PRORFDEL':
        message_identifier = b'\x63'
        if gnss_type == 'IRNSS_L5':
            gnss_id = 2
        elif gnss_type == 'IRNSS_S1':
            gnss_id = 3
        elif gnss_type == 'GPS_L1':
            gnss_id = 6
        mes_length = 14

    elif command_type == 'REFOUT':
        message_identifier = b'\x64'
        gnss_id = 0
        mes_length = 10

    elif command_type == 'ANTPWR':
        message_identifier = b'\x65'
        gnss_id = 0
        mes_length = 10

    elif command_type == 'SETMASK':
        message_identifier = b'\x67'
        gnss_id = 0
        mes_length = 13

    elif command_type == 'DATARATE':
        message_identifier = b'\x5c'
        gnss_id = 0
        mes_length = 10

    elif command_type == 'TIMEIN':
        message_identifier = b'\x59'
        gnss_id = 0
        mes_length = 15

    elif command_type == 'MSGSELECT':
        message_identifier = b'\x69'
        gnss_id = 0
        mes_length = 13

    elif command_type == 'CLKSTEERING':
        message_identifier = b'\x6b'
        if gnss_type in ('IRNSS_L5', 'IRNSS_S1', 'GPS_L1'):
            gnss_id = 0
        mes_length = 10

    elif command_type == 'ETHPROTOCOL':
        message_identifier = b'\x6e'
        gnss_id = 0
        mes_length = 10

    gnss_id = struct.pack('>B', gnss_id)
    mes_length = struct.pack('>H', mes_length)
    set_default = struct.pack('>B', set_default)
    return message_identifier, mes_length, gnss_id, set_default


def SETSTATE_INPUT():
    recv_state = input(
        'To set as Maintenance type 1, to set as Operational type any other key\t')

    if recv_state == '1':
        recv_state = 'Maintenance'
    else:
        recv_state = 'Operational'

    return SETSTATE('IRNSS_L5', recv_state, 0)


def SETSTATE(gnss_type, recv_state, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('SETSTATE', gnss_type, set_default)
    if recv_state == 'Operational':
        sync = b'\xac\xc0\xcd'
        rest_of_message = mes_iden+mes_len+gnss_id+set_def+struct.pack('>B', 0)
    if recv_state == 'Maintenance':
        sync = b'\xac\xc0\xcd'
        rest_of_message = mes_iden+mes_len+gnss_id+set_def+struct.pack('>B', 2)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def ADDPRN_INPUT():

    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        else:
            print('Invalid input')

    while True:
        PRN = int(input('Enter PRN number in range 8 to 11\t'))
        if PRN not in range(8, 11):
            print('Invalid input')
        else:
            break

    while True:
        G2_Delay = int(input('Enter the G2 Shift register value (0-1023)\t'))
        if G2_Delay not in range(0, 1024):
            print('Invalid input')
        else:
            break

    set_default = input(
        'Do you want to set this PRN to be added by default (y/n)\t')

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return ADDPRN(gnss_type, PRN, G2_Delay, set_default)


def ADDPRN(gnss_type, PRN, G2_Delay, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('ADDPRN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', PRN)+struct.pack('>H', G2_Delay)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def NMEAN_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    NMEAN_en = input(
        'Do you want to enable NMEA message transmission? (y/n)\t')

    if NMEAN_en.lower() == 'y':
        NMEAN_en = 1
    else:
        NMEA_en = 0

    send_all = input('Do you want to get all the messages? (y/n)\t')

    if send_all.lower() == 'y':
        for i in range(0, 8):
            NMEA_mes_sel += 2 ** i
    else:
        to_ask = ['PVT Messages', 'RMC Message', 'ZDA Message',
                  'GGA Message', 'VTG Message', 'GSV Message', 'GSA Message']
        NMEA_mes_sel = 0
        for item, index in zip(to_ask, range(1, 8)):
            use_en = input('Do you want to get %s? (y/n)\t' % (item))
            if use_en.lower() == 'y':
                NMEA_mes_sel += 2**index

    baud_rates = [230400, 115200, 57600, 38400, 19200, 9600]

    NMEA_baud_sel = 0
    for rate, index in zip(baud_rates, range(0, 6)):
        if input('Do you want to set baud rate %d? (y,n)\t' % (rate)).lower() == 'y':
            NMEA_baud_sel = 2 ** index
            break

    if NMEA_baud_sel == 0:
        print('Setting baud rate to 4800')
        NMEA_baud_sel = 2 ** 6

    NMEA_data_sel = 0

    if input('Do you want to set data rate as 5Hz? (y/n)\t').lower() == 'y':
        NMEA_data_sel = 1

    set_default = input('Do you want to save this settings for NMEA? (y/n)\t')

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return NMEAN(gnss_type, NMEA_en, NMEA_mes_sel, NMEA_baud_sel, NMEA_data_sel, set_default)


def NMEAN(gnss_type, NMEA_en, NMEA_mes_sel, NMEA_baud_sel, NMEA_data_sel, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('NMEAN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', NMEA_en)+struct.pack('>B', NMEA_mes_sel) +\
        struct.pack('>B', NMEA_baud_sel)+struct.pack('>B', NMEA_data_sel)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def ASSIGN_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    if input('Do you want to change setting for all satellites? (y/n)\t').lower() == 'y':
        channel_number = 2 ** 8 - 1

    elif gnss_type in ('IRNSS_L5', 'IRNSS_S1'):
        while True:
            channel_number = int(input('Select channel number (1-11) \t'))
            if channel_number in range(1, 12):
                break
            else:
                print('Invalid input')

    else:
        while True:
            channel_number = int(input('Select channel number (1-12) \t'))
            if channel_number in range(1, 13):
                break
            else:
                print('Invalid input')

    if input('Do you want to set as idle? (y/n)\t').lower() == 'y':
        idle_free_prn = 2 ** 8 - 1

    elif input('Do you want to set as free? (y/n)\t').lower() == 'y':
        idle_free_prn = 2 ** 8 - 2

    elif gnss_type in ('IRNSS_L5', 'IRNSS_S1'):
        while True:
            idle_free_prn = int(
                input('Select PRN number (1-11) to assign to the channel\t'))
            if idle_free_prn in range(1, 12):
                break
            else:
                print('Invalid input')

    else:
        while True:
            idle_free_prn = int(
                input('Select PRN number (1-32) to assign to the channel\t'))
            if idle_free_prn in range(1, 33):
                break
            else:
                print('Invalid input')

    set_default = input(
        'Do you want to save this settings as default? (y/n)\t')

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return ASSIGN(gnss_type, channel_number, idle_free_prn, set_default)


def ASSIGN(gnss_type, channel_number, idle_free_prn, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('ASSIGN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', channel_number)+struct.pack('>B', idle_free_prn)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def EXCSAT_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    if input('Do you want to change setting for all satellites? (y/n)\t').lower() == 'y':
        PRN = 2 ** 8 - 1

    elif gnss_type in ('IRNSS_L5', 'IRNSS_S1'):
        while True:
            PRN = int(input('Select PRN number (1-11) \t'))
            if PRN in range(1, 12):
                break
            else:
                print('Invalid input')

    else:
        while True:
            PRN = int(input('Select PRN number (1-32) \t'))
            if PRN in range(1, 33):
                break
            else:
                print('Invalid input')

    if input('Do you want to include?').lower().strip() == 'y':
        incl = 'Yes'
    else:
        incl = 'No'

    set_default = input(
        'Do you want to save this settings as default? (y/n)\t')

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return EXCSAT(gnss_type, incl, PRN, set_default)


def EXCSAT(gnss_type, incl, PRN, set_default=0):
    """
        If for all put PRN = 0XFF
    """
    sync = b'\xac\xc0\xcd'
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('EXCSAT', gnss_type, set_default)

    if incl == 'Yes':
        rest_of_message = mes_iden+mes_len+gnss_id +\
            set_def+struct.pack('>B', 1)+struct.pack('>B', PRN)
    else:
        rest_of_message = mes_iden+mes_len+gnss_id +\
            set_def+struct.pack('>B', 2)+struct.pack('>B', PRN)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def IONMODEL_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    if input('Do you want to enable? (y/n)\t').lower().strip() == 'y':
        enable = 1
    else:
        enable = 0

    set_default = input(
        'Do you want to save this settings as default? (y/n)\t').strip()

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return IONMODEL(gnss_type, enable, set_default)


def IONMODEL(gnss_type, enable, set_default=0):
    """
        0-Disable
        1-Enable
    """
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('IONMODEL', gnss_type, set_default)
    assert enable in (0, 1)
    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id +\
        set_def+struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def TROPOMODEL_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    if input('Do you want to enable tropomodel? (y/n)\t').lower().strip() == 'y':
        enable = 1
    else:
        enable = 0

    set_default = input(
        'Do you want to save this settings as default? (y/n)\t').strip()

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return TROPOMODEL(gnss_type, enable, set_default)


def TROPOMODEL(gnss_type, enable, set_default=0):
    """
        0-Disable
        1-Enable
    """
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('TROPOMODEL', gnss_type, set_default)
    assert enable in (0, 1)
    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id +\
        set_def+struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def POSFIX_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    while True:
        lat = float(input('Enter the fixed latitude!\t'))
        if lat >= -90 and lat <= 90:
            break

    while True:
        long = float(input('Enter the fixed longitude!\t'))
        if long >= -180 and long <= 180:
            break

    while True:
        alt = float(input('Enter the fixed altitude!\t'))
        if alt >= -1000 and alt <= 2000:
            break

    set_default = input(
        'Do you want to save this settings as default? (y/n)\t').strip()

    if set_default.lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return POSFIX(gnss_type, lat, long, alt, set_default)


def POSFIX(gnss_type, lat, long, alt, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('POSFIX', gnss_type, set_default)

    assert lat < 90 and lat > -90
    assert lat < 180 and lat > -180
    assert alt < 20000 and alt > -10000

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>d', lat)+struct.pack('>d', long) +\
        struct.pack('>d', alt)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def SRESET_INPUT():
    gnss_type = 'IRNSS_L5'

    if input('Are you sure you want to reset to factory default? (y/n)\t').strip().lower() == 'y':
        restore = 1
    else:
        restore = 0

    return SRESET(gnss_type, restore)


def SRESET(gnss_type, restore, set_default=0):
    """
        0 - user set config
        1 - factory defaults
    """
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('SRESET', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', restore)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def POSSEL_INPUT():
    gnss_type = 'IRNSS_L5'
    while True:
        config_gnss = int(input('Enter 1. IRNSS-L5 + IRNSS-S1\t2. IRNSS-L5\t3. IRNSS-S1\n\
                            4. IRNSS-L5 + GPS-L1\t5. IRNSS-S1 + GPS-L1\t6. GPS-L1\n\
                            7. IRNSS-GPS'))
        if config_gnss in range(1, 8):
            break

    if input('Do you want to enable dual IRNSS mode? (y/n)\t').strip().lower() == 'y':
        dual_mode = 1
    else:
        dual_mode = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return POSSEL(gnss_type, config_gnss, dual_mode, set_default)


def POSSEL(gnss_type, config_gnss, dual_mode, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('POSSEL', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', config_gnss)+struct.pack('>B', 1) +\
        struct.pack('>B', dual_mode)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message

def DPBENB_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break
    
    if input('Do you want to enable digital pulse banking? (y/n)\t').strip().lower() == 'y':
        enable = 1
    else:
        enable = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1

    else:
        set_default = 0

    return DPBENB(gnss_type, enable, set_default)



def DPBENB(gnss_type, enable, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('DPBENB', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def SBASEN_INPUT():
    gnss_type = 'SBAS'

    if input('Do you want to enable GPS position with SBAS? (y/n)\t').strip().lower() == 'y':
        enable = 1
    else:
        enable = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return SBASEN(gnss_type, enable, set_default)


def SBASEN(gnss_type, enable, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('SBASEN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def ETHPRT_INPUT():
    gnss_type = 'IRNSS_L5'

    recv_ip = input('Enter receiver ip address:\t').strip()
    recv_ip = recv_ip.split('.')
    for ip_part, i in zip(recv_ip, range(4)):
        recv_ip[i] = int(ip_part)
        assert recv_ip[i] in range(256)
    
    sub_net_mask = input('Enter subnet mask:\t').strip()
    sub_net_mask = sub_net_mask.split('.')
    for mask_part, i in zip(sub_net_mask, range(4)):
        sub_net_mask[i] = int(mask_part)
        assert sub_net_mask[i] in range(256)
    
    gateway = input('Enter subnet mask:\t').strip()
    gateway = gateway.split('.')
    for gateway_part, i in zip(gateway, range(4)):
        gateway[i] = int(gateway_part)
        assert gateway[i] in range(256)

    host_ip = input('Enter subnet mask:\t').strip()
    host_ip = host_ip.split('.')
    for host_part, i in zip(host_ip, range(4)):
        host_ip[i] = int(host_part)
        assert host_ip[i] in range(256)

    while True:
        port = int(input('Enter the port number (1024 to 65535)\t').strip())
        if port >= 1024 and port <= 65535:
            break
    
    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0
    
    return ETHPRT(gnss_type, recv_ip, sub_net_mask, gateway, host_ip, port, set_default)


def ETHPRT(gnss_type, recv_ip, sub_net_mask, gateway, host_ip, port, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('ETHPRT', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', recv_ip[0]) + struct.pack('>B', recv_ip[1]) +\
        struct.pack('>B', recv_ip[2]) + struct.pack('>B', recv_ip[3]) +\
        struct.pack('>B', sub_net_mask[0]) + struct.pack('>B', sub_net_mask[1]) +\
        struct.pack('>B', sub_net_mask[2]) + struct.pack('>B', sub_net_mask[3]) +\
        struct.pack('>B', gateway[0]) + struct.pack('>B', gateway[1]) +\
        struct.pack('>B', gateway[2]) + struct.pack('>B', gateway[3]) +\
        struct.pack('>B', host_ip[0]) + struct.pack('>B', host_ip[1]) +\
        struct.pack('>B', host_ip[2]) + struct.pack('>B', host_ip[3]) +\
        struct.pack('>H', port)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def CWMEN_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    if input('Do you want to enable Comtinuous Wave Mitigation? (y/n)\t').strip().lower() == 'y':
        enable = 1
    else:
        enable = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return CWMEN(gnss_type, enable, set_default)


def CWMEN(gnss_type, enable, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('CWMEN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def PRORFDEL_INPUT():
    while True:
        gnss_type = int(input('Enter\n1)IRNSS_L5\t2)IRNSS_S1\t3)GPS_L1\t'))

        if gnss_type == 1:
            gnss_type = 'IRNSS_L5'
            break

        elif gnss_type == 2:
            gnss_type = 'IRNSS_S1'
            break

        elif gnss_type == 3:
            gnss_type = 'GPS_L1'
            break

    while True:
        RF_delay = float(input('Enter RF delay between 0 and 1000!\t'))

        if RF_delay <= 1000 and RF_delay >=0:
            break
    
    while True:
        device = int(input('Enter device to set delay for\n1)LNA\t2)Cable\t3)Receiver\t'))
        if device in (1, 2, 3):
            break
    
    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0 
    
    return PRORFDEL(gnss_type, RF_delay, device, set_default)


def PRORFDEL(gnss_type, RF_delay, device, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('PRORFDEL', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>f', RF_delay), struct.pack('>B', device)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def REFOUT_INPUT():
    gnss_type = 'IRNSS_L5'

    while True:
        output_type = int(input('Enter Reference type\n0)1PPS out\t1)10Mhz out\t'))
        if output_type in (0, 1):
            break
    
    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0 

    return REFOUT(gnss_type, output_type, set_default)


def REFOUT(gnss_type, output_type, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('REFOUT', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id + set_def +\
        struct.pack('>B', output_type)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def ANTPWR_INPUT():
    gnss_type = 'IRNSS_L5'

    if input('Do you want to enable power to antenna? (y/n)\t').strip().lower() == 'y':
        enable = 1
    else:
        enable = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return ANTPWR(gnss_type, enable, set_default) 


def ANTPWR(gnss_type, enable, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('ANTPWR', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def SETMASK_INPUT():
    gnss_type = 'IRNSS_L5'

    while True:
        angle = float(input('Enter the mask angle in degrees!\t'))
        if angle >= 0 and angle <= 90:
            break

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return SETMASK(gnss_type, angle, set_default)   


def SETMASK(gnss_type, angle, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('SETMASK', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'
    assert angle > 0 and angle < 90

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>f', angle)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def DATARATE_INPUT():
    gnss_type = 'IRNSS_L5'
    
    while True:
        rate = int(input('Enter\n0)1 Hz\t1)5Hz')) 
        if rate in (0, 1):
            break
    
    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0
    
    return DATARATE(gnss_type, rate, set_default)


def DATARATE(gnss_type, rate, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('DATARATE', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', rate)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def TIMEIN_INPUT():
    gnss_type = 'IRNSS_L5'

    while True:
        week_no = int(input('Enter the week number (0-1023)!\t'))
        if week_no >= 0 and week_no <=1023:
            break
    
    while True:
        TOWC = int(input('Enter Time of Week Count (in seconds)!\t'))
        if TOWC >= 0 and TOWC <= 60799:
            break

    return TIMEIN(gnss_type, week_no, TOWC)


def TIMEIN(gnss_type, week_no, TOWC, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('TIMEIN', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>H', week_no) + struct.pack('>I', TOWC)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def MSGSELECT_INPUT():
    gnss_type = 'IRNSS_L5'

    messages = ['SATB - GPS L1', 'SATB - IRNSS L5', 'SATB - IRNSS S1', 'SBSATB', 'SBASCORR', 'POSB', \
        'TIDB', 'CLKB', 'DOPB', 'CONB', 'RNBB - GPS L1', 'RNBB - IRNSS L5', 'RNBB - IRNSS S1', 'IMB']
    
    select_key = 0

    for message, num in zip(messages, range(len(message))):
        if input('Do you want to recieve %s file? (y/n)').strip().lower() == 'y':
            select_key = select_key + 2**num 
    
    return MSGSELECT(gnss_type, select_key)


def MSGSELECT(gnss_type, select_key, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('MSGSELECT', gnss_type, set_default)

    print(mes_iden)
    print(mes_len + gnss_id + set_def)
    sync = b'\xac\xc0\xcd'

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>I', select_key)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def CLKSTEERING_INPUT():
    gnss_type = 'IRNSS_L5'

    if input('Do you want to enable clock steering? (y/n)\t').strip().lower() == 'y':
        enable = 1
    else:
        enable = 0

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return CLKSTEERING(gnss_type, enable, set_default) 


def CLKSTEERING(gnss_type, enable, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('CLKSTEERING', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', enable)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def ETHPROTOCOL_INPUT():
    gnss_type = 'IRNSS_L5'

    while True:
        ep_type = int(input('Enter\n0)UDP\t1)TCP')) 
        if ep_type in (0, 1):
            break

    if input('Do you want to save this settings as default? (y/n)\t').strip().lower() == 'y':
        set_default = 1
    else:
        set_default = 0

    return ETHPROTOCOL(gnss_type, ep_type, set_default) 


def ETHPROTOCOL(gnss_type, ep_type, set_default=0):
    mes_iden, mes_len, gnss_id, set_def \
        = message_hdr('ETHPROTOCOL', gnss_type, set_default)

    sync = b'\xac\xc0\xcd'

    if ep_type == 'TCP':
        ep_type = 1
    else:
        ep_type = 0

    rest_of_message = mes_iden+mes_len+gnss_id+set_def +\
        struct.pack('>B', ep_type)

    chk_sum = check_sum_gen(sync, rest_of_message)
    message = sync+chk_sum+rest_of_message

    return message


def check_sum_gen(sync, rest_of_message):
    xor_test = sync + rest_of_message
    chk_sum = 0
    for i in xor_test:
        chk_sum = chk_sum ^ i
    print(struct.pack('>B', chk_sum))
    return struct.pack('>B', chk_sum)


def command_request():
    command_types = ['ETHPRT', 'SETSTATE', 'ASSIGN', 'EXCSAT',\
            'DPBENB', 'IONMODEL', 'TROPOMODEL', 'SRESET', 'POSFIX',\
            'POSSEL', 'NMEAN', 'SBASEN', 'CWMEN', 'PRORFDEL', 'REFOUT',\
            'REFOUT', 'ANTPWR', 'SETMASK', 'DATARATE', 'TIMEIN',\
            'MSGSELECT', 'CLKSTEERING', 'ETHPROTOCOL']
    print('Enter the following numbers for the following commands:\n')
    for i, command_type in zip(range(len(command_types), command_types)):
        print('%d) %s \n' %(i, command_type))
    
    command_int = int(input())
    
    command_type = command_types[command_int]

    if command_type == 'ETHPRT':
        return ETHPRT_INPUT
    elif command_type == 'SETSTATE':
        return SETSTATE_INPUT
    elif command_type == 'ASSIGN':
        return ASSIGN_INPUT
    elif command_type == 'EXCSAT':
        return EXCSAT_INPUT
    elif command_type == 'DPBENB':
        return DPBENB_INPUT
    elif command_type == 'IONMODEL':
        return IONMODEL_INPUT
    elif command_type == 'TROPOMODEL':
        return TROPOMODEL_INPUT
    elif command_type == 'SRESET':
        return SRESET_INPUT
    elif command_type == 'POSFIX':
        return POSFIX_INPUT
    elif command_type == 'POSSEL':
        return POSSEL_INPUT
    elif command_type == 'NMEAN':
        return NMEAN_INPUT
    elif command_type == 'SBASEN':
        return SBASEN_INPUT
    elif command_type == 'CWMEN':
        return CWMEN_INPUT
    elif command_type == 'PRORFDEL':
        return PRORFDEL_INPUT
    elif command_type == 'REFOUT':
        return REFOUT_INPUT
    elif command_type == 'ANTPWR':
        return ANTPWR_INPUT
    elif command_type == 'SETMASK':
        return SETMASK_INPUT
    elif command_type == 'DATARATE':
        return DATARATE_INPUT
    elif command_type == 'TIMEIN':
        return TIMEIN_INPUT
    elif command_type == 'MSGSELECT':
        return MSGSELECT_INPUT
    elif command_type == 'CLKSTEERING':
        return CLKSTEERING_INPUT
    elif command_type == 'ETHPROTOCOL':
        return ETHPROTOCOL_INPUT
    