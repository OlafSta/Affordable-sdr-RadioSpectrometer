Here is a more indepth explination of the limitations of the inital model.


## 1. Opening and closing RTL object:
Each time the RTL sdr object is opened in python it adds a delay, this delay builds up to substantial over time (Compareson at the end of this section). 
Currently the SDR object is open at each frequency jump. 
This is fixed by combining the main function with the rtlsdr function into one function, then opening up the rtl sdr at the start of the recording/main function.

The code for this fix can be found in the V2.py section.

Comparing the version with and without the fix was done through excel. A number of recordings of 4 second duration where recorded, so the code recorded information at each frequency for 4 seconds and then did a fequency jump after. So i recorded the time taken to do 1,2,4,8,16,20,30,40 jumps for the two versions of the record function. The information was then plotted on excel as a time (y-axis) and no. Jumps (x-axis), knowing that the time set on the python code is 4 seconds per jump we can see the average time by fitting a slope to the plotted lines and trying to get them to be as close to 4 as possible. 
The V1 (vanilla) code had a slope of 5.45s/jump and the V2 code had a slope of 4.5s/jump. 
<img width="1064" height="605" alt="image" src="https://github.com/user-attachments/assets/f13f3b0a-a213-4e16-99b3-16a3f6afbb12" />


## 2. Reduce the number of loops
This works by trying to change the way the data is represented 
