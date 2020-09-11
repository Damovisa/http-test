# Raspberry Pi HTTP Test
A simple looping HTTP request intended for use from a Raspberry Pi.

## Usage
`http-test.py -t <target url> -f <frequency> -o <output file>')`

*Target URL* should be a valid URL. Default is `https://google.com.au`.
*Frequency* is measured in seconds. Default is `5`.
*Output file* is the log file the results will be written to. Default is `http-test.log`.

## Notes
 - The greater of 5 seconds or `Frequency` is used as a timeout value for requests.
 - A best effort is made to perform a request according to the frequency specified. Slight drift isn't out of the question, however. 