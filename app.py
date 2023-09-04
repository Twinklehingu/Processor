# web-app for API image manipulation
from collections.abc import MutableMapping
from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image

app = Flask(__name__)
app.debug=True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

global mainFileName 

# default access page
@app.route("/")
def main():
    return render_template('index.html')


# upload selected image and forward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = str(os.path.splitext(filename)[1]).lower()
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp") or (ext==".jpeg"):
        print("File accepted")
    else:
        return render_template("error.html", message="The selected file is not supported."), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)
    global mainFileName
    mainFileName = str(os.path.splitext(filename)[0])
    print('Original File Name is',mainFileName)
    # forward to processing page
    return render_template("process.html", image_name=filename)

@app.route("/submit", methods=["POST"])
def submit():
    angleFlag, flipFlag, resizeFlag, thumbnailFlag, grayscaleFlag, rotateFlag = False, False, False, False, False, False
    
    selectedOptionsDict = (request.form.to_dict())
    print(selectedOptionsDict)
    filename = selectedOptionsDict['image']
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])
    imgBlob = Image.open(destination)
    if 'flip' in selectedOptionsDict:
        flipFlag = True
        flipMode = selectedOptionsDict['flip']
        imgBlob = flip(imgBlob, flipMode)

    if selectedOptionsDict['angle'] != "":
        angle = selectedOptionsDict['angle']
        angleFlag = True
        imgBlob = rotate(imgBlob, angle)
    
    
    resizeX = selectedOptionsDict['X']
    resizeY = selectedOptionsDict['Y']
    if resizeX == "" and resizeY !="":
            return render_template("error.html", message="Please enter X and Y dimensions for Resize"), 400
    elif resizeY == "" and resizeX !="":
            return render_template("error.html", message="Please enter X and Y dimensions for Resize"), 400
    elif resizeY == "" and resizeX =="":
        resizeFlag = False
    elif resizeY != "" and resizeX !="":
        imgBlob = resize(imgBlob, resizeX, resizeY)
        resizeFlag = True
    
    thumbnailX = selectedOptionsDict['sizeX']
    thumbnailY = selectedOptionsDict['sizeY']
    if thumbnailX == "" and thumbnailY !="":
            return render_template("error.html", message="Please enter X and Y dimensions for Thumbnail"), 400
    elif thumbnailY == "" and thumbnailX !="":
            return render_template("error.html", message="Please enter X and Y dimensions for Thumbnail"), 400
    elif thumbnailY == "" and thumbnailX =="":
        thumbnailFlag = False
    elif thumbnailY != "" and thumbnailX !="":
        thumbnailFlag = True
        imgBlob = thumbnail(imgBlob, thumbnailX, thumbnailY)
    
    if 'grayscale' in selectedOptionsDict:
        grayscaleFlag = True
        grayMode = selectedOptionsDict['grayscale']
        imgBlob = grayscale(imgBlob)
    
    if 'Rotate' in selectedOptionsDict:
        rotateFlag = True
        mode = selectedOptionsDict['Rotate']
        imgBlob = rotateleftright(imgBlob, mode)
    
    fileNameSplit = (os.path.splitext(filename))
    print(fileNameSplit)
    destinationFileName = str(fileNameSplit[0]) + '_ResultImage' +  str(fileNameSplit[1])
    print('Destination file is',destinationFileName)
    destinationFolder = "/".join([target, destinationFileName])
    print('Destination Folder is',destinationFolder)
    imgBlob.save(destinationFolder)
    # print("angleFlag, flipFlag, resizeFlag, thumbnailFlag, grayscaleFlag, rotateFlag")
    # print(angleFlag, flipFlag, resizeFlag, thumbnailFlag, grayscaleFlag, rotateFlag)
    
    return render_template("process.html", image_name=destinationFileName)
    pass
# rotate filename the specified degrees

def rotate(img, angle):
    # retrieve parameters from html form
    # angle = request.form['angle']
    # filename = request.form['image']
    
    # global mainFileName
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName) + '_RotateDegree_' + str(angle) + str(fileNameSplit[1])
    # # open and process image
    # target = os.path.join(APP_ROOT, 'static/images')
    # destination = "/".join([target, filename])

    # img = Image.open(destination)
    img = img.rotate(int(angle),expand=True)
    return img
    # save and return image
    # destination = "/".join([target, destinationFileName])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)

    #return render_template("processing.html", image_name=destinationFileName)
    #return send_image(destinationFileName)


