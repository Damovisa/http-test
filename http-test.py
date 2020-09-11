import sys, os, time, getopt, logging, requests

def main(argv):
    target = 'https://www.google.com.au'
    frequency = 5
    outputfile = 'http-test.log'
    try:
        opts, args = getopt.getopt(
            argv, "ht:f:o:", ["target=", "frequency=", "outputfile="])
    except getopt.GetoptError:
        print('http-test.py -t <target url> -f <frequency> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('http-test.py -t <target url> -f <frequency> -o <outputfile>')
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-f", "--frequency"):
            frequency = int(arg)
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
    print('Target URL is ', target)
    print('Frequency is ', frequency, ' seconds')
    print('Output log file is ', outputfile)
    print("Press Ctrl-C to exit")

    # Write header to new log file
    if not os.path.isfile(outputfile):
        f = open(outputfile, "a")
        f.write("timestamp,id,target,response_size,elapsed_ms,status_code,message\n")
        f.close()

    # Set up logger
    logger = logging.getLogger('http-test')
    hdlr = logging.FileHandler(outputfile)
    formatter = logging.Formatter('%(asctime)s,%(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

    # Loop until exit
    try:
        while True:
            print(".", end="", flush=True)
            try:
                # timeout of frequency or 5 seconds, whichever is larger
                r = requests.get(target, timeout=max(5,frequency))

                logger.info('%s,%d,%.2f,%s',target, len(r.content), (r.elapsed.total_seconds()*1000), r.status_code)
                remainingtime = max(0,frequency-r.elapsed.total_seconds())
            except requests.exceptions.Timeout as et:
                logger.info('%s,%d,%.2f,%s,"%s"',target, 0, max(5,frequency), 0, et)
                remainingtime = max(frequency-max(5,frequency),0)
            except requests.exceptions.ConnectTimeout as ect:
                logger.info('%s,%d,%.2f,%s,"%s"',target, 0, max(5,frequency), 0, ect)
                remainingtime = max(frequency-max(5,frequency),0)
            except requests.exceptions.RequestException as er:
                logger.info('%s,%d,%.2f,%s,%s',target, 0, 0, 'N/A', er)
                remainingtime = frequency

            time.sleep(remainingtime)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
