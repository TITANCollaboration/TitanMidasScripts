#!/usr/bin/python

import pythonmidas.pythonmidas as Midas
import time
import smtplib

# Time command was last executed
VacuumAlarmFirstTriggered = "/Alarms/Alarms/Demo ODB/Time triggered first"

# Check when the last time the command was executed.
# If it is '0', then it is the first time the alarm is executed,
# so we should send an email.
# Otherwise, if the last time the command was executed is greater
# than zero, we should not send an email.

# Get the time the alarm was first triggered
try:
    FirstTriggered = time.strptime(Midas.varget(VacuumAlarmFirstTriggered),
                                   "%a %b %d %H:%M:%S %Y")
    FirstTriggered = time.mktime(FirstTriggered)
except:
    FirstTriggered = 0
    print "First Triggered Time is empty!"

# Get the current time
CurrentTime = time.mktime(time.localtime())

# If the current time and first triggered time are close together
# send an email to the mailing list
if CurrentTime - FirstTriggered < 10:
    SERVER = "localhost"
    FROM = "mpet@titan01.triumf.ca"
    # Get list of addresses for email
    TO = [x[1] for x in Midas.dirlist("/Experiment/Variables/Contacts")]

    SUBJECT = "ALARM: MpetVacuum"

    TEXT = "Vacuum Alarm in MPET.\n\n"
    TEXT += "Please reset the Alarm on 'titan01.triumf.ca:8080'.\n\n"
    vaclevel = Midas.varget("/Equipment/Beamline/Variables/Measured[58]")
    TEXT += "Current Vacuum = %s Torr\n" % vaclevel
    #TEXT += "This is a test of the email list. Please ignore."

    # Prepare actual message

    message = """\
            From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail

    for recep in TO:
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, [recep], message)
        server.quit()
