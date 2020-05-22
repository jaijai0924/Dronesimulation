#Abdulaziz Macabangon
#Andrew Paguntalan
#ENGR423
#Final Project programming track

import LocoDroneX
from tkinter import *
from tkinter import ttk

#need this to create a window for Tkinter
root = Tk()
root.geometry("200x200")

#Label 1 for a prompt to pick a route
lbl = Label(root, text="Pick a route!")

lbl.grid(row = 0, column = 0)

lbl2 = Label(root, text ="square: glass: triangle: ")
lbl2.grid(row = 1, column = 0)
textBox = Text(root, width = 7,height = 1)
textBox.grid(row = 2, column = 0)

lbl3 = Label(root, text ="Pick a desired take of altitude!")
lbl3.grid(row = 3, column = 0)

textBox2 = Text(root, width = 7,height = 1)
textBox2.grid(row = 4 , column = 0)

lbl4 = Label(root, text ="Geofence length!")
lbl4.grid(row = 5, column = 0)

textBox3 = Text(root, width = 7,height = 1)
textBox3.grid(row = 6 , column = 0)


#function for the click event when a user inputs their entry
def myClick():
    #1.0/end1-c means start from the beginning character 
    #and the other parts means that the character that is autuomatically 
    #created it deletes that in the input 
    value = textBox.get("1.0", "end-1c")
    #call locodrone instance 
    ldX = LocoDroneX.LocoDroneX()
    ldX.connect('127.0.0.1:14540')
    #mission mode as we're going to upload custom waypoints
    ldX.changeMode("MISSION")
    #geofencing purposes, call a maximum edglen a drone can go
    geofen = textBox3.get("1.0", "end-1c")
    edglen = int(geofen)
    #converts meters into latitude and logitude for geofencing 
    ldX.getTotalDisplacement(edglen)
    #start position  get current start position
    #get data returns a dictionary
    startPos = ldX.getData(LocoDroneX.GET_POSITION)
    #end post if you don't want to go back to original location 
    #endPos = {'lat': startPos['lat', 'lon':startPos['lon'],'alt':ldX.takeoffAlt]}
    
    #approximate difference in lat and lon for input distance in meters
    distance = ldX.getTotalDisplacement(5)
    #Creates waypoints dictionary 
    waypoints = {'points': [] }
    #take off altitude input
    takeoff = textBox2.get("1.0", "end-1c")
    #overrides the takeoff altitude
    ldX.takeoffAlt = int(takeoff)
    #if statement was created inside the def function as I was having alot of issues
    #with global scopes for tkinter entries
    if value == 'square' :
        #nested if statement to implement geofencing 
        if edglen > 200: 
            ldX.disconnect() 
        else: 
            #square waypoints
            waypoints['points'].append([startPos['lat'], startPos['lon'] + distance[1], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'] + distance[0], startPos['lon'] +distance[1], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'] + distance[0], startPos['lon'], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'], startPos['lon'], ldX.takeoffAlt])
            #inserts the first waypoint in the datalogs 
            ldX.waypoints.insert(0, [startPos['lat'], startPos['lon'], startPos['alt']])
            #creates loggers
            ldX.createLoggers(LocoDroneX.LOG_DATA, .2)
            ldX.startMission(waypoints)
    elif value == 'glass':
        if edglen > 200: 
            ldX.disconnect()
    #hourglass waypoints 
        else:
            waypoints['points'].append([startPos['lat'], startPos['lon'], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'], startPos['lon'] + distance[1], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'] + distance[0], startPos['lon'], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'] + distance[0], startPos['lon'] + distance[1], ldX.takeoffAlt])
            ldX.waypoints.insert(0, [startPos['lat'], startPos['lon'], startPos['alt']])
            ldX.createLoggers(LocoDroneX.LOG_DATA, .2)
            ldX.startMission(waypoints)
    elif value == 'triangle':
        if edglen > 200: 
            ldX.disconnect() 
        else:
            waypoints['points'].append([startPos['lat'], startPos['lon'], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'], startPos['lon'] + distance[1], ldX.takeoffAlt])
            waypoints['points'].append([startPos['lat'] + distance[0], startPos['lon'], ldX.takeoffAlt])
            ldX.waypoints.insert(0, [startPos['lat'], startPos['lon'], startPos['alt']])
            ldX.createLoggers(LocoDroneX.LOG_DATA, .2)
            ldX.startMission(waypoints)          
    else: 
        ldX.disconnect()


btn = Button(root, height= 1, width=15, text= "Enter", command=lambda: myClick())
btn.grid(row = 7, column = 0)


    
#needed to keep the window open for GUI 
mainloop()