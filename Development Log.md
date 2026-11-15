# Development Log

<img width="409" height="277" alt="image" src="https://github.com/user-attachments/assets/a854d7ba-37c2-484a-8115-d3d88dc3652c" />

## 19-20 October - Creating Starter Files

I created the first basic starter files for the data viewer into the github repository. It includes the app.py file, data\_visualiser file, and file\_manager file. The next stage is to do the chat app and to improve the Data Visualiser (local mode)

## 20 October - Chat Files

I created the chat\_app and chat\_message files for the project. Next will be actually starting the code for the Data Management System

## 21 October Onwards - MVC \& Login Begin 

## Local Mode Development

### Local View - After Implementation 
<img width="1914" height="998" alt="image" src="https://github.com/user-attachments/assets/26737ec8-f747-4f62-8009-2e2707b2aa73" />

### Local Controller
<img width="337" height="162" alt="image" src="https://github.com/user-attachments/assets/e88797e0-cb70-4e43-9fb6-a95847e97aa0" />
<br>
The initialisers. 

#### Draw Figure 
The _draw_figure method inside the local controller is the block of code that I made to insert MatPlogLib inside of the freesmiplegui inside the UI. I did this as a canvas <br>
<img width="557" height="235" alt="image" src="https://github.com/user-attachments/assets/e3e21fa3-0b18-4aff-96b9-e7d073bd41ce" /> <br>
The block of code above shows the widget and canvas being created, allowing it to be used later on within FreeSimpleGUI. <br>

<img width="409" height="277" alt="image" src="https://github.com/user-attachments/assets/046e8b3c-c86a-481f-974c-b690ec66fd7c" /> <br>

I used Tkinter to generate the chart when the user generates a table and it gives the option for a toolbar. 

## Headless testing 
I created over 40 headless tests that all pass, checking the variety of the application to check if it works. <br>
<img width="650" height="241" alt="image" src="https://github.com/user-attachments/assets/f01fd491-8d44-4822-b9e9-1478b1548b2e" />

## Remote Mode Development 
I Have started making remote mode after completing local mode. I will not make the DES and graphing yet, and just create the multiple sessions and allowing multi-threading for allowing many people at once to view the chat and data. 

## Issues had
I did struggle with the multiprocessing as I accidentally made it GUI dependent, although I had fixed it and it did not take long to bring in multiprocessing.<br>
I had not finished everything in time; the main functionality is working, although I do not have it where you can make a private session inside the GUI. All sessions made in the GUI are automatically public.<br>
I ended up making a new file called remote_worker, which is what works with all the database operations and deals with the repositories and MongoDB connection.

## Things that went well
I actually ended up getting most of the functionality completed. 
The core functionality works, the DES display shows up, it allows users to zoom,/pan. It allows users to login with their credentials, or make a new account, you can select sessions, upload data, and there is a chat in remote mode. 


