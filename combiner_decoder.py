import threading
from queue import Queue
from combiner_utility import source_log, thread_safe, create_all_temp_files, buff_size_calc, initializer, using_temp_file, extract_header
from combiner_utility import files_to_save, current_time, get_path, writer, find_dict_method, delete_all_temp_files
import sys

no_of_threads = 1

file_to_open = source_log()

names = files_to_save()

file_locks = thread_safe(names)  # contains the lock for each file's thread
temp_files = create_all_temp_files(names)  # creates all the temporary files
# dynamically calculates the buffer size based on RAM
blk_buff_size = buff_size_calc()
dict_of_dicts = initializer(names)  # a dictionary of all dictionaries
chk_sums = []


first_in_set = True
is_first_time = True


def threader():
    while True:
        worker = q.get()
        using_temp_file(worker[0], worker[1], worker[2],
                        worker[3], worker[4], worker[5])
        q.task_done()


q = Queue()

for x in range(no_of_threads):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

current_time()

try:
    with open(file_to_open, 'rb') as file:
        opening_statement = file.read(7)

        if opening_statement != b'IRNSSUR':
            sys.exit()

        chk1 = file.read(1)
        chk2 = file.read(1)

        while chk1 != b'':
            while True:
                chk0 = chk1
                chk1 = chk2
                chk2 = file.read(1)

                if (chk0 == b'\xac') and (chk1 == b'\xc0') and (chk2 == b'\xcd'):
                    break
                if chk0 == b'' and chk1 == b'' and chk2 == b'':
                    raise EOFError

            to_pass, mes_iden, gnss_id, chk_sum, mes_length = extract_header(
                temp_files['header'], file.read(29))
            chk_sums.append([chk_sum, mes_iden])

            towc = to_pass['TOWC']
            week_no = to_pass['Week_no']
            blk_ct = to_pass['Block_ct']

            if first_in_set:
                final_blk_ct = blk_ct + blk_buff_size
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

            if dict_key in names:
                q.put([temp_files[dict_key], file.read(mes_length - 32), method,
                       dict_of_dicts[dict_key], to_pass, file_locks[dict_key]])
            else:
                file.read(mes_length - 32)
            # using_temp_file(temp_files[dict_key], file.read(mes_length - 32), method, dict_of_dicts[dict_key], to_pass)

            chk1 = file.read(1)
            chk2 = file.read(1)

except EOFError:
    pass

finally:
    writer(dict_of_dicts, initial_towc_path, is_first_time, chk_sums)
    dict_of_dicts = initializer(names)
    delete_all_temp_files(temp_files)

q.join()

current_time()
