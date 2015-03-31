import os
import struct
import json
#-*- coding: utf-8 -*-
#!/usr/bin/python


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
# hello
# start of the func that going aloing dir and searching qcow2 files


def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            filename = open(path, 'rb')

            def unpacker(karetka, howmany, form):
                filename.seek(int(karetka))
                output = filename.read(int(howmany))
                output = struct.unpack(str(form), output)
                return output
            about = unpacker(0, 4, '4s')
            if about == ('QFI\xfb',):
                backing_file_offset = unpacker(8, 8, '>Q')
                backing_file_size = unpacker(16, 4, '>I')
                virtual_size = unpacker(24, 8, '>Q')
                nb_snapshots = unpacker(60, 4, '>I')
                snapshots_offset = unpacker(64,8,'>Q')
                information = {"filename": path, "virtual_size": virtual_size}
                with open('info.json', 'w') as outfile:
                    json.dump(information, outfile)
                print (path)
                print (virtual_size)
                #if nb_snapshots != (0,):

                # print (snapshots_offset)
                if backing_file_offset != (0,):
                    backing_file_info=unpacker(backing_file_offset[0],backing_file_size[0],str(backing_file_size[0])+'s')
                    print (backing_file_info)

                # if backing_file_offset != (0,):
                # information.setdefault("backing_file", backing_file_offset)

            else:
                filename.close()
                pass

            filename.close()
        else:
            walk(path)

walk('/home/ilya/TESTQCOW/')
