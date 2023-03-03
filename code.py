import board
import storage
import digitalio
import time
import os
import supervisor
import microcontroller
import adafruit_character_lcd.character_lcd as characterlcd

# Menu varioable setup - yes I know the code is messy
setm = ("Upload Speed","Back Light","Auto Run")
speed = ("4.7Mhz ","4Mhz   ","Slow  ")
# settings for KeyPressLength, post-release debounce delay and settle time after entry mode change all in seconds
speedv = (0.005,0.005,0.06,0.006,0.006,0.08,0.1,0.1,0.2) # 4.7,4, and a slow one for debug 
blight = ("Off ","On ")
arun = ("Off ","On ")  
    
print("Pico MK14 uploader")




# Initialise all GPIO ports used by this program and set to high
cap = digitalio.DigitalInOut(board.GP6)
c6 = digitalio.DigitalInOut(board.GP7)
c7 = digitalio.DigitalInOut(board.GP8)
c5 = digitalio.DigitalInOut(board.GP9)
c4 = digitalio.DigitalInOut(board.GP10)
c3 = digitalio.DigitalInOut(board.GP11)
c2 = digitalio.DigitalInOut(board.GP12)
c1 = digitalio.DigitalInOut(board.GP13)
c0 = digitalio.DigitalInOut(board.GP14)
r3 = digitalio.DigitalInOut(board.GP15)
r2 = digitalio.DigitalInOut(board.GP16)
r1 = digitalio.DigitalInOut(board.GP17)
r0 = digitalio.DigitalInOut(board.GP18)

lcd_rs = digitalio.DigitalInOut(board.GP19)
lcd_en = digitalio.DigitalInOut(board.GP20)
lcd_d4 = digitalio.DigitalInOut(board.GP21)
lcd_d5 = digitalio.DigitalInOut(board.GP22)
lcd_d6 = digitalio.DigitalInOut(board.GP26)
lcd_d7 = digitalio.DigitalInOut(board.GP27)

k_up = digitalio.DigitalInOut(board.GP3)
k_dn = digitalio.DigitalInOut(board.GP4)
k_sel = digitalio.DigitalInOut(board.GP2)
k_dev = digitalio.DigitalInOut(board.GP5)

backl = digitalio.DigitalInOut(board.GP28)
backl.direction = digitalio.Direction.OUTPUT

k_up.switch_to_input(pull=digitalio.Pull.UP)
k_dn.switch_to_input(pull=digitalio.Pull.UP)
k_sel.switch_to_input(pull=digitalio.Pull.UP)
k_dev.switch_to_input(pull=digitalio.Pull.UP)

c6.direction = digitalio.Direction.OUTPUT
c7.direction = digitalio.Direction.OUTPUT
c5.direction = digitalio.Direction.OUTPUT
c4.direction = digitalio.Direction.OUTPUT
c3.direction = digitalio.Direction.OUTPUT
c2.direction = digitalio.Direction.OUTPUT
c1.direction = digitalio.Direction.OUTPUT
c0.direction = digitalio.Direction.OUTPUT
r3.direction = digitalio.Direction.OUTPUT
r2.direction = digitalio.Direction.OUTPUT
r1.direction = digitalio.Direction.OUTPUT
r0.direction = digitalio.Direction.OUTPUT
cap.direction = digitalio.Direction.OUTPUT

c6.value = True
c7.value = True
c5.value = True
c4.value = True
c3.value = True
c2.value = True
c1.value = True
c0.value = True
r3.value = True
r2.value = True
r1.value = True
r0.value = True
cap.value = True

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD(
    lcd_rs,
    lcd_en,
    lcd_d4,
    lcd_d5,
    lcd_d6,
    lcd_d7,
    lcd_columns,
    lcd_rows,
)

#load current setup data
try:
    setd = open('menust.txt')
    setupdat = setd.read()
    setd.close()
    speedd = int(setupdat[0])
    blightd = int(setupdat[1])
    arund = int(setupdat[2])
    menust = True
except:
    lcd.message = "Bad menutx file\nloading defaults"
    speedd = 2
    blightd = 1
    arund = 1
    menust = False   # flage an error in the data file - don't allow setup
    time.sleep(2)
    
