import socket
import os
import threading
from queue import Queue
from combiner_utility import source_log, thread_safe, create_all_temp_files, buff_size_calc, initializer, using_temp_file, extract_header
from combiner_utility import files_to_save, current_time, get_path, writer, find_dict_method, delete_all_temp_files, datetime
import sys

no_of_threads = 2  # number of threads we want in our queue

# for tcp connection with IGSRx
TCP_IP = '192.168.0.146'  # default ip which the receiver looks for
TCP_PORT = 2000  # default port for tcp comm. with receiver

# Multithreading to stop the capture
stop = 0  # if we need to stop capturing


def stop_capture():
    global stop
    a = str(input())  # accepting user interupt to stop capture
    if a.lower().rstrip().lstrip():
        stop = 1
    else:
        pass


names = files_to_save()  # gets user input on the files they want to save

# setting up the tcp connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
print("\nWaiting for IRNSS reciever to connect...\n")
s.listen(1)
conn, addr = s.accept()
print('Connection established with IRNSS reciever at:' + str(addr))

# Printing other useful info about the ongoing capture
date = datetime.now()
print("\nData logging started at : " + str(date)+'\n')  # start time of capture
print("Type 'stop' to stop\n")  # prompt for method to end the capture
fcounter = -1

file_locks = thread_safe(names)  # contains the lock for each file's thread
temp_files = create_all_temp_files(names)  # creates all the temporary files
# dynamically calculates the buffer size based on RAM
blk_buff_size = buff_size_calc()
dict_of_dicts = initializer(names)  # a dictionary of all dictionaries
# file = create_temp_file()  # a temp file to simulate the .log file

first_in_set = True
is_first_time = True

chk_sums = []

def threader():
    while True:
        worker = q.get()
        using_temp_file(worker[0], worker[1], worker[2],
                        worker[3], worker[4], worker[5])
        q.task_done()


q = Queue()

# Multithreading to stop the capture

for x in range(no_of_threads):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


try:
    t1 = threading.Thread(target=stop_capture, args=())
    t1.start()
    chk1 = conn.recv(1)
    chk2 = conn.recv(1)

    while chk1 != b'' and not stop:
        while True:
            chk0 = chk1
            chk1 = chk2
            chk2 = conn.recv(1)

            if (chk0 == b'\xac') and (chk1 == b'\xc0') and (chk2 == b'\xcd'):
                break
            if chk0 == b'' and chk1 == b'' and chk2 == b'':
                raise EOFError

        to_pass, mes_iden, gnss_id, chk_sum, mes_length = extract_header(
            temp_files['header'], conn.recv(29))

        towc = to_pass['TOWC']
        week_no = to_pass['Week_no']
        blk_ct = to_pass['Block_ct']

        if first_in_set:
            final_blk_ct = blk_ct + blk_buff_size
            week_no = week_no
            initial_week_no = week_no
            time_diff = 604800 * initial_week_no
            initial_towc_path, final_towc = get_path(towc, week_no)
            first_in_set = False

        if week_no - initial_week_no == 1024:
            week_no = initial_week_no

        if blk_ct >= final_blk_ct or towc >= final_towc - time_diff:
            writer(dict_of_dicts, initial_towc_path, is_first_time, chk_sums)

            if is_first_time:
                is_first_time = False

            if towc >= final_towc - time_diff:
                is_first_time = True
                initial_towc_path, final_towc = get_path(towc, week_no)

                if (final_towc - time_diff) // 604800 == 1:
                    initial_week_no += 1
                    time_diff = 604800 * initial_week_no

            final_blk_ct = blk_ct + blk_buff_size

            dict_of_dicts = initializer(names)

        dict_key, method = find_dict_method(mes_iden, gnss_id)

        data = conn.recv(mes_length - 32)
        if not data:
            break

        if dict_key in names:
            q.put([temp_files[dict_key], data, method,
                   dict_of_dicts[dict_key], to_pass, file_locks[dict_key]])

        chk1 = conn.recv(1)
        chk2 = conn.recv(1)

except EOFError:
    pass

finally:
    writer(dict_of_dicts, initial_towc_path, is_first_time, chk_sums)
    dict_of_dicts = initializer(names)
    delete_all_temp_files(temp_files)
    conn.close()

q.join()
current_time()
