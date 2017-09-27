## import the serial library
import serial
import string

fileName= input('Enter file name: ') #ask user to name the file

fileType= input('Enter file type: ') #ask the user or choose for the user?
filetype= '.csv'

ser=serial.Serial('COM8',9600)
## open text file to store the current 

text_file = open(fileName+fileType, 'w')
## read serial data from arduino and 
while 1:
    if ser.inWaiting():
        x=ser.readline()
        print(x)
##        data= int(filter(str.isdigit, x))
        text_file.write(str (x))
        text_file.write('\n')
        if x=='\n':
             text_file.seek(0)
             text_file.truncate()
        text_file.flush()

## close the serial connection and text file
text_file.close()
ser.close()
