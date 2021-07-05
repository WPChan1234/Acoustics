from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import ezdxf
import tkinter.messagebox
import collections



tkinter.messagebox.showinfo('DXF 2 Segment list: Introduction', 'Convert Duct segment to segment list' )

docPath = askopenfilename(title='Select DXF File with "Duct Segement" Blocks only ------------------(MIN 2 BLOCKS!!)')
doc = ezdxf.readfile(docPath)
print(docPath)


msp = doc.modelspace()
List = []
SegList=[]
BendList=[]
SegFile=[]
ListFile=["Seg/BEND ID,WxD(MM),Length,Lining, Precedent_Segment, Remark"]


# Duplicacy check#

for insert in msp.query('INSERT'):
    List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]

    if any("SEG_ID" in s for s in List): ### Filter applied to search Segment blocks only ###
        SEG_ID = List[0][1]
        SegList.append(SEG_ID)
    if any("BEND_ID" in s for s in List): ### Filter applied to search Bend blocks only ###
        BEND_ID = List[0][1]
        BendList.append(BEND_ID)


Duplicated_SEG = [item for item, count in collections.Counter(SegList).items() if count > 1]
Duplicated_BEND = [item for item, count in collections.Counter(BendList).items() if count > 1]

tkinter.messagebox.showinfo("Segment Duplicate Check","Duplicated SEG_ID "
                                                  "(Gd to go if no duplicated SEG_ID) = "+ str(Duplicated_SEG))
tkinter.messagebox.showinfo("Segment Duplicate Check","Duplicated BEND_ID "
                                                  "(Gd to go if no duplicated SEG_ID) = "+ str(Duplicated_BEND))


# Segment LIST
for insert in msp.query('INSERT'):

            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("SEG_ID" in s for s in List):### Filter applied to search NSR blocks only ###
                print(List)

                SEG_ID = List[0][1]
                Width_Depth = List[1][1]
                Lining = List[4][1]
                Remark = List[5][1]
                Length = List[6][1]
                print(Length)

                Precedent_Seg = List[7][1]


                while Length == '##################': ## error message for corrupted SEG block
                    tkinter.messagebox.showinfo("Error","SEG block corrupted, rebuild ""Length"" attribute")
                    break

                    exit

                ListFile.append(SEG_ID + "," + Width_Depth+ ","+ Length + ","  + Lining + "," + Precedent_Seg+ ","+ Remark)


# Bend LIST
for insert in msp.query('INSERT'):

            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("BEND_ID" in s for s in List):### Filter applied to search NSR blocks only ###
                print(List)

                BEND_ID = List[0][1]
                Width_Depth = List[1][1]
                Lining = List[3][1]
                Remark = List[4][1]
                Length = "-"
                Precedent_Seg = List[6][1]

                ListFile.append(BEND_ID + "," + Width_Depth + ","+ Length + ","+ Lining + "," + Precedent_Seg+ ","+ Remark)


with open('ListFile.Rec', 'w') as f:
    for item in ListFile:
        f.write("%s\n" % item)

f = asksaveasfile(mode='w', defaultextension=".txt",title='Save Duct Segment/ Bend Detail file as',initialfile="Segment info list.txt")
for item in ListFile:
    f.write("%s\n" % item)
f.close()