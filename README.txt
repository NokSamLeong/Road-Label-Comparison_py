Road Label Comparison UserInterface Python Version
by Nok Sam Leong 
first version 03/08/2020
last update 03/013/2020

Execuable path: RoadLabelComparison\Src\dist\RLC\RoadLabelComparison.exe
Image path: RoadLabelComparison\pic
Result path: RoadLabelComparison\result.xlsx

The program was specifically designed for the road label comparison task.
at least 1 and at most 4 different images for each key. 

Instruction
Pressing << or >> will save your selection
non-labeled checkbox is considered to be an invalid selection
put images in the 'pic' file. Recommend to put less than 100 images each time.
Open button opens the first image in the current set
Open button will work properly only if the default photo viewer app is Window Photo Viewer
Maximum selection for each key is 2 labels.
if None is selected, no labels will be marked even if they are selected.
Do not need to delete the key string in the comment field. It is there for convenience.
Make sure to delete the images which you already give judgment to.
The result is saved as an Excel file.

Update
03/09/2020	fixed open butten

03/13/2020	add << button
		giving choice to remove images