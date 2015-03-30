import os
import struct
import json


"""
QCowHeader = struct('''> #big-endian
        4s  #uint32_t magic;
        I   #uint32_t version;
        Q   #uint64_t backing_file_offset;
        I   #uint32_t backing_file_size;
        I   #uint32_t cluster_bits;
        Q   #uint64_t size; /* in bytes */
        I   #uint32_t crypt_method;
        I   #uint32_t l1_size;
        Q   #uint64_t l1_table_offset;
        Q   #uint64_t refcount_table_offset;
        I   #uint32_t refcount_table_clusters;
        I   #uint32_t nb_snapshots;
        Q   #uint64_t snapshots_offset;
        ''')

QCowSnapshotHeader = struct('''> #big-endian
        Q   #uint64_t l1_table_offset;
        I   #uint32_t l1_size;
        H   #uint16_t id_str_size;
        H   #uint16_t name_size;
        I   #uint32_t date_sec;
        I   #uint32_t date_nsec;
        Q   #uint64_t vm_clock_nsec;
        I   #uint32_t vm_state_size;
        I   #uint32_t extra_data_size; /* for extension */
            #/* extra data follows */
            #/* id_str follows */
            #/* name follows  */
        ''')
"""

#start of the func that going aloing dir and searching qcow2 files
def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            try:
#
                filename = open(path, 'rb')
                filename.seek(0)
                about = filename.read(4)
                about = struct.unpack('4s', about)
                filename.seek(8)
                backing_file_offset = filename.read(8)
                backing_file_offset = struct.unpack('Q', backing_file_offset)
                filename.seek(24)
                virtual_size = filename.read(8)
                virtual_size = struct.unpack('>Q', virtual_size)
                filename.close
            except struct.error:
                pass
            if about == ('QFI\xfb',):
                information = {"filename": path, "virtual_size": virtual_size}
                if backing_file_offset != 0:
                    information.setdefault ("backing_file", backing_file_offset)
                with open('info.json', 'w') as outfile: json.dump(information, outfile)
                print (path)
                print (virtual_size)
                if backing_file_offset != (0,):
                    print (backing_file_offset)
        else:
            walk(path)
walk('/home/ilya/TESTQCOW')
