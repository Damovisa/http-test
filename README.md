# Raspberry Pi HTTP Test
A simple looping HTTP request intended for use from a Raspberry Pi.

## Usage
`http-test.py -t <target url> -f <frequency> -o <output file>`

 - *target url* should be a valid URL. Default is `https://google.com.au`.
 - *frequency* is measured in seconds. Default is `5`.
 - *output file* is the log file the results will be written to. Default is `http-test.log`.

## Notes
 - The greater of 5 seconds or `Frequency` is used as a timeout value for requests.
 - A best effort is made to perform a request according to the frequency specified. Slight drift is to be expected.

 # Bonus: Azure file upload function
 It occurred to me that I probably want a way to automatically upload these log files. [Azure Files](https://azure.microsoft.com/en-au/services/storage/files/?WT.mc_id=devops-0000-dabrady) to the rescue!

 It comes with a handy [Python SDK](https://docs.microsoft.com/en-us/azure/storage/files/storage-python-how-to-use-file-storage?WT.mc_id=devops-0000-dabrady), so I created an `upload.py` script to upload any files provided as arguments. They're automatically prefixed with a timestamp to avoid any confusion, but there are probably better ways.

 ## Usage
 `upload.py [file paths]`

 * *file paths* is one or more arguments with the full paths to files to upload

 ## Notes:
  - The script expects to find an `upload.config` file with settings. See below.
  - All files will be uploaded to the location specified in the config file, but will be prefixed with a timestamp in `YYYYMMDD-HHMM_` format. e.g. `20200915-1455_myfile.txt`

## Config
The script expects to find an `upload.config` file with four lines:
 - The storage account name
 - A storage account access key
 - The file share name
 - The directory name (must be provided)