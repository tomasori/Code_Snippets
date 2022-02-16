#
# This code uses several snippets of code I found that I've combined/tweaked/etc.
# I note the areas where the snippets are located by adding
# the text "The following is code I found online that i think is cool"
#
# Note: I could have made the matplotlib code something basic but I left
# it since it may add value to however is reviewing this code.
#
# TEST data is provided at the end of this code so this .py file will
# run if you have all required modules installed.
#
# the code I use or will be using, only sends back the cropped image.
# I updated to send back two images so the cropped versus uncropped versions
# can be compared. I reduced the width of both plots to 400px so they
# can be seen side-by-side in a browser window.


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as mp3d
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import io
import base64
import cv2      # OpenCV


def plot_iso_view(num_of_plans, joints):
    ''' Function plots a 3D view of an offshore jacket.
        Function returns and Base64 encoded PNG file that can be sent
        to browsers and/or through Flask.
    '''

    #----------------------------------------------------------
    # The following is code I found online that i think is cool
    #----------------------------------------------------------
    # Get max and min X, Y, and Z values for use in scaling the 3D plot(s)
    # and used to size the planes defining the WL and ML
    #
    # code returns a tuple with with the max or min value with the key
    # where it was obtain from so grab the first part of the tuple.
    # NOTE: [0] needed to grab the first value in the tuple
    maxX = max((joints[key][0],key) for key in joints)[0]
    minX = min((joints[key][0],key) for key in joints)[0]
    maxY = max((joints[key][1],key) for key in joints)[0]
    minY = min((joints[key][1],key) for key in joints)[0]
    maxZ = max((joints[key][2],key) for key in joints)[0]
    minZ = min((joints[key][2],key) for key in joints)[0]
    #------------------------------------------------------------------------

    # get mudline elevation
    ml_elev = joints['101L'][2]
    #print(ml_elev)

    #set marker sizes used in  ISO view
    markersize = 5

    # create figure
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection = '3d')

    # set size of plot
    fig.set_figwidth(8)
    fig.set_figheight(8)

    # Add in the planes that represent the waterline and Mudline
    spacer_wl = 1.20    # make WL plane wider by this factor
    spacer_ml = 1.75    # make ML plane wider by this factor
    alpha_wl = 0.15     # transparency factor for Waterline
    alpha_ml = 0.45     # transparency factor for Mudline
    # waterline joint coordinates
    wl_plane = [(minX*spacer_wl, minY*spacer_wl, 0),
                (maxX*spacer_wl, minY*spacer_wl, 0),
                (maxX*spacer_wl, maxY*spacer_wl, 0),
                (minX*spacer_wl, maxY*spacer_wl, 0)
                ]
    # add WL plane
    wl_face = mp3d.art3d.Poly3DCollection([wl_plane], alpha=alpha_wl, linewidth=1)
    # mudline joint coordinates
    ml_plane = [(minX*spacer_ml, minY*spacer_ml, ml_elev),
                (maxX*spacer_ml, minY*spacer_ml, ml_elev),
                (maxX*spacer_ml, maxY*spacer_ml, ml_elev),
                (minX*spacer_ml, maxY*spacer_ml, ml_elev)
                ]
    # add ML plane
    ml_face = mp3d.art3d.Poly3DCollection([ml_plane], alpha=alpha_ml, linewidth=1)
    # set colors of the two planes.
    wl_face.set_facecolor("mediumblue") # use a medium blue for waterline
    ax.add_collection3d(wl_face)
    ml_face.set_facecolor("#C4A484")    # use a light brown for mudline
    #C4A484
    ax.add_collection3d(ml_face)

    # do the horz plans
    for i in range(1, num_of_plans+1):
        A1 = str(i)+ "01L"
        A2 = str(i)+ "02L"
        B1 = str(i)+ "03L"
        B2 = str(i)+ "04L"
        x = [ joints[A1][0], joints[A2][0],  joints[B2][0],  joints[B1][0],  joints[A1][0] ]
        y = [ joints[A1][1], joints[A2][1],  joints[B2][1],  joints[B1][1],  joints[A1][1] ]
        z = [ joints[A1][2], joints[A2][2],  joints[B2][2],  joints[B1][2],  joints[A1][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

    # Do the four legs
    # Jts that start 1xxx are at ML.  Jts that start with (num_of_plans+1) is the WP
    for i in range(4):
        bot =  "a0bL".replace("a",str(0)).replace("b",str(i+1))
        pile = "a0bL".replace("a",str(num_of_plans+1)).replace("b",str(i+1))
        if num_of_plans == 8:
            letter = "A"
        else:
            letter = str(num_of_plans+2)
        top =  "a0bL".replace("a",letter).replace("b",str(i+1))

        x = [ joints[bot][0], joints[pile][0], joints[top][0] ]
        y = [ joints[bot][1], joints[pile][1], joints[top][1] ]
        z = [ joints[bot][2], joints[pile][2], joints[top][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

    # Do x-braces on Row A and B
    for i in range(num_of_plans-1):

        # plot x-braces on Row A
        j11 = "a0bL".replace("a",str(i+1)).replace("b","1")
        j12 = "a0bL".replace("a",str(i+2)).replace("b","2")
        jxx = "a0bX".replace("a",str(i+1)).replace("b","1")
        j21 = "a0bL".replace("a",str(i+1)).replace("b","2")
        j22 = "a0bL".replace("a",str(i+2)).replace("b","1")
        x = [ joints[j11][0], joints[jxx][0], joints[j12][0] ]
        y = [ joints[j11][1], joints[jxx][1], joints[j12][1] ]
        z = [ joints[j11][2], joints[jxx][2], joints[j12][2] ]

        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')
        x = [ joints[j21][0], joints[jxx][0], joints[j22][0] ]
        y = [ joints[j21][1], joints[jxx][1], joints[j22][1] ]
        z = [ joints[j21][2], joints[jxx][2], joints[j22][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

        # plot x-braces on Row B
        j11 = "a0bL".replace("a",str(i+1)).replace("b","3")
        j12 = "a0bL".replace("a",str(i+2)).replace("b","4")
        jxx = "a0bX".replace("a",str(i+1)).replace("b","3")
        j21 = "a0bL".replace("a",str(i+1)).replace("b","4")
        j22 = "a0bL".replace("a",str(i+2)).replace("b","3")
        x = [ joints[j11][0], joints[jxx][0], joints[j12][0] ]
        y = [ joints[j11][1], joints[jxx][1], joints[j12][1] ]
        z = [ joints[j11][2], joints[jxx][2], joints[j12][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')
        x = [ joints[j21][0], joints[jxx][0], joints[j22][0] ]
        y = [ joints[j21][1], joints[jxx][1], joints[j22][1] ]
        z = [ joints[j21][2], joints[jxx][2], joints[j22][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

        # plot x-braces on Row 2
        j11 = "a0bL".replace("a",str(i+1)).replace("b","2")
        j12 = "a0bL".replace("a",str(i+2)).replace("b","4")
        jxx = "a0bX".replace("a",str(i+1)).replace("b","2")
        j21 = "a0bL".replace("a",str(i+1)).replace("b","4")
        j22 = "a0bL".replace("a",str(i+2)).replace("b","2")
        x = [ joints[j11][0], joints[jxx][0], joints[j12][0] ]
        y = [ joints[j11][1], joints[jxx][1], joints[j12][1] ]
        z = [ joints[j11][2], joints[jxx][2], joints[j12][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')
        x = [ joints[j21][0], joints[jxx][0], joints[j22][0] ]
        y = [ joints[j21][1], joints[jxx][1], joints[j22][1] ]
        z = [ joints[j21][2], joints[jxx][2], joints[j22][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

        # plot x-braces on Row 1
        j11 = "a0bL".replace("a",str(i+1)).replace("b","3")
        j12 = "a0bL".replace("a",str(i+2)).replace("b","1")
        jxx = "a0bX".replace("a",str(i+1)).replace("b","4")
        j21 = "a0bL".replace("a",str(i+1)).replace("b","1")
        j22 = "a0bL".replace("a",str(i+2)).replace("b","3")
        x = [ joints[j11][0], joints[jxx][0], joints[j12][0] ]
        y = [ joints[j11][1], joints[jxx][1], joints[j12][1] ]
        z = [ joints[j11][2], joints[jxx][2], joints[j12][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')
        x = [ joints[j21][0], joints[jxx][0], joints[j22][0] ]
        y = [ joints[j21][1], joints[jxx][1], joints[j22][1] ]
        z = [ joints[j21][2], joints[jxx][2], joints[j22][2] ]
        ax.scatter(x,y,z, color='red', marker = "o", s = markersize)
        ax.plot3D(x,y,z, color='grey')

    # turn off all axes
    ax.set_axis_off()

    # rotate angle of 3D plot
    ax.view_init(6, -55)
    # set orientation to "persp"ective (ortho is also an option)
    ax.set_proj_type('persp')

    # do the math to make the scales the same on all axes
    max_range = np.array([maxX-minX, maxY-minY, maxZ-minZ]).max() / 2.0
    mid_x = (maxX+minX) * 0.5
    mid_y = (maxY+minY) * 0.5
    mid_z = (maxZ+minZ) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # make plot as tight as possible (ie, the least amount of whitespace around the plot)
    plt.margins(x=0, y=0)
    plt.tight_layout(pad=0)

    # Show the plot!
    # plt.show()

    # Convert plot to PNG image BEFORE CROPPING
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    #----------------------------------------------------------
    # The following is code I found online that i think is cool
    #----------------------------------------------------------
    # Encode the uncropped PNG image to base64 string
    # create Base64 encoded PNG file of the original uncropped version
    pngImageB64_uncropped = "data:image/png;base64," + base64.b64encode(pngImage.getvalue()).decode('utf8')
    #----------------------------------------------------------


    #----------------------------------------------------------
    # The following is code I found online that i think is cool
    #----------------------------------------------------------
    # Crop the image since I can't get rid of the extra whitespace on
    # the ISO plot since no axes are shown.
    # Use OpenCV to trim the whitespace.
    # Code cuts off the ML plane corners on the left and right, BUT, the
    # png file looks so better without so much useless whitespace.

    # redraw the canvas
    fig.canvas.draw()

    # convert canvas to image
    img_cv2 = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img_cv2  = img_cv2.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img_cv2 is rgb, convert to opencv's default bgr
    img_cv2 = cv2.cvtColor(img_cv2,cv2.COLOR_RGB2BGR)

    # # display image with opencv or any operation you like
    # cv2.imshow("plot",img_cv2) # shows the original plot before trimming
    # cv2.waitKey()

    original = img_cv2.copy()
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (25,25), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Perform morph operations, first open to remove noise, then close to combine
    noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

    # Find enclosing boundingbox and crop ROI
    coords = cv2.findNonZero(close)
    x,y,w,h = cv2.boundingRect(coords)
    cv2.rectangle(img_cv2, (x, y), (x + w, y + h), (36,255,12), 2)
    cropped_img = original[y:y+h, x:x+w]

    # # see the steps this code takes by uncomment the items below
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('close', close)
    # cv2.imshow('image', img_cv2)
    # cv2.imshow('crop', cropped_img)
    # cv2.waitKey()

    # covert cv2 image to a Base64 encoded PNG file
    retval, buffer = cv2.imencode('.png', cropped_img)
    cv2_base64_png = base64.b64encode(buffer).decode("utf-8")
    pngImageB64_cropped = "data:image/png;base64," +  cv2_base64_png
    #----------------------------------------------------------

    # return a tuple with both images
    return (pngImageB64_uncropped, pngImageB64_cropped)


##########
# Testing
#

# These two variables my app calcs its based user input
# they are provided as input here for testing purposes.
# Best bet is to leave these two variables alone.
plans = 3       # number of framing plans in the jacket.
# the following dictionary has all of the joint (node) numbers as keys and the
# X,Y, and Z coordinates are provided in a list.
jts = {'001L': [-38.125, -38.125, -123], '002L': [38.125, -38.125, -123], '003L': [-38.125, 38.125, -123], '004L': [38.125, 38.125, -123], '101L': [-37.75, -37.75, -120], '102L': [37.75, -37.75, -120], '103L': [-37.75, 37.75, -120], '104L': [37.75, 37.75, -120], '101P': [-37.75, -37.75, -120], '102P': [37.75, -37.75, -120], '103P': [-37.75, 37.75, -120], '104P': [37.75, 37.75, -120], '201L': [-28.07189430729605, -28.07189430729605, -42.57515445836834], '202L': [28.07189430729605, -28.07189430729605, -42.57515445836834], '203L': [-28.07189430729605, 28.07189430729605, -42.57515445836834], '204L': [28.07189430729605, 28.07189430729605, -42.57515445836834], '201P': [-28.07189430729605, -28.07189430729605, -42.57515445836834], '202P': [28.07189430729605, -28.07189430729605, -42.57515445836834], '203P': [-28.07189430729605, 28.07189430729605, -42.57515445836834], '204P': [28.07189430729605, 28.07189430729605, -42.57515445836834], '301L': [-20.875, -20.875, 15], '302L': [20.875, -20.875, 15], '303L': [-20.875, 20.875, 15], '304L': [20.875, 20.875, 15], '301P': [-20.875, -20.875, 15], '302P': [20.875, -20.875, 15], '303P': [-20.875, 20.875, 15], '304P': [20.875, 20.875, 15], '401L': [-20.375, -20.375, 19], '402L': [20.375, -20.375, 19], '403L': [-20.375, 20.375, 19], '404L': [20.375, 20.375, 19], '401P': [-20.375, -20.375, 19], '402P': [20.375, -20.375, 19], '403P': [-20.375, 20.375, 19], '404P': [20.375, 20.375, 19], '501L': [-20.0, -20.0, 22], '502L': [20.0, -20.0, 22], '503L': [-20.0, 20.0, 22], '504L': [20.0, 20.0, 22], '501P': [-20.0, -20.0, 22], '502P': [20.0, -20.0, 22], '503P': [-20.0, 20.0, 22], '504P': [20.0, 20.0, 22], '101X': [0.0, -32.19943823412452, -75.59550587299614], '103X': [0.0, 32.19943823412452, -75.59550587299614], '201X': [0.0, -23.94435038046757, -9.554803043740531], '203X': [0.0, 23.94435038046757, -9.554803043740531], '102X': [32.19943823412452, 0.0, -75.59550587299614], '104X': [-32.19943823412452, 0.0, -75.59550587299614], '202X': [23.94435038046757, 0.0, -9.554803043740531], '204X': [-23.94435038046757, 0.0, -9.554803043740531]}

# generate plots
image1, image2 = plot_iso_view(plans, jts ) # function returns a tuple so save to two variables

# create HTML code so images can be viewed in a browser.
image_html = '<html><img src="{}" width="400"><img src="{}" width="400"></html>'.format(image1, image2)


#----------------------------------------------------------
# The following is code I found online that i think is cool
#----------------------------------------------------------

# Temporary TESTING code to send image to browser window automatically
# Yes, the imports should be up top but I leave it in the "testing" area
# since this stuff gets commented out when it's implemented with the rest
# of the app.
import tempfile
import webbrowser
# send to browser
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    url = 'file://' + f.name
    f.write(image_html)
webbrowser.open(url)
