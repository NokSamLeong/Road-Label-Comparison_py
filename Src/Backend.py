from os import listdir
import os
import pandas as pd
from PIL import Image


class Backend:
    RLBpath = ""
    thisPy = os.path.realpath(__file__)
    src, thisPy = os.path.split(thisPy)
    RLBpath, src = os.path.split(src)
    try:
        frame = pd.read_excel(RLBpath + "\\result.xlsx", index_col=None, header=None)  # dataframe
        frame[0] = frame[0].astype(str)
    except IOError as e:
        frame = pd.DataFrame()
    currentKey = ""
    theList = []
    current = []
    stopRecord = False
    # checkBox Array
    checkboxBoo = []
    isNone = False

    def change_none(self):
        if self.isNone:
            self.isNone = False
        else:
            self.isNone = True

    def get_pre(self):
        if not self.frame.empty:
            # check if data frame is empty
            # yes return empty string and empty list, otherwise return comment and the list of the previous key
            last_row = self.frame.tail(1).values.tolist()[0]
            temp = str(last_row[1]) + ".PNG"
            if temp in listdir(self.RLBpath + "\\pic") or :  # check if the images in the previous row are in the file
                self.current.reverse()  # put the current list back into the pending list
                for image in self.current:
                    self.theList.insert(0, image)
                self.currentKey = last_row[0]
                self.current = []
                self.checkboxBoo = []
                for image in listdir(self.RLBpath + "\\pic"):  # put the previous row into the current list
                    if image[0:16]+" " == self.currentKey:
                        self.checkboxBoo.append(False)
                        self.current.append(image)
                if last_row[1] == "none":  # if selected none previously
                    self.isNone = True
                    print("N")
                else:
                    self.isNone = False
                    for num in range(len(self.current)):
                        if num == self.current.index(last_row[1]+".PNG"):
                            self.checkboxBoo[num] = True
                print(self.checkboxBoo)
                self.frame.drop(self.frame.tail(1).index, inplace=True)  # remove last row from the frame
                com = last_row[3] if (len(last_row) >= 4 and not last_row[3] == "") else self.currentKey
                return com, self.current
            else:
                return "", []

    # get next set of date
    # return list of strings that represent the files which share the say key
    def get_next(self):
        # check if the next one in the dataframe yes then read from it, no them get from the list
        self.isNone = False
        self.current = []
        self.checkboxBoo = []
        if len(self.theList) != 0:
            self.currentKey = self.theList[0][0:16]
            while len(self.theList) != 0 and self.theList[0][0:16] == self.currentKey:
                self.current.append(self.theList.pop(0))
        else:
            self.stopRecord = True
        for f in self.current:
            self.checkboxBoo.append(False)
        return self.current

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
                    temp[0] = self.current[num][0:28]
                elif temp[1] == "" and self.checkboxBoo[num] and len(self.current) >= num:
                    temp[1] = self.current[num][0:28]
        else:
            temp[0] = "none"
        self.frame = self.frame.append(pd.Series([self.currentKey+" ", temp[0], temp[1], comment]), ignore_index=True)
        self.frame.to_excel(r""+self.RLBpath + "\\result.xlsx", index=False, header=False)

    def open_image(self):
        filename = self.RLBpath + "\pic\\" + self.current[0]
        image = Image.open(filename)
        image.show()

    # read the file
    def run(self):
        for f in listdir(self.RLBpath + "\\pic"):
            self.theList.append(f)

    def __init__(self):
        self.run()



