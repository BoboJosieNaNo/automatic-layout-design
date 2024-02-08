#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 19:51:42 2023

@author: bobonano
"""

#!/usr/bin/env python
# coding: utf-8

# In[75]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math
from random import random


# In[76]:


#revised general guillotine algorithm

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.index=None
    
    def area(self):
        return self.width * self.height    
    
    def collide(self, rect):
        return (self.x < rect.x + rect.width and
                self.x + self.width > rect.x and
                self.y < rect.y + rect.height and
                self.y + self.height > rect.y)
        
class Guillotine:
    def __init__(self, container_width, container_height):
        self.container_width = container_width
        self.container_height = container_height
        self.used_rectangles = []
        self.free_rectangles = [Rectangle(container_width, container_height)]
        
    def find_position(self, rect):
        best_area = float("inf")
        best_rect = None
        best_rec_x = float("inf")
        best_rec_y = float("inf")
        
        for free_rect in self.free_rectangles:  # blank space
            non_overlapping = True
            for used_rect in self.used_rectangles:
                if free_rect.collide(used_rect):
                    self.free_rectangles.extend(self.split_rect(free_rect, used_rect))
                    non_overlapping = False
            if not non_overlapping:
                self.free_rectangles.remove(free_rect)    
                
        for free_rect in self.free_rectangles: #blank space
            non_overlapping = True
            for used_rect in self.used_rectangles:
                if free_rect.collide(used_rect):
                    non_overlapping = False
                    break
            if non_overlapping and rect.width <= free_rect.width and rect.height <= free_rect.height: 
                area = free_rect.width * free_rect.height - rect.width * rect.height
                if free_rect.y < best_rec_y:
                    if free_rect.x < best_rec_x:
                        if area < best_area: #minimum waste
                            best_area = area
                            best_rect = free_rect 
                            best_rec_x = free_rect.x
                            best_rec_y = free_rect.y
                        else:
                            best_area = area
                            best_rect = free_rect 
                            best_rec_x = free_rect.x
                            best_rec_y = free_rect.y
                    else:
                        best_area = area
                        best_rect = free_rect 
                        best_rec_x = free_rect.x
                        best_rec_y = free_rect.y              

        return best_rect

    def split_rect(self, free_rect, rect):
        new_rects = []

            #top
        if rect.x < free_rect.x + free_rect.width and rect.x + rect.width > free_rect.x:
            if rect.y > free_rect.y and rect.y < free_rect.y + free_rect.height:
                new_rect = Rectangle(free_rect.width, rect.y - free_rect.y-0.25)
                new_rect.x = free_rect.x
                new_rect.y = free_rect.y
                new_rects.append(new_rect)
            #bottom
            if rect.y + rect.height < free_rect.y + free_rect.height:
                new_rect = Rectangle(free_rect.width, free_rect.y + free_rect.height - (rect.y + rect.height)-0.25)
                new_rect.x = free_rect.x
                new_rect.y = rect.y + rect.height+0.25
                new_rects.append(new_rect)
            #left
        if rect.y < free_rect.y + free_rect.height and rect.y + rect.height > free_rect.y:
            if rect.x > free_rect.x and rect.x < free_rect.x + free_rect.width:
                new_rect = Rectangle(rect.x - free_rect.x-0.25, free_rect.height)
                new_rect.x = free_rect.x
                new_rect.y = free_rect.y
                new_rects.append(new_rect)
            #right
            if rect.x + rect.width < free_rect.x + free_rect.width:
                new_rect = Rectangle(free_rect.x + free_rect.width - (rect.x + rect.width)-0.25, free_rect.height)
                new_rect.x = rect.x + rect.width+0.25
                new_rect.y = free_rect.y
                new_rects.append(new_rect)

        # Remove used_rect from split_rectangles
        new_rects = [r for r in new_rects if not r.collide(rect)]

        return new_rects
   

    def place_rect(self, rect):
        position = self.find_position(rect)

        if position is None:
            return False
        else:
            rect.x = position.x
            rect.y = position.y
            self.used_rectangles.append(rect)

        new_free_rects = []

        for free_rect in self.free_rectangles:
            if free_rect == position:
                new_free_rects.extend(self.split_rect(free_rect, rect))
            else:
                new_free_rects.append(free_rect)

        self.free_rectangles = new_free_rects

        return True
        
def visualize(width, height, items, No):

    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)
    axes.add_patch(
        patches.Rectangle(
            (0, 0),  # (x,y)
            width,  # width
            height,  # height
            hatch='x',
            fill=False,
        )
    )
    for item_name, item_list in items.items():
        for x, y, w, h in item_list:
            axes.add_patch(
                patches.Rectangle(
                    (x, y),  # (x,y)
                    w,  # width
                    h,  # height
                    color=(random(), random(), random()),
                )
            )
            axes.text(x, y, item_name[0:6])

    axes.set_xlim(0, width)
    axes.set_ylim(0, height)
    plt.gca().set_aspect('equal', adjustable='box') 
    
    position_note = '\n'.join([f'{key}: {value}' for key, value in items.items()])
    fig.text(0.1, 0.02, position_note, fontsize=12, ha='left', va='top')

    name='Gemline_Layout'+str(No)+'.pdf'
    fig.savefig(name, bbox_inches='tight')
    
    plt.show()

def number_up(original_list,RectIndex0):
    grouped_rectangles = {} #each group is that rect has same index[0]
    up_dict={}
    for rect in original_list:
        if rect.index[0] not in grouped_rectangles:
            grouped_rectangles[rect.index[0]] = []
        grouped_rectangles[rect.index[0]].append(rect)

    for idx, rects in grouped_rectangles.items():
        sum_idx = len(rects)
        up_dict[idx] = sum_idx

    return up_dict[RectIndex0]


# In[83]:


#input EXCEL data file:
inputfile = pd.read_excel('Copy of Gemline Data _Spec Sheets.xlsx', sheet_name='Spec Sheets')
#inputfile = inputfile.drop('Opt Mfg Sel', axis=1)
inputfile["Ship Date"] = pd.to_datetime(inputfile["Ship Date"])

#sort by ship date and order quantity
inputfile = inputfile.sort_values(by=["Ship Date", "Required Qty"], ascending=[True, True])

# Create a new column for the shipdate groups
inputfile["Ship Date_group"] = pd.cut(inputfile["Ship Date"], bins=pd.date_range(start="2022-10-02", end="2022-12-30", freq="2D"))

# Sort the data by shipdate group and orderquantity
inputfile = inputfile.sort_values(["Ship Date_group", "Required Qty"])

inputfile = inputfile.reset_index(drop=True)

# Assume you have a Pandas Series object called size_notes
size_notes = pd.Series(inputfile["Notes"])

# Define a regular expression pattern to match the size information
pattern = r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)'

# Extract the size information from each string in the Series and create a new DataFrame
size_df = size_notes.str.extractall(pattern).reset_index(level=1, drop=True)
size_df.columns = ['Width', 'Height']
size_df = size_df.astype(float)

# Combine the "Width" and "Height" columns into a tuple for each row
size_tuples = size_df.apply(lambda row: (row['Width'], row['Height']), axis=1)

#add width and height to dataframe
inputfile['Width']=size_df['Width']
inputfile['Height']=size_df['Height']

inputfile = inputfile.dropna(how='any')
inputfile = inputfile.reset_index(drop=True)
inputfile['No'] = range(1, len(inputfile)+1)

inputfile = inputfile[(inputfile['Ship Date'] == "2022-10-03") | (inputfile['Ship Date'] == "2022-10-04") | (inputfile['Ship Date'] == "2022-10-05") | (inputfile['Ship Date'] == "2022-10-06") | (inputfile['Ship Date'] == "2022-10-07")  | (inputfile['Ship Date'] == "2022-10-08")  | (inputfile['Ship Date'] == "2022-10-09")  | (inputfile['Ship Date'] == "2022-10-10")  | (inputfile['Ship Date'] == "2022-10-11")  | (inputfile['Ship Date'] == "2022-10-12")  | (inputfile['Ship Date'] == "2022-10-13")  | (inputfile['Ship Date'] == "2022-10-14") ]

#create an empty output dataframe
outputfile = inputfile.copy()
outputfile.insert(0, 'File', '')
outputfile.insert(1, 'Waste', '')
outputfile.insert(2, 'Sheets', '')
outputfile.insert(3, '# Up', '')


# In[84]:


LayoutPDF=0
while not inputfile.empty:
    
    #set order quantity
    qty_uqe_logo={i: inputfile.loc[i, 'Required Qty'] for i in range(inputfile.shape[0]) if i not in [258,259,270,275,276,277,278,298,300,305,306,307,308,309,310,312,313,314]}

    #set repeated time
    repeat_uqe_logo={i: math.ceil(qty_uqe_logo[i]/qty_uqe_logo[0]) for i in list(qty_uqe_logo.keys())}

    #input rectangles
    rects = []
    index_list=[]
    for i in list(repeat_uqe_logo.keys()):
        for j in range(repeat_uqe_logo[i]):
            rects.append(Rectangle(inputfile.loc[i, 'Width'], inputfile.loc[i, 'Height']))
            index_list.append([i,j])

    #add index to each rect
    for i, rect in enumerate(rects):
        rect.index=index_list[i]

    #define to list
    processed_rects=[]

    # Example code for using the Guillotine class
    if __name__ == '__main__':
        ##input
        # Define the container size
        container_width = 17.83
        container_height = 11.27 

        #temporary list
        processing0_rects=[]
        processing1_rects=[]
        processing25_rects=[]
        processing50_rects=[]
        processing100_rects=[]
        
        #batch joining the temporary list  
        filled0_size=0
        filled1_size=0
        filled25_size=0
        filled50_size=0
        filled100_size=0
        for rect in rects:
            if inputfile.loc[rect.index[0],'Required Qty']==1:
                filled1_size+=rect.width*rect.height
                if filled1_size>2*(container_width*container_height):
                    break
                else:
                    processing1_rects.append(rect)
            elif inputfile.loc[rect.index[0],'Required Qty']==25:
                filled25_size+=rect.width*rect.height
                if filled25_size>2*(container_width*container_height):
                    break
                else:
                    processing25_rects.append(rect)
            elif inputfile.loc[rect.index[0],'Required Qty']==50:
                filled50_size+=rect.width*rect.height
                if filled50_size>2*(container_width*container_height):
                    break
                else:
                    processing50_rects.append(rect)                    
            elif inputfile.loc[rect.index[0],'Required Qty']==100:
                filled100_size+=rect.width*rect.height
                if filled100_size>2*(container_width*container_height):
                    break
                else:
                    processing100_rects.append(rect)
            else:
                filled0_size+=rect.width*rect.height
                if filled0_size>2*(container_width*container_height):
                    break
                else:
                    processing0_rects.append(rect)
                    
                    
        #sort by area
        rects_sorted0 = sorted(processing0_rects, key=lambda x: x.area(), reverse=True)
        rects_sorted1 = sorted(processing1_rects, key=lambda x: x.area(), reverse=True)
        rects_sorted25 = sorted(processing25_rects, key=lambda x: x.area(), reverse=True)
        rects_sorted50 = sorted(processing50_rects, key=lambda x: x.area(), reverse=True)
        rects_sorted100 = sorted(processing100_rects, key=lambda x: x.area(), reverse=True)

        # Initialize the Guillotine algorithm
        guillotine0 = Guillotine(container_width, container_height)
        guillotine1 = Guillotine(container_width, container_height)
        guillotine25 = Guillotine(container_width, container_height)
        guillotine50 = Guillotine(container_width, container_height)
        guillotine100 = Guillotine(container_width, container_height)

        # Place the rectangles into the container
        for rect in rects_sorted0:
            success = guillotine0.place_rect(rect)
            if not success: #not in used_rectangles
                processing0_rects.remove(rect)
                print("Failed to place rectangle", rect.width, "x", rect.height)
            if success:
                if rect.index[0] not in processed_rects:
                    processed_rects.append(rect.index[0])

        for rect in rects_sorted1:
            success = guillotine1.place_rect(rect)
            if not success: #not in used_rectangles
                processing1_rects.remove(rect)
                print("Failed to place rectangle", rect.width, "x", rect.height)
            if success:
                if rect.index[0] not in processed_rects:
                    processed_rects.append(rect.index[0])                  
                    
        for rect in rects_sorted25:
            success = guillotine25.place_rect(rect)
            if not success: #not in used_rectangles
                processing25_rects.remove(rect)
                print("Failed to place rectangle", rect.width, "x", rect.height)
            if success:
                if rect.index[0] not in processed_rects:
                    processed_rects.append(rect.index[0])                 
                    
        for rect in rects_sorted50:
            success = guillotine50.place_rect(rect)
            if not success: #not in used_rectangles
                processing50_rects.remove(rect)
                print("Failed to place rectangle", rect.width, "x", rect.height)
            if success:
                if rect.index[0] not in processed_rects:
                    processed_rects.append(rect.index[0])
                    
        for rect in rects_sorted100:
            success = guillotine100.place_rect(rect)
            if not success: #not in used_rectangles
                processing100_rects.remove(rect)
                print("Failed to place rectangle", rect.width, "x", rect.height)
            if success:
                if rect.index[0] not in processed_rects:
                    processed_rects.append(rect.index[0])
                    
        ##output

        # Print the packing result (position)
        PackingResult0=[]
        print("Packing result:")
        for rect in processing0_rects:
            PackingResult0.append((rect.index,(rect.x,rect.y,rect.width,rect.height)))
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): x="+str(rect.x)+", y="+str(rect.y))
        
        PackingResult1=[]
        print("Packing result:")
        for rect in processing1_rects:
            PackingResult1.append((rect.index,(rect.x,rect.y,rect.width,rect.height)))
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): x="+str(rect.x)+", y="+str(rect.y))
        
        PackingResult25=[]
        print("Packing result:")
        for rect in processing25_rects:
            PackingResult25.append((rect.index,(rect.x,rect.y,rect.width,rect.height)))
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): x="+str(rect.x)+", y="+str(rect.y))
            
        PackingResult50=[]
        print("Packing result:")
        for rect in processing50_rects:
            PackingResult50.append((rect.index,(rect.x,rect.y,rect.width,rect.height)))
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): x="+str(rect.x)+", y="+str(rect.y))
            
        PackingResult100=[]
        print("Packing result:")
        for rect in processing100_rects:
            PackingResult100.append((rect.index,(rect.x,rect.y,rect.width,rect.height)))
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): x="+str(rect.x)+", y="+str(rect.y))

        
        #wasted space
        used_space0=0
        for rect in processing0_rects:
            used_space0+=rect.width*rect.height
        wasted_space0=1-used_space0/(container_width*container_height)
        print("%wasted space0 = "+str(wasted_space0))
        
        used_space1=0
        for rect in processing1_rects:
            used_space1+=rect.width*rect.height
        wasted_space1=1-used_space1/(container_width*container_height)
        print("%wasted space1 = "+str(wasted_space1))
        
        used_space25=0
        for rect in processing25_rects:
            used_space25+=rect.width*rect.height
        wasted_space25=1-used_space25/(container_width*container_height)
        print("%wasted space25 = "+str(wasted_space25))
        
        used_space50=0
        for rect in processing50_rects:
            used_space50+=rect.width*rect.height
        wasted_space50=1-used_space50/(container_width*container_height)
        print("%wasted space50 = "+str(wasted_space50))
        
        used_space100=0
        for rect in processing100_rects:
            used_space100+=rect.width*rect.height
        wasted_space100=1-used_space100/(container_width*container_height)
        print("%wasted space100 = "+str(wasted_space100))

        # #up
        for rect in processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, '# Up'] = number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])        
        
        #amount of carrier sheet
        SheetAmount0=0
        for rect in processing0_rects:
            s=math.ceil(qty_uqe_logo[rect.index[0]]/number_up(processing0_rects,rect.index[0]))
            if s>SheetAmount0:
                SheetAmount0=s
            else:
                continue

        for rect in processing0_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Sheets'] = SheetAmount0
            
        print("total amount of sheets0="+str(SheetAmount0))
        
        SheetAmount1=0
        for rect in processing1_rects:
            s=math.ceil(qty_uqe_logo[rect.index[0]]/number_up(processing1_rects,rect.index[0]))
            if s>SheetAmount1:
                SheetAmount1=s
            else:
                continue

        for rect in processing1_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Sheets'] = SheetAmount1
            
        SheetAmount25=0
        for rect in processing25_rects:
            s=math.ceil(qty_uqe_logo[rect.index[0]]/number_up(processing25_rects,rect.index[0]))
            if s>SheetAmount25:
                SheetAmount25=s
            else:
                continue

        for rect in processing25_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Sheets'] = SheetAmount25
            
        SheetAmount50=0
        for rect in processing50_rects:
            s=math.ceil(qty_uqe_logo[rect.index[0]]/number_up(processing50_rects,rect.index[0]))
            if s>SheetAmount50:
                SheetAmount50=s
            else:
                continue

        for rect in processing50_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Sheets'] = SheetAmount50            
            
        SheetAmount100=0
        for rect in processing100_rects:
            s=math.ceil(qty_uqe_logo[rect.index[0]]/number_up(processing100_rects,rect.index[0]))
            if s>SheetAmount100:
                SheetAmount100=s
            else:
                continue

        for rect in processing100_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Sheets'] = SheetAmount100
            
        #wasted unneeded transfer
        for rect in processing0_rects:
            WastedTransfer0=SheetAmount0*number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])-qty_uqe_logo[rect.index[0]]
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Waste'] = WastedTransfer0
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): "+str(WastedTransfer0))

        for rect in processing1_rects:
            WastedTransfer1=SheetAmount1*number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])-qty_uqe_logo[rect.index[0]]
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Waste'] = WastedTransfer1
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): "+str(WastedTransfer1))            
            
        for rect in processing25_rects:
            WastedTransfer25=SheetAmount25*number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])-qty_uqe_logo[rect.index[0]]
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Waste'] = WastedTransfer25
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): "+str(WastedTransfer25))            
            
        for rect in processing50_rects:
            WastedTransfer50=SheetAmount50*number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])-qty_uqe_logo[rect.index[0]]
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Waste'] = WastedTransfer50
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): "+str(WastedTransfer50))            
            
        for rect in processing100_rects:
            WastedTransfer100=SheetAmount100*number_up((processing0_rects+processing1_rects+processing25_rects+processing50_rects+processing100_rects),rect.index[0])-qty_uqe_logo[rect.index[0]]
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'Waste'] = WastedTransfer100
            print(rect.index,"Rectangle("+str(rect.width)+", "+str(rect.height)+"): "+str(WastedTransfer100))            
            
            
        ##Visualization
        # Create a dictionary to map the index i to the logo name
        LogoName_dict = {}
        for i, row in inputfile.iterrows():
            LogoName_dict[i] = row['Logo Name']

        # Create a dictionary to store the (x, y, w, h) values for each logo name
        LogoNameValue_dict0 = {}
        for item in PackingResult0:
            i = item[0][0]
            logo_name = LogoName_dict[i]
            rect = item[1]
            if logo_name in LogoNameValue_dict0:
                LogoNameValue_dict0[logo_name].append(rect)
            else:
                LogoNameValue_dict0[logo_name] = [rect]

        LayoutPDF+=1
        visualize(17.83, 11.27, LogoNameValue_dict0, LayoutPDF)

        #filename for each layout with position
        for rect in processing0_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'File'] = 'Gemline_Layout'+str(LayoutPDF)+'.pdf'           
        
        LogoNameValue_dict1 = {}
        for item in PackingResult1:
            i = item[0][0]
            logo_name = LogoName_dict[i]
            rect = item[1]
            if logo_name in LogoNameValue_dict1:
                LogoNameValue_dict1[logo_name].append(rect)
            else:
                LogoNameValue_dict1[logo_name] = [rect]

        LayoutPDF+=1
        visualize(17.83, 11.27, LogoNameValue_dict1, LayoutPDF)

        #filename for each layout with position
        for rect in processing1_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'File'] = 'Gemline_Layout'+str(LayoutPDF)+'.pdf'           
        
        LogoNameValue_dict25 = {}
        for item in PackingResult25:
            i = item[0][0]
            logo_name = LogoName_dict[i]
            rect = item[1]
            if logo_name in LogoNameValue_dict25:
                LogoNameValue_dict25[logo_name].append(rect)
            else:
                LogoNameValue_dict25[logo_name] = [rect]

        LayoutPDF+=1
        visualize(17.83, 11.27, LogoNameValue_dict25, LayoutPDF)       

        #filename for each layout with position
        for rect in processing25_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'File'] = 'Gemline_Layout'+str(LayoutPDF)+'.pdf'           
        
        LogoNameValue_dict50 = {}
        for item in PackingResult50:
            i = item[0][0]
            logo_name = LogoName_dict[i]
            rect = item[1]
            if logo_name in LogoNameValue_dict50:
                LogoNameValue_dict50[logo_name].append(rect)
            else:
                LogoNameValue_dict50[logo_name] = [rect]

        LayoutPDF+=1
        visualize(17.83, 11.27, LogoNameValue_dict50, LayoutPDF)        

        #filename for each layout with position
        for rect in processing50_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'File'] = 'Gemline_Layout'+str(LayoutPDF)+'.pdf'           
        
        LogoNameValue_dict100 = {}
        for item in PackingResult100:
            i = item[0][0]
            logo_name = LogoName_dict[i]
            rect = item[1]
            if logo_name in LogoNameValue_dict100:
                LogoNameValue_dict100[logo_name].append(rect)
            else:
                LogoNameValue_dict100[logo_name] = [rect]

        LayoutPDF+=1
        visualize(17.83, 11.27, LogoNameValue_dict100, LayoutPDF)                
        
        #filename for each layout with position
        for rect in processing100_rects:
            outputfile.loc[inputfile.loc[rect.index[0],'No']-1, 'File'] = 'Gemline_Layout'+str(LayoutPDF)+'.pdf'            

        #updat the dataframe
        for i in processed_rects:
            inputfile.drop(i, inplace=True)

        inputfile = inputfile.reset_index(drop=True)
        


# In[85]:


#export to excel file
outputfile.to_excel('Gemline_Output.xlsx', index=False)


# In[ ]:



