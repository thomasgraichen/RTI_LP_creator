'''
Created on 20.08.2016

@author: Thomas Graichen (www.tgraichen.de)

'''

import bpy
import math
import os

#<USER VARs>
pointPrefix = "posVert."
outputFilename = "realLPs.txt"
lightName = "Sun"
#</USER VARs>

def myTranslate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

bpy.ops.object.select_all(action='DESELECT')

lightObj = bpy.data.objects[lightName]
#select and activate camera in scene...
lightObj.select = True
bpy.context.scene.objects.active = lightObj
#set our framecounter start
framecounter = 1
#initialize our DICT
result = {}

for obj in bpy.data.objects:
	#for all points...
	if pointPrefix in obj.name:
		#set frame...
		bpy.context.scene.frame_set(framecounter)
		#move light to point's location...
		lightObj.location = obj.location
		#insert location- and rotation-keyframe for light...
		bpy.ops.anim.keyframe_insert_menu(type='Location')
		#normalize for RTIbuilder input and write light location into LIST...
		loc = []
		loc.append( myTranslate(lightObj.location[0], -1, 1, -0.99999999, 0.99999999) ) #ensuring we are not above abs(1) due to FPprecision
		loc.append( myTranslate(lightObj.location[1], -1, 1, -0.99999999, 0.99999999) )
		loc.append( myTranslate(lightObj.location[2], -1, 1, -0.99999999, 0.99999999) )
		#put LIST into DICT (key = frame)...
		result[framecounter] = loc
		#increment framecounter...
		framecounter += 1
#This is how our DCIT should look like:   { # : [locX, locY, locZ] }
#</set frame, light position and rotation, repeat>

#<write DICT to TXT file>
with open(outputFilename, "w") as text_file:
	objList = []
	for obj in bpy.data.objects:
		#for all points...
		if pointPrefix in obj.name:
			objList.append(obj)
	#this is our header...
	text_file.write( str( len(objList) ) + "\n")
	
	for frame, location in result.items():
		text_file.write("ico_" + str(frame).zfill(2) + ".jpg" + "       ")
		itemcounter = 1
		for item in location:
			if itemcounter < 3:
				#add our location items (SPACE is separator)
				text_file.write('{:.8f}'.format(item) + " ")
				itemcounter += 1
			else:
				#add our location items (SPACE is separator)
				text_file.write('{:.8f}'.format(item))
				itemcounter += 1
		#add newline at end of line
		text_file.write("\n")
#</write DICT to TXT file>

#deselect all...
lightObj.select = False
bpy.ops.object.select_all(action='DESELECT')