print("Setup detail for debug only",speedd,blightd,arund)    

# If your MK14 has the 'Old' OS with the "---- --" reset prompt, edit
# the line below to read 'MK14_OS = 0'
MK14_OS = 1
OutputMode = 1

#set initial speed timings
# Minimum length of a keypress (seconds).
KeyPressLength = speedv[speedd]
# Time for post-release debounce delay (seconds).
KeyReleaseLength = speedv[speedd+1] 
# Additional settle time after entry mode change (seconds).
ModeChangeSettleTime = speedv[speedd+2]


def Press_MK14_Key(inp): # for Valid chars pulse relevant cross on keyboard matrix
    if inp=="m":        # Mem, the most commonly struck key
        r3.value = False
        c3.value = False
        time.sleep(KeyPressLength)
        r3.value = True
        c3.value = True
    elif inp=="0":
        r0.value = False
        c0.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c0.value = True
    elif inp=="1":
        r0.value = False
        c1.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c1.value = True
    elif inp=="2":
        r0.value = False
        c2.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c2.value = True
    elif inp=="3":
        r0.value = False
        c3.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c3.value = True
    elif inp=="4":
        r0.value = False
        c4.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c4.value = True
    elif inp=="5":
        r0.value = False
        c5.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c5.value = True
    elif inp=="6":
        r0.value = False
        c6.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c6.value = True
    elif inp=="7":
        r0.value = False
        c7.value = False
        time.sleep(KeyPressLength)
        r0.value = True
        c7.value = True
    elif inp=="8":
        r1.value = False
        c0.value = False
        time.sleep(KeyPressLength)
        r1.value = True
        c0.value = True
    elif inp=="9":
        r1.value = False
        c1.value = False
        time.sleep(KeyPressLength)
        r1.value = True
        c1.value = True
    elif inp=="A":
        r2.value = False
        c0.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c0.value = True
    elif inp=="B":
        r2.value = False
        c1.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c1.value = True
    elif inp=="C":
        r2.value = False
        c2.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c2.value = True
    elif inp=="D":
        r2.value = False
        c3.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c3.value = True
    elif inp=="E":
        r2.value = False
        c6.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c6.value = True
    elif inp=="F":
        r2.value = False
        c7.value = False
        time.sleep(KeyPressLength)
        r2.value = True
        c7.value = True
    elif inp=="g":      # Go
        r3.value = False
        c2.value = False
        time.sleep(KeyPressLength)
        r3.value = True
        c2.value = True
    elif inp=="q":      # Q=Abort ('A' already taken)
        r3.value = False
        c4.value = False
        time.sleep(KeyPressLength)
        r3.value = True
        c4.value = True
    elif inp=="t":      # Term
        r3.value = False
        c7.value = False
        time.sleep(KeyPressLength)
        r3.value = True
        c7.value = True
    elif inp=="r":      # System Reset
        cap.value = False
        time.sleep(0.1)
        cap.value = True
        time.sleep(KeyReleaseLength) # extra bit of delay for a reset
    time.sleep(KeyReleaseLength)