# flip filename 'vertical' or 'horizontal'

def flip(img, mode):
    
    # retrieve parameters from html form
    # if 'horizontal' in request.form['mode']:
    #     mode = 'horizontal'
    # elif 'vertical' in request.form['mode']:
    #     mode = 'vertical'
    # else:
    #     return render_template("error.html", message="Mode not supported (vertical - horizontal)"), 400
    # filename = request.form['image']
    # global mainFileName
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName)  + '_Flip_' + str(mode) + str(fileNameSplit[1])
    # open and process image
    # target = os.path.join(APP_ROOT, 'static/images')
    # destination = "/".join([target, filename])
    # img = Image.open(destination)

    if mode == 'horizontal':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    return img
    # save and return image
    # destination = "/".join([target, destinationFileName])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)

    #return render_template("processing.html", image_name=destinationFileName)


# crop filename from (x1,y1) to (x2,y2)

def resize(img, x, y):
    # retrieve parameters from html form
    
    # x = int(request.form['X'])
    # y = int(request.form['Y'])
    # filename = request.form['image']
    # global mainFileName
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName)  + '_Resize_' + str(x) + '_' + str(y)+ str(fileNameSplit[1])
    # # open image
    # target = os.path.join(APP_ROOT, 'static/images')
    # destination = "/".join([target, filename])

    # img = Image.open(destination)
    

    # resizePossible = True
    # if x == 0 or y==0 :
    #     resizePossible = False
    

    # crop image and show
    
    img = img.resize((int(x),int(y)),Image.ANTIALIAS)
    return img
    #     # save and return image
    #     destination = "/".join([target, destinationFileName])
    #     if os.path.isfile(destination):
    #         os.remove(destination)
    #     img.save(destination)
    #     #return send_image(destinationFileName)
    #     return render_template("processing.html", image_name=destinationFileName)
    # else:
    #     return render_template("error.html", message="Resize dimensions not valid"), 400
    # return '', 204



def grayscale(img):
    # filename = request.form['image']
    # target = os.path.join(APP_ROOT, 'static/images')
    # global mainFileName
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName)  + '_GrayScale' + str(fileNameSplit[1])
    # destination = "/".join([target, filename])
    try:
        img = img.convert('L')
        
    except:
        img = img.convert('LA')
    
    return img
    
    
    # destination = "/".join([target, destinationFileName])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)

    # return render_template("processing.html", image_name=destinationFileName)
    #return send_image(destinationFileName)



def thumbnail(img, sizeWidth, sizeHeight):
    # filename = request.form['image']
    # sizeWidth = int(request.form['sizeX'])
    # sizeHeight = int(request.form['sizeY'])
    # target = os.path.join(APP_ROOT, 'static/images')

    # global mainFileName
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName)  + '_Thumbnail_'+ str(sizeWidth)+ '_' + str(sizeHeight) + str(fileNameSplit[1])
    # destination = "/".join([target, filename])

    # img = Image.open(destination)
    # originalImageWidth, originalImageHeight= img.size


    img.thumbnail((int(sizeWidth), int(sizeHeight)))
    return img
    # destination = "/".join([target, destinationFileName])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)

    # return render_template("processing.html", image_name=destinationFileName)
    #return send_image(destinationFileName)
@app.route("/rotateleftright",methods=["POST"])
def rotateleftright(img, mode):

    

    if mode == 'Left':
        
        angle = 90
    elif mode == 'Right':
        
        angle = -90
    # global mainFileName
    # target = os.path.join(APP_ROOT, 'static/images')    
    # fileNameSplit = (os.path.splitext(filename))
    # destinationFileName = str(mainFileName)  + '_Rotate_'+ str(mode)+ str(fileNameSplit[1])
    # destination = "/".join([target, filename])

    # img = Image.open(destination)
    img = img.rotate(angle, expand=True)
    return img
    # destination = "/".join([target, destinationFileName])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)
    # return render_template("processing.html", image_name=destinationFileName)
    #return send_image(destinationFileName)
    
# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == "__main__":
    #app.run()
    app.run(host='127.0.0.1', port=9874)

