from flask import Flask, render_template, request, send_file, Response
import pandas as pd
from imutils.video import VideoStream
import imutils
from datetime import datetime
import cv2
import time
from werkzeug import secure_filename
import numpy
from pyzbar import pyzbar
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 800  # Set Duration To 1000 ms == 1 second


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
def generate():
    global df1
    df1 = pd.DataFrame(columns=['TIMESTAMP','DATA','TYPE'])
    found = set()
    while True:
            frameData = vs.read()
            frameData = imutils.resize(frameData, width=600)
            barcodes = pyzbar.decode(frameData)
            timestamp = datetime.now()
            cv2.putText(frameData, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frameData.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
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
                    df1=df1.append(pd.DataFrame({"TIMESTAMP":[datetime.today().now().strftime("%Y-%m-%d-%H-%M-%S-%f")],
                            "DATA":[barcodeData],
                            "TYPE":[barcodeType]}))
                    found.add(barcodeData)

                    # Producing sound on identification of a barcode
                    winsound.Beep(frequency, duration)
                    # Producing sound on identification of a barcode
                    #cv2.imshow("Barcode Scanner", frameData1)
            (flag, encodedImage) = cv2.imencode(".jpg", frameData)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def generate_video():
    global df2
    df2 = pd.DataFrame(columns=['TIMESTAMP','DATA','TYPE'])
    found = set()
    while True:
        #CHECK FROM HERE
            frameData = vs1.read()
            #frameData = numpy.fromstring(frameData, numpy.uint8)
            # convert numpy array to image
            frameData = frameData[1]
            if frameData is None:
                break
            barcodes = pyzbar.decode(frameData)
            timestamp = datetime.now()
            cv2.putText(frameData, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frameData.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
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
                    df2=df2.append(pd.DataFrame({"TIMESTAMP":[datetime.today().now().strftime("%Y-%m-%d-%H-%M-%S-%f")],
                            "DATA":[barcodeData],
                            "TYPE":[barcodeType]}))
                    found.add(barcodeData)

                    # Producing sound on identification of a barcode
                    winsound.Beep(frequency, duration)
                    # Producing sound on identification of a barcode
                    #cv2.imshow("Barcode Scanner", frameData1)
            (flag, encodedImage) = cv2.imencode(".jpg", frameData)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def generate_image():
    global filename3
    frameData = cv2.imread(filename3)
    (flag, encodedImage) = cv2.imencode(".jpg", frameData)
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/home_t")
def home_t():
    return render_template("home.html")

# FOR IMAGE
@app.route('/success-table', methods=['POST','GET'])
def success_table():
    global filename
    global filename3
    df = pd.DataFrame(columns=['TIMESTAMP','DATA','TYPE'])
    if request.method=="POST":
        filestr = request.files['image'].read()
        #convert string data to numpy array
        try:
            npimg = numpy.fromstring(filestr, numpy.uint8)
            # convert numpy array to image
            im = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            decodedObjects = pyzbar.decode(im)
            got_it=set()
            frameData1 = im
            for g in decodedObjects:
                (x, y, width, height) = g.rect
                cv2.rectangle(frameData1, (x, y), (x + width, y + height), (0, 0, 255), 2)
                barcodeData = g.data.decode("utf-8")
                barcodeType = g.type
                textData = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frameData1, textData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # Checking for duplicate barcodes and writing info in the csv file
                if barcodeData not in got_it:
                    # csvWrite.write("{},{},{}\n".format(datetime.today().strftime('%Y-%m-%d'),barcodeData,barcodeType))
                    # csvWrite.flush()
                    df=df.append(pd.DataFrame({"TIMESTAMP":[datetime.today().strftime('%Y-%m-%d')],
                             "DATA":[barcodeData],
                             "TYPE":[barcodeType]}))
                    got_it.add(barcodeData)
                    # Producing sound on identification of a barcode
                    #cv2.imshow("Barcode Scanner", frameData1)
                    key = cv2.waitKey(1) & 0xFF
                    winsound.Beep(frequency, duration)
            filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+".csv")
            filename3 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+".jpg")
            cv2.imwrite(filename3,frameData1)
            df.to_csv(filename,index=None)
            return render_template("index.html",text=df.to_html(), btn='download.html')
        except Exception as e:
            return render_template("index.html", text=str(e))
    else:
        return render_template("index.html")

#FOR PLAYING VIDEO
@app.route('/video-table', methods=['POST','GET'])
def video_table():
    global vs1 
    # df = pd.DataFrame(columns=['TIMESTAMP','DATA','TYPE'])
    if request.method=="POST":
        filestr = request.files['video']
        filestr.save(secure_filename(filestr.filename))
        time.sleep(2.0)
        vs1 = cv2.VideoCapture(filestr.filename)
        # filestr = request.files['video'].read()
        #convert string data to numpy array
        try:   
            return render_template("stream2.html")
        except Exception as e:
            return render_template("index2.html", text=str(e))
    else:
        return render_template("index2.html")
    
@app.route('/video_feed1')
def video_feed1():
    return Response(generate_video(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
    
@app.route('/video-play-stop', methods=['POST','GET'])
def video_play_stop():
    cv2.destroyAllWindows()
    vs1.release()
    return render_template("index2.html",text=df2.to_html(index=False), btn='download_vp.html')

@app.route("/download_vpp/")
def download_vpp():
    print(df2)
    filename2 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+".csv")
    df2.to_csv(filename2,index=None)
    return send_file(filename2,as_attachment=True,cache_timeout=0)


# FOR STREAMING VIDEO 
@app.route('/video-stream', methods=['POST','GET'])
def video_stream():
    import time
    
    global vs
    if request.method=="POST":
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        #convert string data to numpy array
        try:          
            return render_template("stream.html")
        except Exception as e:
            return render_template("index3.html", text=str(e))
    else:
        return render_template("index3.html")
@app.route('/video_feed')
def video_feed():
    return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

    
@app.route('/video-stream-stop', methods=['POST','GET'])
def video_stream_stop():
    cv2.destroyAllWindows()
    vs.stop()
    return render_template("index3.html",text=df1.to_html(index=False), btn='download_v.html')

@app.route("/download-file/")
def download():
    return send_file(filename,as_attachment=True,cache_timeout=0)

@app.route("/download_vi/")
def download_vi():
    print(df1)
    filename1 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+".csv")
    df1.to_csv(filename1,index=None)
    return send_file(filename1,as_attachment=True,cache_timeout=0)

@app.route("/viewImage/")
def viewImage():
    return Response(generate_image(),mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
    global filename1
    global filename2
    global filename3
    app.run(debug=True)