def SendFileToMK14(FileName):
    # Try to reset the MK14 before sending the file
    print ("Resetting...")
    Press_MK14_Key("r")
		
    # Assume by default that this file does not contain an execution
    # address at FFFE unless we find otherwise.	
    ExecuteFlag=0

    # Initially no errors have occurred. This flag will be set to 1
    # If an error occurs during the load process
    ErrorFlag=0

    # Open the file
    with open(FileName) as fileobj:

        # While there are lines to read from the file, read a line

        AddressAsHex="" # Hex string copy of most recent address incremented to. Empty on first pass.

        print ("Sending... ")

        for line in fileobj:

           # Check for Intel Hex Line start character
           # If not, declare file invalid and exit
           print(line)

           if (line [0]!=":"):
                ErrorFlag=1
                print ("Invalid Hex File")
                break
           else:
                # Read this line's 'record type',
                # If it is not a normal record (00), don't do anything with the line

                RecordTypeString=line[7:9]
                if (RecordTypeString=="00"):

                   # ..A normal record, so proceed to scan the line
                   # Zero the calculated line checksum

                   ChkSum=0

                   # By default, send whatever is read from the line to the
                   # MK14. This can be overridden with OutputMode = 0 if we only
                   # want to read and checksum the line, and not send it.

                   OutputMode=1

                   #Convert the record type to raw and add it to the calculated checksum

                   RecordTypeRaw=int(RecordTypeString, 16)
                   ChkSum=ChkSum+RecordTypeRaw

                   # Get the number of data bytes this line holds,
                   # convert to raw value and add to checksum.

                   DataBytesCountString=line[1:3]
                   DataBytesCount=int(DataBytesCountString,16)
                   ChkSum=ChkSum+DataBytesCount

                   # Get the four address digits, convert to raw 4 digit
                   # address, used as address upcounter.

                   AddressDigitsString=line[3:7]
                   AddressDigitsRaw=int(AddressDigitsString,16)

                   # Get the hi byte (only) of the address,
                   # add its byte value to the checksum.

                   AddressDigitsHiString=AddressDigitsString[0:2]
                   AddressDigitsHiRaw=int(AddressDigitsHiString,16)
                   ChkSum=ChkSum+AddressDigitsHiRaw

                   # Get the lo byte (only) of the address,
                   # add its byte value to the checksum.

                   AddressDigitsLoString=AddressDigitsString[2:4]
                   AddressDigitsLoRaw=int(AddressDigitsLoString,16)
                   ChkSum=ChkSum+AddressDigitsLoRaw

                   # Special case: If a line with the start address
                   # = FFFE is found, the first two data bytes are
                   # saved to be used as the execution address to run
                   # the program from after the file has been loaded.
                   # OutputMode is set to '0' for the rest of this
                   # line so that nothing from the line is sent to
                   # the MK14, although the line is still processed
                   # and checksummed.

                   if (AddressDigitsString=="FFFE") & (DataBytesCount > 1):
                       OutputMode=0
                       ExecuteFlag=1
                       ExecutionAddressHiString=line[9:11]
                       ExecutionAddressLoString=line[11:13]	
                       print("ex add")

                   # If the start address of this line does not follow
                   # on consecutively from the last address in the previous
                   # line, change to the new address before returning to data
                   # entry mode. When processing the first first line in the
                   # file, AddressAsHex is empty, forcing entry of the start
                   # address of the first line.
                    
                   print(AddressDigitsString,AddressAsHex) 
                   if (AddressDigitsString!=AddressAsHex):

                      # Change to address entry mode. Key depends on
                      # whether the OS is old or new version.
                      print("add update")
                      if MK14_OS!=1:
                          Press_MK14_Key('m')  # Old OS: Press Mem
                      else:
                          Press_MK14_Key('q')  # New OS: Press Abort

                      # Allow settle time after mode change
                      time.sleep(ModeChangeSettleTime)

                      Press_MK14_Key(AddressDigitsHiString[0])
                      Press_MK14_Key(AddressDigitsHiString[1])
                      Press_MK14_Key(AddressDigitsLoString[0])
                      Press_MK14_Key(AddressDigitsLoString[1])

                      #Change to data entry mode
                      Press_MK14_Key('t')  # Press Term

		      # Allow settle time after mode change
                      time.sleep(ModeChangeSettleTime)

                   # Scan and output the data bytes as MSD and LSD and
                   # add the byte value of the databyte to the checksum

                   for x in range (9,(9+DataBytesCount*2),2):
                        DataByteString=line[x:x+2]
                        DataByteRaw=int(DataByteString,16)
                        ChkSum=ChkSum+DataByteRaw

                        #Output the high and low digits of the databyte
                        Press_MK14_Key(DataByteString[0])
                        Press_MK14_Key(DataByteString[1])

                        # On New OS only a single 'MEM' press is required
                        # to enter data / advance address. On Old OS,
                        # Term-Mem-Term sequence is required for each
                        # data byte entry / address advance.

                        if MK14_OS !=1:
                            Press_MK14_Key('t')  # Press Term

                        Press_MK14_Key('m')  # Press Mem

                        if MK14_OS !=1:
                            Press_MK14_Key('t') # Press Term

                        #advance the raw address keeper
                        AddressDigitsRaw=AddressDigitsRaw+1

                   # Get the line's checksum from the end of the line
                   LineChecksumString=line[(9+(DataBytesCount*2)):(9+(DataBytesCount*2)+2)]

                   # Calculated checksum has to be converted to its 8-bit twos-
                   # complement before comparison with the file checksum

                   # Invert it
                   ChkSum=~ChkSum

                   # Strip it back down to one byte
                   ChkSum=ChkSum & 255

                   # Add one to it
                   ChkSum=ChkSum+1

                   # Convert it to hex string
                   ChkSumHexString = "%0.2X" % ChkSum

                   # Check whether it is valid, if not, abort
                   if LineChecksumString!=ChkSumHexString:
                       print ("Invalid Checksum in file.")
                       ErrorFlag=1
                       break

                   # AddressAsHex = ASCII hex version of current address
                   AddressAsHex="%0.4X" % AddressDigitsRaw

        # When all lines have been processed, exit data entry mode.
        Press_MK14_Key('q')
        time.sleep(ModeChangeSettleTime)

	# If an execution address was found in the file at special address FFFE and
        # there were no errors during the load process, execute froom that address.
        # Key sequence depends on OS version.
        # if autorun is set to off in Execute flag is over ruled

        if (ExecuteFlag==1 and arund==True) & (ErrorFlag==0):

            if MK14_OS !=1:
                Press_MK14_Key('g')

            Press_MK14_Key (ExecutionAddressHiString[0])
            Press_MK14_Key (ExecutionAddressHiString[1])
            Press_MK14_Key (ExecutionAddressLoString[0])
            Press_MK14_Key (ExecutionAddressLoString[1])

            if MK14_OS !=1:
                Press_MK14_Key ('t')
            else:
                Press_MK14_Key ('g')

            print ("Executing...")

        if ErrorFlag==0:
            print ("Done.")
        else:
            print ("Aborted.")	


