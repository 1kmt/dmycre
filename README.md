# About dmycre&#46;py ( Dummy File Creator )
This tool creates dummy files for program testing.
You can specify the size and number of files to create.
The data is in binary format and can be selected from random numbers, fixed values, and sequential numbers.  
&nbsp;  
## Features
The main features are as follows:
- Specify multiple sizes separated by spaces. (-l option)
- Specify a lower and upper size limit, and the file will be created with all sizes within that range. (-r option)
- Specify how many files to create for each size. (-m option)
- Write random numbers up to the specified size. (-rnd option)
- Writes the specified fixed value repeatedly up to the specified size. The specified fixed value is processed as a hexadecimal number. (-fix option)
- By specifying a start value and an end value, a sequence of values from the start value to the end value is written. The specified value is processed as a hexadecimal number. (-seq option)
&nbsp;  
&nbsp;  
## Installation
### 1.&nbsp;&nbsp;Check Python version ( version >= 3.6 required )
Available since Python 3.6.
To check the version, at the command prompt or terminal type:
```
python -V
```
or
```
python
```
Upgrade Python to the latest version if nessasary.  
[https://www.python.org/downloads/](https://www.python.org/downloads/)
&nbsp;  
### 2.&nbsp;&nbsp;Clone this repository
Change the current directory to the location where you want to install and run the following command:
```
git clone https://github.com/1kmt/dmycre.git
cd dmycre
```
### 3.&nbsp;&nbsp;Install the dependencies
Need packages for working.
If the package is not installed, install it using the following command.
```
python -m pip install numpy
``` 
### 4.&nbsp;&nbsp;Run
See 'Command line examples'
&nbsp;  
&nbsp;  
## Usage
```
usage: dmycre.py [-h] [-m HOWMANY] [-o OUTPUT] [-v]
                 (-l LIST [LIST ...] | -r RANGE RANGE)
                 (-rnd | -fix FIXED | -seq SEQUENTIAL SEQUENTIAL)

This tool creates dummy files for program testing. You can specify the size
and number of files to create. The data is in binary format and can be
selected from random numbers, fixed values, and sequential numbers.

optional arguments:
  -h, --help            show this help message and exit
  -m HOWMANY, --howmany HOWMANY
                        specify the number of files to create
  -o OUTPUT, --output OUTPUT
                        change the output directory
  -v, --version         show program's version number and exit
  -l LIST [LIST ...], --list LIST [LIST ...]
                        specify a list of file sizes (e.g. -l 10 100 200
                        2000000)
  -r RANGE RANGE, --range RANGE RANGE
                        specify a range of file sizes (e.g. -r 10 20)
  -rnd, --random        writes a random number to the file
  -fix FIXED, --fixed FIXED
                        specifies a fixed value to be written to the file
                        (e.g. -fix 09AB)
  -seq SEQUENTIAL SEQUENTIAL, --sequential SEQUENTIAL SEQUENTIAL
                        specifies a sequential number to be written to the
                        file (e.g. -seq 00 FF, -seq FF 00)
```
### &#9635;&nbsp;&nbsp;Command line examples
Ten 10-byte, 20-byte, 100-byte, and 20000000-byte files will be created each.
A random number is written to the file.
```
python dmycre.py -l 10 20 100 20000000 -m 10 -rnd
```
Creates 99-byte, 100-byte, and 101-byte files.
A fixed value "09AB(hex)" is written to the file.
```
root@kali:~/Desktop# python3 dmycre.py -l 20 100 -m 30 -fix 09AB -o ./dummy
2022-08-27 02:45:55[I] [START    ] /root/Desktop/dmycre.py
2022-08-27 02:45:55[I] [OUT_DIR  ] /root/Desktop/dummy
2022-08-27 02:45:55[I] [MAKE_FILE] 0000000020 bytes x 30 files
PROGRESS|████████████████████████████████████████|   30/30   ( 100.0% )
2022-08-27 02:45:55[I] [MAKE_FILE] 0000000100 bytes x 30 files
PROGRESS|████████████████████████████████████████|   30/30   ( 100.0% )
2022-08-27 02:45:55[I] [END      ] /root/Desktop/dmycre.py
root@kali:~/Desktop# xxd ./dummy/size00000000100_0002.dat | head -n 10
00000000: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000010: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000020: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000030: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000040: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000050: 09ab 09ab 09ab 09ab 09ab 09ab 09ab 09ab  ................
00000060: 09ab 09ab 
```
If the -seq option is used, the following files are created.
```
root@kali:~/Desktop# python3 dmycre.py -r 1000 1002 -m 30 -seq 00 FF -o ./dummy
2022-08-27 02:49:09[I] [START    ] /root/Desktop/dmycre.py
2022-08-27 02:49:09[I] [OUT_DIR  ] /root/Desktop/dummy
2022-08-27 02:49:09[I] [MAKE_FILE] 0000001000 bytes x 30 files
PROGRESS|████████████████████████████████████████|   30/30   ( 100.0% )
2022-08-27 02:49:09[I] [MAKE_FILE] 0000001001 bytes x 30 files
PROGRESS|████████████████████████████████████████|   30/30   ( 100.0% )
2022-08-27 02:49:10[I] [MAKE_FILE] 0000001002 bytes x 30 files
PROGRESS|████████████████████████████████████████|   30/30   ( 100.0% )
2022-08-27 02:49:10[I] [END      ] /root/Desktop/dmycre.py
root@kali:~/Desktop# xxd ./dummy/size00000001000_0002.dat | head -n 10
00000000: 0001 0203 0405 0607 0809 0a0b 0c0d 0e0f  ................
00000010: 1011 1213 1415 1617 1819 1a1b 1c1d 1e1f  ................
00000020: 2021 2223 2425 2627 2829 2a2b 2c2d 2e2f   !"#$%&'()*+,-./
00000030: 3031 3233 3435 3637 3839 3a3b 3c3d 3e3f  0123456789:;<=>?
00000040: 4041 4243 4445 4647 4849 4a4b 4c4d 4e4f  @ABCDEFGHIJKLMNO
00000050: 5051 5253 5455 5657 5859 5a5b 5c5d 5e5f  PQRSTUVWXYZ[\]^_
00000060: 6061 6263 6465 6667 6869 6a6b 6c6d 6e6f  `abcdefghijklmno
00000070: 7071 7273 7475 7677 7879 7a7b 7c7d 7e7f  pqrstuvwxyz{|}~.
00000080: 8081 8283 8485 8687 8889 8a8b 8c8d 8e8f  ................
00000090: 9091 9293 9495 9697 9899 9a9b 9c9d 9e9f  ................
```
