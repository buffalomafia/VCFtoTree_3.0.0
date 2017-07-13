from Tkinter import *
import os
import sys
import subprocess
import threading


#This Class is responsible for keeping track of all the frame layouts
class Frames:

    #These variables will be passed to the shell script
    selectedSpecies = []
    speciesList2 = []
    customOutputs = ["", "", "", "", ""]
    chromosomeOutputs = ["", "", ""]
    populationList = []



    def __init__(self, master):

        #Frames to be displayed in the main window
        self.speciesSelection = Frame(master)
        self.specFrame = Frame(master)
        self.customFrame = Frame(master)
        self.populationSelection = Frame(master)
        self.confPage = Frame(master)
        self.buildPage = Frame(master)

        #TODO: Implemnt this
        self.previousFrame = None
        self.currentFrame = None

        #This is for distinguishing between both and custom
        self.bothHuman = 0

        #If otherSpecies was selected
        self.otherSpecies = 0

        #For checkbox values
        self._raxML = 0
        self._FastTree = 0




        '''
        ----------------------------------------------------------------------------------------------------------------
        OPENING SCREEN
        ----------------------------------------------------------------------------------------------------------------
        '''
        # Description: If the "human" button is clicked, begin() is called and the program executes like it originally did
        # If the user selects the "other" button, then alternateBegin() is called, defined below

        #Buttons and Labels
        self.mainLabel = Label(master, text="VCF to Tree\n", font=('Times', 30), fg="brown")
        self.lineLabel = Label(master, text="-----------------------------------------------\n", font=('Times', 20), fg='brown')
        self.questionLabel = Label(master, text="Are you comparing humans, \n or another species?", font=('Times', 20), fg='brown')
        self.humanButton = Button(master, text="Human", font=('Times', 15), fg='brown', command= lambda: openingScreenNext(self, "Human"), bg='papaya whip')
        self.otherButton = Button(master, text="Other", font=('Times', 15), fg='brown', command= lambda: openingScreenNext(self, "Other"), bg='papaya whip')

        # Places buttons and label
        self.mainLabel.place(relx=0.5, rely=.2, anchor=CENTER)
        self.lineLabel.place(relx=.5, rely=.25, anchor=CENTER)
        self.questionLabel.place(relx=.5, rely=.3, anchor=CENTER)
        self.humanButton.place(relx=.5, rely=.5, anchor=CENTER)
        self.otherButton.place(relx=.5, rely=.6, anchor=CENTER)




        '''
        ----------------------------------------------------------------------------------------------------------------
        SPECIES SELECTION
        ----------------------------------------------------------------------------------------------------------------
        '''

        Label(self.speciesSelection, text="\n\n\nPlease select the species you \n would like to compare  \n",font=('Times', 20), fg='brown').pack(side=TOP)
        self.DropDown = Listbox(self.speciesSelection, height=10, width=25, selectmode=MULTIPLE, font=('Times', 15),activestyle='none')
        self.DropDown.pack(side=TOP)
        self.DropDown.yview()

        self.DropDown.insert(1, 'Human (1000 Genome)')
        self.DropDown.insert(2, 'Human (Custom)')
        self.DropDown.insert(3, 'Neanderthal')
        self.DropDown.insert(4, 'Vindija')
        self.DropDown.insert(5, 'Denisova')
        self.DropDown.insert(6, 'Chimp')
        self.DropDown.insert(7, 'Rhesus-macaque')

        self.Next = Button(self.speciesSelection, text="Next", font=('Times', 12), fg='brown',command= lambda: speciesSelectionNext(self),borderwidth=4)
        self.Next.pack(side=RIGHT, pady=45)



        '''
        ----------------------------------------------------------------------------------------------------------------
        POPULATION SELECTION
        ----------------------------------------------------------------------------------------------------------------
        '''

        Label(self.populationSelection, text="\n\n\nPlease select the populations you \n would like to compare  \n", font=('Times', 20), fg='brown').pack(side=TOP)

        self.DropDown2 = Listbox(self.populationSelection, height=5, width=25, selectmode=MULTIPLE, font=('Times', 15), activestyle='none')
        self.DropDown2.pack(side=TOP)
        self.DropDown2.yview()

        self.DropDown2.insert(1, 'ALL')
        self.DropDown2.insert(2, 'ACB')
        self.DropDown2.insert(3, 'CHS')
        self.DropDown2.insert(4, 'GIH')
        self.DropDown2.insert(5, 'LWK')
        self.DropDown2.insert(6, 'ASW')
        self.DropDown2.insert(7, 'CLM')
        self.DropDown2.insert(8, 'GWD')
        self.DropDown2.insert(9, 'MSL')
        self.DropDown2.insert(10, 'PUR')
        self.DropDown2.insert(11, 'BEB')
        self.DropDown2.insert(12, 'MXL')
        self.DropDown2.insert(13, 'STU')
        self.DropDown2.insert(14, 'CDX')
        self.DropDown2.insert(15, 'ESN')
        self.DropDown2.insert(16, 'ITU')
        self.DropDown2.insert(17, 'TSI')
        self.DropDown2.insert(18, 'CEU')
        self.DropDown2.insert(19, 'FIN')
        self.DropDown2.insert(20, 'JPT')
        self.DropDown2.insert(21, 'PEL')
        self.DropDown2.insert(22, 'YRI')
        self.DropDown2.insert(23, 'CHB')
        self.DropDown2.insert(24, 'GBR')
        self.DropDown2.insert(25, 'KHV')
        self.DropDown2.insert(26, 'PJL')
        self.DropDown2.insert(27, 'IBS')

        self.Next = Button(self.populationSelection, text="Next", font=('Times', 12), fg='brown', command= lambda: populationSelectionNext(self), borderwidth=4)
        self.Previous = Button(self.populationSelection, text="Back", font=('Times', 12), fg='brown', command=lambda : previousFrame(self), borderwidth=4)
        self.Next.pack(side=RIGHT, pady=45, padx=100)
        self.Previous.pack(side=LEFT, pady=45, padx=100)



        '''
        ----------------------------------------------------------------------------------------------------------------
        Custom Species/ Custom Human
        ----------------------------------------------------------------------------------------------------------------
        '''

        # Other Species Frame

        # Variables for URL, vcf file name, and number of species
        self.URL = StringVar()
        self.vcfFileN = StringVar()
        self.numSpecie = StringVar()

        # Labels and Entry Boxes
        Label(self.customFrame, text="\n\nPlease provide the url to the chromosome file you'd like to use.",font=('Times', 15), fg='brown').pack(side=TOP)
        Label(self.customFrame, text="e.x. http://hgdownload.soe.ucsc.edu/goldenPath/equCab2/chromosomes/chr3.fa.gz",font=('Times', 11), fg='brown').pack(side=TOP)
        self.chromosomeURL = Entry(self.customFrame, textvariable=self.URL)
        self.chromosomeURL.pack(side=TOP, pady=10)

        Label(self.customFrame, text='\n\nPlease provide the vcf file name', font=('Times', 15), fg='brown').pack(side=TOP)
        self.vcfFile = Entry(self.customFrame, textvariable=self.vcfFileN)
        self.vcfFile.pack(side=TOP, pady=10)

        Label(self.customFrame, text="\n\nNumber of species ", font=('Times', 15), fg='brown').pack(side=TOP)
        Label(self.customFrame, text="( 0 if 'Human (Custom)' option not selected )", font=('Times', 11), fg='brown').pack(side=TOP)
        self.numSpecies = Entry(self.customFrame, textvariable=self.numSpecie)
        self.numSpecies.pack(side=TOP, pady=10)

        # TODO: Do we need a previous button for this page?

        # The lambda function is so that I can pass in the argument 'counter'
        self.Next = Button(self.customFrame, text="Next", font=('Times', 12), fg='brown', command=lambda: customFrameNext(self, self.bothHuman), borderwidth=4).pack(side=RIGHT, pady=45, padx=100)
        self.Back = Button(self.customFrame, text="Back", font=('Times', 12), fg='brown', command = lambda: previousFrame(self), borderwidth=4).pack(side=LEFT, pady=45, padx=100)


        '''
        ----------------------------------------------------------------------------------------------------------------
        SPEC FRAME
        ----------------------------------------------------------------------------------------------------------------
        '''

        # Variables for ch no and region
        self.c = StringVar()
        self.rS = StringVar()
        self.rE = StringVar()

        # Entry boxes for spec frame -----------------------------------------------------------------------------------

        Label(self.specFrame, text="\n Please select the chromosome and region \n to be analyzed: \n", font=('Times', 20),
              fg='brown').pack(side=TOP)

        Label(self.specFrame, text="\n Chromosome Number:", font=('Times', 15), fg='brown').pack(side=TOP)
        self.c_num = Entry(self.specFrame, textvariable=self.c)
        self.c_num.pack(side=TOP)

        Label(self.specFrame, text="\n Start of region:", font=('Times', 15), fg='brown').pack(side=TOP)
        self.r_Start = Entry(self.specFrame, textvariable=self.rS)
        self.r_Start.pack(side=TOP)

        Label(self.specFrame, text="\n End of region:", font=('Times', 15), fg='brown').pack(side=TOP)
        self.r_End = Entry(self.specFrame, textvariable=self.rE)
        self.r_End.pack(side=TOP)

        self.Next = Button(self.specFrame, text="Next", font=('Times', 12), fg='brown', command= lambda: specFrameNext(self), borderwidth=4)
        self.Previous = Button(self.specFrame, text="Back", font=('Times', 12), fg='brown', command= lambda: previousFrame(self),
                               borderwidth=4)

        self.Next.pack(side=RIGHT, pady=45, padx=100)
        self.Previous.pack(side=LEFT, pady=45, padx=100)

        '''
        ----------------------------------------------------------------------------------------------------------------
        CONFIRMATION PAGE
        ----------------------------------------------------------------------------------------------------------------
        '''


        alignmentLabel = Label(self.confPage,
                               text="\n\nPlease select an option below if you'd like to \n build a tree with your alignment, otherwise, simply press continue\n\n\n\n\n",
                               font=('Times', 15), fg='brown').pack(side=TOP)
        self._raxML = IntVar()
        self._FastTree = IntVar()
        c = Checkbutton(self.confPage, text="Build Tree Using RaxML", variable=self._raxML)
        d = Checkbutton(self.confPage, text="Build Tree Using FastTree", variable=self._FastTree)
        confirm = Button(self.confPage, text="Build", font=('Times', 12), fg='brown',
                         command= lambda: buildTree(self), borderwidth=4)

        c.pack(side=TOP)
        d.pack(side=TOP)

        confirm.pack(side=TOP, pady = 30)






















        '''
        --------------------------------------------------------------------------------------------------------------------
        BUTTON FUNCTIONS
        --------------------------------------------------------------------------------------------------------------------
        '''

        #From openingScreen to Species Selection or custom Frame
        def openingScreenNext(self, humanOrOther):

            #This is a special case for the previousFrame() function
            self.previousFrame = "master"


            #Unpack main screen
            self.mainLabel.place_forget()
            self.lineLabel.place_forget()
            self.questionLabel.place_forget()
            self.humanButton.place_forget()
            self.otherButton.place_forget()

            #If Human selected open Species Selection
            if (humanOrOther == "Human"):
                self.currentFrame = self.speciesSelection
                self.currentFrame.pack()

            # If other selected open customFrame
            elif (humanOrOther == "Other"):
                self.currentFrame = self.customFrame
                self.currentFrame.pack()

        #---------------------------------------------------------------------------------------------------------------
        def populationSelectionNext(self):
            self.currentFrame = self.specFrame
            self.previousFrame = self.populationSelection

            print("Selected populations:")
            print(self.populationList)

            self.previousFrame.pack_forget()
            self.currentFrame.pack()


        # --------------------------------------------------------------------------------------------------------------
        #From species selection to populatin selection
        def speciesSelectionNext(self):

            #Get selections from drowpdown
            self.selectedSpecies = [self.DropDown.get(selected) for selected in self.DropDown.curselection()]
            print(self.selectedSpecies)

            #add selected species to speciesList2
            if len(self.selectedSpecies) > 0:
                self.speciesList2 = ','.join(self.selectedSpecies)

            else:
                self.DropDown.configure(bg='tomato')
                return

            print("Selected species:")
            print(self.speciesList2)
            #Both custom and 1000 genome selected so launch customFrame and populationSelection
            if "Human (1000 Genome)" in self.selectedSpecies and "Human (Custom)" in self.selectedSpecies:
                print("1000 Genome and custom")
                self.bothHuman = 1
                self.previousFrame = self.currentFrame
                self.currentFrame = self.customFrame

                self.previousFrame.pack_forget()
                self.currentFrame.pack()


            #Only custom human selected so only launch customFrame, then specFrame
            elif "Human (Custom)" in self.selectedSpecies:
                print("Only selected custom human")
                print("Launch custom Frame, then specFrame ")
                self.previousFrame = self.currentFrame
                self.currentFrame = self.customFrame

                self.previousFrame.pack_forget()
                self.currentFrame.pack()

            else:
                print("Only 1000 genome human")
                print("Launching population selection frame")
                self.previousFrame = self.currentFrame
                self.currentFrame = self.populationSelection

                self.previousFrame.pack_forget()
                self.currentFrame.pack()

            #No species selected, set red, don't continue to next frame


        #---------------------------------------------------------------------------------------------------------------

        #From custom frame to populationSelection or specFrame
        def customFrameNext(self, bothHuman):

            #Keep track of unfilled Fields
            redCount = 0

            if (len(self.URL.get())) == 0:
                print("Missing URL)")
                self.chromosomeURL.configure(bg='tomato')
                redCount = 1

            if (len(self.vcfFileN.get())) == 0:
                print("Missing vcf file name)")
                self.vcfFile.configure(bg='tomato')
                redCount = 1

            if (len(self.numSpecie.get())) == 0:
                print("Missing URL)")
                self.numSpecies.configure(bg='tomato')
                redCount = 1

            if redCount == 1:
                return

            # values stored
            self._URL = self.URL.get()
            self._vcfFileName = self.vcfFileN.get()
            self._numSpecies = int(self.numSpecie.get())

            # Store the values so that hey can be used in the script
            self.customOutputs[0] = self._URL
            self.customOutputs[1] = self._vcfFileName
            self.customOutputs[2] = self._numSpecies

            print("Custom Values (not including rax and fastree) : ")
            print(self.customOutputs)

            #If 1000 Genome also selcted go to population selection
            if bothHuman == 1:
                print("Launching populationSelection")
                self.previousFrame = self.currentFrame
                self.currentFrame = self.populationSelection

                self.previousFrame.pack_forget()
                self.currentFrame.pack()

            #Otherwise go to specFrame
            elif bothHuman == 0:
                print("launching specFrame")
                self.previousFrame = self.currentFrame
                self.currentFrame = self.specFrame

                self.previousFrame.pack_forget()
                self.currentFrame.pack()

       #----------------------------------------------------------------------------------------------------------------

        #Go back
        def previousFrame(self):
            self.currentFrame.pack_forget()
            self.currentFrame = self.previousFrame
            self.previousFrame.pack()

       #----------------------------------------------------------------------------------------------------------------

        #Export populationList, then coninue to specFrame
        def populationSelectionNext(self):

            self.populationList = [self.DropDown2.get(selected2) for selected2 in self.DropDown2.curselection()]
            if len(self.populationList) > 0:
                self.populationList2 = ','.join(self.populationList)
                print("Population List: ")
                print(self.populationList)

                self.previousFrame = self.populationSelection
                self.currentFrame = self.specFrame

                self.previousFrame.pack_forget()
                self.currentFrame.pack()

            else:
                self.DropDown2.configure(bg='tomato')
                return


        def specFrameNext(self):
            try:

                cnum = int(self.c.get())
                rStart = int(self.rS.get())
                rEnd = int(self.rE.get())

                self.chromosomeOutputs[0] = (cnum)
                self.chromosomeOutputs[1] = (rStart)
                self.chromosomeOutputs[2] = (rEnd)

                # To produce only one set of widgets
                complex_indels = open('Code/complex_indelregions.txt', 'r')

                for indel in complex_indels:
                    indel = indel.strip()

                    if indel.startswith('#'):
                        continue

                    fields = indel.split('\t')
                    indel_chr = int(fields[0][3:])
                    indel_start = int(fields[1])
                    indel_end = int(fields[2])

                    # print cnum, str(indel_chr)

                    if not cnum == indel_chr:
                        continue

                    else:

                        # print cnum, str(indel_chr), indel_start, int(rStart)
                        if indel_start >= int(rStart) and indel_start <= int(rEnd):
                            print cnum, str(indel_chr), indel_start, int(rStart), int(rEnd)
                            self.warningLabel1 = Label(self.confPage,
                                                       text="\n WARNING: Your selected region contains complex indels, \n this may effect the tree.",
                                                       font=('Times', 12), fg='red')
                            self.warningLabel1.pack(side=TOP)

                        # TYPO, here should be >=, I guess I did this wrong from the beginning.
                        elif indel_end >= int(rStart) and indel_end <= int(rEnd):
                            print cnum, str(indel_chr), indel_end, int(rStart), int(rEnd)
                            self.warningLabel2 = Label(self.confPage,
                                                       text="\n WARNING: Your selected region contains complex indels, \n this may effect the tree.",
                                                       font=('Times', 12), fg='red')
                            self.warningLabel2.pack(side=TOP)
            except:
                self.setRed(self.c, self.c_num)
                self.setRed(self.rS, self.r_Start)
                self.setRed(self.rE, self.r_End)
                return

            print("Chromosome Values: ")
            print(self.chromosomeOutputs)

            print("\nLaunching Confirmation Page")

            self.previousFrame = self.specFrame
            self.currentFrame = self.confPage

            self.previousFrame.pack_forget()
            self.currentFrame.pack()



        # Used to handle empty entry box instances
        # red if empty, reset to white if corrected
        def setRed(self, sVar, entryBox):
            try:
                int(sVar.get())

                if len(sVar.get()) == 0:
                    entryBox.configure(bg='tomato')

                else:
                    entryBox.configure(bg='white')

            except:
                entryBox.configure(bg='tomato')

        #---------------------------------------------------------------------------------------------------------------
        def buildTree(self):

            #Get checkbox values
            self.customOutputs[3] = self._raxML.get()
            self.customOutputs[4] = self._FastTree.get()

            print("\n\n------------------ Final Outputs ------------------------\n\n")

            print("Ref Address, VCF Address, #Species, RaxML, FastTree")
            print(self.customOutputs)

            print("\nChromosome Number, Start, End")
            print(self.chromosomeOutputs)

            print("\nSelected Species: ")
            print(self.speciesList2)

            print("\nPopulation List: ")
            print(self.populationList)

            print("\n---------------------------------------------------------\n\n")

            #If other species was selected
            if self.otherSpecies == 1:
                print("build tree for other species called")

                os.system('chmod +x Code/otheranimals.sh')
                os.system('Code/otheranimals.sh %s %s %s %s %s %s %s %s &' % (
                str(self.customOutputs[0]), str(self.customOutputs[1]), str(self.chromosomeOutputs[0]), str(self.chromosomeOutputs[1]),
                str(self.chromosomeOutputs[2]), str(self.customOutputs[2]), str(self.customOutputs[3]), str(self.customOutputs[4])))

                return

            #Normal Build Tree Function
            elif self.otherSpecies == 0:
                os.system('chmod +x Code/buildTree_1click_erica.sh')
                command = "Code/buildTree_1click_erica.sh %s %s %s %s %s" .format((self.chromosomeOutputs[0]), str(self.chromosomeOutputs[1]), str(self.chromosomeOutputs[2]), self.populationList,self.speciesList2, str(self.customOutputs[3]), str(self.customOutputs[4]))
                os.system(command)

                return

    #END CLASS DEFINITION


'''
------------------------------------------------------------------------------------------------------------------------
        Launch Application
------------------------------------------------------------------------------------------------------------------------
'''

root = Tk()
root.title("VCF to Tree")
root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)
Frames = Frames(root)
# mainloop() keeps the application running, without which it dissappears
root.mainloop()