#gets or renews the file list and parses it to just include .hex items
#returns a nice clean string containing names of all the hex files
#well thats the plan anyway
def get_files():
    appl = list()
    dirl = os.listdir()
    for flr in dirl:
        if flr.endswith('hex'):
           appl.append(flr)         
    return(appl)

#toggle backlight
def backlight():
    if blightd == True:
        backl.value = True
    else:
        backl.value = False        

               
#---------------------------------------------------------------------------------------------------
# Main Body Of Program
#---------------------------------------------------------------------------------------------------

# check for an abort, if dev key is held down at power up or when the pico comes out of reset
# abort the application. This ensures with the application auto running it can be got out of loop
# without some more extreme action!

if k_dev.value == False:
    lcd.clear()
    lcd.message = "Exciting App"
    exit()  #basically this just creates and error to abort the program as exit is not defined

# set backlight based on stored value
backlight()
    
# check for select push being down if so enter setup mode
# also check a good menust has been loaded - a bad one will cause the app to crash
# this is not easily fixable 
if k_sel.value == False and menust == True:
    
    storage.remount("/", False)
    
    lcd.clear()
    lcd.message = "Entering Setup\nMode"
    time.sleep(1)
    while k_sel.value == False:
            time.sleep(.1)
    lcd.clear()
    scn = 0
    lcd.message = setm[0]
    lcd.message = "\n" + speed[speedd]
    while k_dev.value == True:
            #look for up / down key press, update display and pointer accordingly
        if k_dn.value == False or k_up.value == False:
            time.sleep(.05)
            if k_up.value == False:
                scn = scn + 1
                if scn >= len(setm):
                    scn = 0
            elif k_dn.value == False:
                scn = scn - 1
                if scn == -1:
                    scn = len(setm)-1
            lcd.clear()
            lcd.message = setm[scn]  # display setup menu 
            if scn == 0:
                lcd.message = "\n" + speed[speedd]
            elif scn == 1:
                lcd.message = "\n" + blight[blightd]
            elif scn == 2:
                lcd.message = "\n" + arun[arund]
                
            while k_dn.value == False or k_up.value == False: # wait for keys be released
                time.sleep(.1)
                
        if k_sel.value == False:  #terst for sel push - if so go to indiv setup updates routines
            if scn == 0: # update speed
                speedd = speedd + 1
                if speedd == 3:
                    speedd = 0
                # disp new speed and update temp speed variables        
                lcd.message = "\n" + speed[speedd]
                # Minimum length of a keypress (seconds).
                KeyPressLength = speedv[speedd]
                # Time for post-release debounce delay (seconds).
                KeyReleaseLength = speedv[speedd+1] 
                # Additional settle time after entry mode change (seconds).
                ModeChangeSettleTime = speedv[speedd+2]
                while k_sel.value == False: # wait for key release
                    time.sleep(.1)
       
            elif scn == 2: # Auto run
                if arund == 1:
                    arund = 0
                else:
                    arund = 1
                lcd.message = "\n" + arun[arund]
           
                while k_sel.value == False: # wait for key release
                    time.sleep(.1)
    
            elif scn == 1: # Backlight
                if blightd == 1:
                    blightd = 0
                else:
                    blightd = 1
                lcd.message = "\n" + blight[blightd]
                backlight()
                while k_sel.value == False: # wait for key release
                    time.sleep(.1)
    
    with open("/menust.txt", "w") as setd:
        setd.write(str(speedd)+str(blightd)+str(arund))
    
        setd.close()
        
    
        
    lcd.clear()
    lcd.message = "Exiting Setup"
    time.sleep(1)
    
    microcontroller.reset()        
    

