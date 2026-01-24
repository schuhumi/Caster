import configparser
import argparse
import csv
import os


def process_table(fn, newfn):
    table = {}
    with open(fn, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in csvreader:
            dst = i
            seq = row[0:-1]
            table[dst] = seq
            i += 1
    fc = len(table[0])
    print(f'Frame count {fc}')
    with open(newfn, 'wb') as binfile: 
        for i in range(fc):
            for dst in range(8):
                d1 = int(table[dst*2][i])
                d2 = int(table[dst*2+1][i])
                d = (d2 << 4 | d1).to_bytes(1)
                binfile.write(d)

def main():
    parser = argparse.ArgumentParser(prog='wvfm_converter')
    parser.add_argument('filename')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.filename)
    #print(config.sections())

    version = config['WAVEFORM']['VERSION']
    if version != '2.0U':
        raise Exception("Input needs to be a unidirection waveform")
    prefix = config['WAVEFORM']['PREFIX']
    # name = config['WAVEFORM']['NAME']
    bpp = int(config['WAVEFORM']['BPP'])
    if bpp != 4:
        raise Exception("Input needs to be an 4bpp waveform")
    modes = int(config['WAVEFORM']['MODES'])
    temps = int(config['WAVEFORM']['TEMPS'])
    tables = int(config['WAVEFORM']['TABLES'])

    # Get all framecounts
    # fc = []
    # for i in range(tables):
    #     fc.append(config['WAVEFORM'][f'TB{i}FC'])

    # trange = []
    # for i in range(temps):
    #     trange.append(config['WAVEFORM'][f'T{i}RANGE'])

    dirname = os.path.dirname(os.path.abspath(args.filename))

    for i in range(tables):
        oldname = f'{prefix}_TB{i}.csv'
        newname = f'{prefix}_TB{i}.bin'
        process_table(os.path.join(dirname, oldname),
                      os.path.join(dirname, newname))

if __name__ == "__main__":
    main()