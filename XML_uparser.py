import math
import os
import timeit
import multiprocessing as mp


def process_wrapper(chunkStart, chunkSize, limitWrite, file_index, tag, tag_len, ):
    with open("dblp.xml", 'r') as f:
        with open(f"splits/dblp_parsed{file_index}.xml", "w+") as fo:
            block = ''
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()
            line_index = 0
            for line in lines:
                if line[:tag_len] == tag:
                    block += f'{line}\n'
                    line_index += 1
                if line_index == limitWrite:
                    fo.write('{:s}\n'.format(block))
                    line_index = 0
                    block = ''
            fo.write('{:s}\n'.format(block))  # write last block
            fo.close()
    f.close()


def chunkify(filein, size=1024 * 1024):
    inputFileEnd = os.path.getsize(filein)
    with open(filein, 'rb') as fi:
        inputChunkEnd = fi.tell()
        while True:
            inputChunkStart = inputChunkEnd
            fi.seek(size, 1)
            fi.readline()
            inputChunkEnd = fi.tell()
            yield inputChunkStart, inputChunkEnd - inputChunkStart
            if inputChunkEnd > inputFileEnd:
                break
    fi.close()


if __name__ == '__main__':
    start = timeit.default_timer()

    # mp objects
    pool = mp.Pool(12)
    jobs = []

    # filein-related
    filein = "dblp.xml"
    tag = '<title>'
    tag_len = len(tag)

    # fileout-related
    file_index = 0

    # parameters
    limit = 200
    fileNb = 200
    chunk = math.ceil(os.path.getsize(filein) / fileNb)

    # create jobs
    for chunkStart, chunkSize in chunkify(filein, chunk):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize, limit, file_index, tag, tag_len)))
        file_index += 1

    # wait for all jobs to finish
    for job in jobs:
        job.get()

    # clean up
    pool.close()

    stop = timeit.default_timer()
    print(f'MultiProcessing -> Parse time: {stop - start}')