#setup and intro screen
lcd.clear()
lcd.message = "S of C MK14\nPico Uploader"

time.sleep(2)
lcd.clear()

#get list of .hex files on pico mounted drive
appl = get_files()
lcd.message = (str(len(appl)) + " hex files\navailable")
    
time.sleep(1)
lcd.clear()

lcd.message = lcd.message = "Upload target-\n" +chr(126)+" " + appl[0][:-4]
appl_no = 0
# main program loop

while True:
    
    #look for up / down key press, update display and pointer accordingly
    if k_dn.value == False or k_up.value == False:
        time.sleep(.05)
        if k_dn.value == False and k_up.value == False:  # refresh file list
            lcd.clear()
            lcd.message = "Refeshing\nfile list"
            appl = get_files()
            time.sleep(1)
            lcd.clear()
            lcd.message = appl[0][:-4]
            
        elif k_up.value == False:
            appl_no = appl_no + 1
            if appl_no >= len(appl):
                appl_no = 0
        elif k_dn.value == False:
            appl_no = appl_no - 1
            if appl_no == -1:
                appl_no = len(appl)-1

        lcd.clear()
        lcd.message = "Upload target-\n"+chr(126)+" "+appl[appl_no][:-4]    
        #    wait for key to be released before moving on   
        while k_dn.value == False or k_up.value == False:
            time.sleep(.1)   
    # test for upload push
    # Sel on it's own uploads currently selected file
    # if Dev is pushed and then Sel held down at the same time the s/w attempts to upload
    # the file pointed to by the text file 'development.txt'
    # this allow quick turn around when developing s/w  

    # test for dev upload
    if k_dev.value == False and k_sel.value == False:
        devf = open('dev.txt')
        dev_file = devf.read()
        
        lcd.clear()
        lcd.message = "Dev Upload-\n"+chr(126)+" "+dev_file[:-4]
        
        SendFileToMK14(dev_file)
        time.sleep(1.5)
        lcd.clear()
        lcd.message = "Upload target-\n" + chr(126)+" " +appl[appl_no][:-4]
    
    #now test for sel push on its own, if send selected file to MK14
    elif k_sel.value == False:
        lcd.message = "Uploading File"
        SendFileToMK14(appl[appl_no])
        lcd.clear()
        lcd.message = "File upload\ncomplete"  
        while k_sel.value == False:
            time.sleep(.1)
        time.sleep(1.5)
        lcd.clear()
        lcd.message = "Upload target-\n" + chr(126)+" " +appl[appl_no][:-4]
    

