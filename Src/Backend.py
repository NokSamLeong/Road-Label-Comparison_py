from os import listdir
import os
import pandas as pd
from pathlib import Path
import subprocess

class Backend:
    RLBpath = ""
    thisPy = Path(os.path.realpath(__file__))
    RLBpath = thisPy.parent.parent.parent.parent
    RLBpath = str(RLBpath)
    current_commend = ""
    current_index = 0
    try:
        frame = pd.read_excel(RLBpath + "\\result.xlsx", index_col=None, header=None)  # dataframe
        frame[0] = frame[0].astype(str)
    except IOError as e:
        frame = pd.DataFrame()
    currentKey = ""
    theList = []  # class variable, list of string, name of images which key isnt in the frame
    current = []  # class variable, list of string, name of currently-looking-at images
    stopRecord = False  # class variable, boolean, if finish all avaliable image
    checkboxBoo = []  # list of boolean
    isNone = False  # boolean, if None is selected

    def get_pre(self):
        if self.current_index >= 1:
            # check if data frame is empty and if currently looking at the first row
            # yes return empty list, otherwise the list of the previous key
            self.current_index -= 1
            pre_row = self.frame.iloc[self.current_index]
            temp = str(pre_row[0])
            target_set = []
            for file in listdir(self.RLBpath + "\\pic"):
                if file[0:16] == temp:
                    target_set.append(file)
                elif temp < file and not file[0:16] == temp:
                    break
                    # if saved key is smaller than current target from the loop,
                    # already passed the position where the key supposed to be and the images not in the path
            if len(target_set) == 0:
                return []
            self.current.reverse()  # put the current list back into the pending list
            self.theList.reverse()  # now vs previously using reverse -> for(append) n+n+n+k vs n+kn where k<=4
            self.theList.extend(self.current)
            self.theList.reverse()
            self.currentKey = pre_row[0]
            self.current = target_set
            self.checkboxBoo = []
            for image in self.current:  # put the previous row into the current list
                self.checkboxBoo.append(False)
            if pre_row[1] == "none":  # if selected none previously
                self.isNone = True
            else:   # if not none
                self.isNone = False
                for num in range(len(self.current)):
                    # if index of the recorded image == position num
                    if num == self.current.index(str(pre_row[1]+".PNG")):
                        self.checkboxBoo[num] = True
                    try:
                        if len(pre_row) > 2 and num == self.current.index(str(pre_row[2] + ".PNG")):
                            self.checkboxBoo[num] = True
                    except ValueError:
                        pass  # only one image selected
            self.current_commend = pre_row[3]
            return self.current

    # get next set of date
    # return list of strings that represent the files which share the say key
    # return True if Images are in the file, otherwise False
    def get_next(self):
        self.isNone = False
        self.stopRecord = False
        self.current = []
        self.checkboxBoo = []
        # current_index looking at the first empty row
        if self.current_index == len(self.frame.index):
            if len(self.theList) == 0:
                self.stopRecord = True
            else:
                self.currentKey = self.theList[0][0:16]
                # put the very first set of images into current list from theList
                while not len(self.theList) == 0 and self.theList[0][0:16] == self.currentKey:
                    self.current.append(self.theList.pop(0))
                for file in self.current:
                    self.checkboxBoo.append(False)

        elif self.current_index == len(self.frame.index)-1:  # if it looking at the last row
            self.current_index += 1  # move to the empty row
            self.get_next()  # execute the if statement above

        else:   # current_index looking in the middle of the dataframe but not last row
            self.current_index += 1  # move ot next row
            current_row = self.frame.iloc[self.current_index]
            self.currentKey = current_row[0]
            for file in listdir(self.RLBpath + "\\pic"):
                if current_row[0] in file:    # if the images are accessible, put into current list
                    self.current.append(file)
                    if file in self.theList:
                        self.theList.remove(file)
            for file in self.current:
                if current_row[1] == "none":
                    self.isNone = True
                    self.checkboxBoo.append(False)
                else:
                    # if false, the current_row contains the file
                    if not current_row[current_row.isin([file[0:-4]])].empty:
                        self.checkboxBoo.append(True)
                    else:
                        self.checkboxBoo.append(False)
            self.current_commend = current_row[3] if not current_row[3] == "" else self.currentKey
        return self.current
        # end of get_next function

    # Record the choice and comment
    # then write it into a .txt file using the tab delimited format
    # Parameter comment comment about the data set
    def write_in(self, comment):
        if comment == self.currentKey:
            comment = ""
        temp = ["", ""]
        if not self.isNone:
            for num in range(len(self.checkboxBoo)):
                if temp[0] == "" and self.checkboxBoo[num] and len(self.current) >= num:
                    temp[0] = self.current[num][0:-4]
                elif temp[1] == "" and self.checkboxBoo[num] and len(self.current) >= num:
                    temp[1] = self.current[num][0:-4]
        else:
            temp[0] = "none"
        if self.current_index == len(self.frame.index):  # write in a new row
            self.frame = self.frame.append(pd.Series([str(self.currentKey), temp[0], temp[1], comment]),
                                           ignore_index=True)
        else:
            upper = self.frame[0:self.current_index]
            lower = self.frame[self.current_index+1:]
            upper = upper.append(pd.Series([str(self.currentKey), temp[0], temp[1], comment]), ignore_index=True)
            self.frame = pd.concat([upper, lower])
            self.frame.reset_index(drop=True)
        self.frame.to_excel(r""+self.RLBpath + "\\result.xlsx", index=False, header=False)

    def get_commend(self):
        return self.current_commend

    def change_none(self):
        if self.isNone:
            self.isNone = False
        else:
            self.isNone = True

    def open_image(self):
        path = self.RLBpath+"\\pic\\"+self.current[0]
        subprocess.run(["explorer", path])

    # read the file
    def run(self):
        if not len(self.frame.index) == 0:
            for file in listdir(self.RLBpath + "\\pic"):
                # check if the key is in the excel file already
                if not file[0:16] in set(self.frame[0]):  # True if f is not in the frame
                    self.theList.append(file)
        else:
            self.theList = listdir(self.RLBpath + "\\pic")
        self.current_index = len(self.frame.index)  # looking at the first empty row

    def __init__(self):
        self.run()

    def delete_image(self):
        for file in listdir(self.RLBpath + "\\pic"):
            if file[0:16] in set(self.frame[0]):
                os.remove(self.RLBpath+"\\pic\\"+file)

    # True if finish all data set False if there is more data set
    def is_stop_record(self):
        return self.stopRecord

    # return current key
    def get_key(self):
        return self.currentKey

    # check if any check box is checked
    # return true if at least one box is checked otherwise false
    def is_any_checked(self):
        result = self.isNone
        for b in self.checkboxBoo:
            result = result or b
        return result


