# USAGE
# python barcode_scanner.py
# python barcode_scanner.py -o results.csv -v "path to a video file"
# python barcode_scanner.py -o results.csv -v videos/coupon.mov

# Importing relevant libraries
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
from datetime import datetime
import imutils
import time
import cv2
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 800  # Set Duration To 1000 ms == 1 second

# Parsing Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodesData.csv",
	help="path to output CSV file ")
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-i", "--image",
	help="path to the (optional) image file")
args = vars(ap.parse_args())

# Taking care of the output header
import csv
csvWrite = open(args["output"], "a")
# checking if the file already exists and getting the number of records
csvfile = open(args["output"], "r")
csv_dict = [row for row in csv.DictReader(csvfile)]
if len(csv_dict) == 0:
	count=0
	# Checking if the header already exists
	f = open(args["output"])
	line = f.readline()
	f.close()
	if len(line) == 0:
		csvWrite.write("{},{},{}\n".format("TIMESTAMP (YYYY-MM-DD)","DATA","TYPE"))
else:
    count=len(csv_dict)				
csvfile.close()

def write_records(bar_codes):
    records_written=len(bar_codes)
    if records_written == 0:
        print( "\n No Barcodes found in the Video.")
    else:
        print( "\n {} new Records written to the Database".format(records_written))
    print("\n Total number of records in {}   :   {}".format(args["output"],count+records_written))


# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	print("Starting Webcam !!!")

#otherwise load the video
else:
    print("Loading Video !!!")
    vs = cv2.VideoCapture(args["video"])


found = set()
while True:
	frameData = vs.read()
	frameData = frameData[1] if args.get("video", False) else imutils.resize(frameData, width=600)
	# If the video is over
	if frameData is None:
    		break
	# Getting the barcodes from the frame
	barcodes = pyzbar.decode(frameData)

	# Looping through each barcode and extracting info
	for barcode in barcodes:
		(x, y, width, height) = barcode.rect
		cv2.rectangle(frameData, (x, y), (x + width, y + height), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		textData = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frameData, textData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# Checking for duplicate barcodes and writing info in the csv file
		if barcodeData not in found:
			csvWrite.write("{},{},{}\n".format(datetime.today().strftime('%Y-%m-%d'),barcodeData,barcodeType))
			csvWrite.flush()
			found.add(barcodeData)

			# Producing sound on identification of a barcode
			winsound.Beep(frequency, duration)

	# Displaying info inside the video
	cv2.imshow("Barcode Scanner", frameData)
	key = cv2.waitKey(1) & 0xFF

	# press e to terminate the camera
	if key == ord("e"):
		break

# close the output CSV file do a bit of cleanup
write_records(found)

csvWrite.close()
cv2.destroyAllWindows()

# if we are not using a video file, stop the video file stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera pointer
else:
	vs.release()