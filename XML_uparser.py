import os
import math
import timeit
import argparse
import multiprocessing as mp


def process_wrapper(chunkStart, chunkSize, limitWrite, outdir, file_index, tag, tag_len):
    with open("dblp.xml", 'r') as f:
        with open(f"{outdir}/dblp_parsed{file_index}.xml", "w+") as fo:
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

    # menu
    parser = argparse.ArgumentParser(description='UParser is an XML large file parser written in python 3.7')
    parser.add_argument('-p', dest='cores', action='store', default=12, type=int,
                        help='maximum number of processes running at the same time (default: 12)')
    parser.add_argument('-m', dest='writeLimit', action='store', default=200, type=int,
                        help='maximum number of lines each process can write at a time (default: 200)')
    parser.add_argument('-n', dest='outFileNb', action='store', default=200, type=int,
                        help='maximum number of output files (default: 200)')
    parser.add_argument('outDir', action='store', type=str,
                        help='output directory')
    parser.add_argument('tag', action='store', type=str,
                        help='tag to retrieve')
    parser.add_argument('inputFile', action='store', type=str,
                        help='input filename')
    args = parser.parse_args()

    start = timeit.default_timer()

    # mp objects
    pool = mp.Pool(args.cores)
    jobs = []

    # filein-related
    filein = args.inputFile
    tag = args.tag
    tag_len = len(tag)

    # fileout-related
    file_index = 0

    # parameters
    limit = args.writeLimit
    fileNb = args.outFileNb
    chunk = math.ceil(os.path.getsize(filein) / fileNb)

    # creating outdir
    if not os.path.exists(args.outDir):
        os.mkdir(args.outDir)
    outdir = args.outDir

    # create jobs
    for chunkStart, chunkSize in chunkify(filein, chunk):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize, limit, outdir, file_index, tag, tag_len)))
        file_index += 1

    # wait for all jobs to finish
    for job in jobs:
        job.get()

    # clean up
    pool.close()

    stop = timeit.default_timer()
    print(f'MultiProcessing -> Parse time: {stop - start}')
