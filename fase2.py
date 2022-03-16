# -*- coding: utf-8 -*-


from binarysearchtree import BinarySearchTree
from binarytree import BinaryTree
from binarytree import Node

import csv  # read files csv, tsv
import os.path  # to work with files and directory https://docs.python.org/3/library/os.path.html
# import queue    package implementes a queueu, https://docs.python.org/3/library/queue.html
import re  # working with regular expressions
import datetime

class BinaryQueue(BinaryTree): # This class will simulate a Queue using only the BinaryTree class, by always branching to the left (resulting in a list)
    def __init__(self, lastelem=None): # Initialize a queue with the constructor of BinaryTree, adding a reference to the last element
        #super(BinaryTree, self).__init__()
        self._root=Node(lastelem)
        self.lastelem=self._root

    def enQueue(self, node):
        if self._root is None: # If the BinaryQueue is empty, we insert it at the root
            self._root=Node(node, parent=None)
            self.lastelem=self._root
        else:
            self.lastelem.left = Node(node, parent=self.lastelem) # If it is not empty, enqueue the element (linking it to the last element)
            self.lastelem = self.lastelem.left # Update the reference to last element

    def deQueue(self):

        if self._root is None: #If the list is empty, return None
            return None

        aux = self._root.elem # Save content of the root on auxiliar variable
        if self._root.left is None: # If it is the only element of the list, update the root to None
            self._root=None
            return aux
        if self._root.left is not None: # If it there are more elements, advance the reference of the root
            self._root=self._root.left
            return aux

def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{2}:\d{2}')  # busca la palabra foo

    if pattern.match(time):
        data = time.split(':')
        hour = int(data[0])
        minute = int(data[1])
        if hour in range(8, 20) and minute in range(0, 60, 5):
            return True

    return False


def changeTime(time, key='prev'):
    times = time.split(':')
    hour = int(times[0])
    minutes = int(times[1])
    if (key != 'prev' and key != 'next'):
        {
            print('error on the key argument')
        }
    if (key == 'prev'):
        minutes = (minutes-5) % 60
        if (minutes == 55):
            hour = (hour-1) % 24
    if (key == 'next'):
        minutes = (minutes+5) % 60
        if (minutes == 0):
            hour = (hour+1) % 24
    hour_res = str(hour)
    minutes_res = str(minutes)
    if (hour < 10):
        hour_res = "0"+hour_res
    if (minutes < 10):
        minutes_res = "0"+minutes_res
    return hour_res+":"+minutes_res


# number of all possible appointments for one day
NUM_APPOINTMENTS = 144


class Patient:
    """Class to represent a Patient"""

    def __init__(self, name, year, covid, vaccine, appointment=None):

        self.name = name
        self.year = year
        self.covid = covid
        self.vaccine = vaccine
        self.appointment = appointment  # string with format hour:minute

    def setAppointment(self, time):
        """gets a string with format hour:minute"""
        self.appointment = time

    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self, other):
        return other != None and self.name == other.name


class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""

    def __init__(self, filetsv=None, orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        # Call to the constructor of the super class, BinarySearchTree.
        # This constructor only define the root to None
        super(HealthCenter2, self).__init__()

        # Now we
        if filetsv is None or not os.path.isfile(filetsv):
            # If the file does not exist, we create an empty tree (health center without patients)
            self.name = ''
            #print('File does not exist ',filetsv)
        else:
            order = 'by appointment'
            if orderByName:
                order = 'by name'

            #print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))

            self.name = filetsv[filetsv.rindex('/')+1:].replace('.tsv', '')
            #print('The name of the health center is {}\n\n'.format(self.name))
            # self.name='LosFrailes'

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")

            for row in lines:
                # print(row)
                name = row[0]  # nombre
                year = int(row[1])  # año nacimiento
                covid = False
                if int(row[2]) == 1:  # covid:0 o 1
                    covid = True
                vaccine = int(row[3])  # número de dosis
                try:
                    appointment = row[4]
                    if checkFormatHour(appointment) == False:
                        #print(appointment, ' is not a right time (hh:minute)')
                        appointment = None

                except:
                    appointment = None

                objPatient = Patient(name, year, covid, vaccine, appointment)
                # name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name, objPatient)
                else:
                    if appointment:
                        self.insert(appointment, objPatient)
                    else:
                        print(
                            objPatient, " was not added because appointment was not valid!!!")

            fichero.close()

    def searchPatients(self, year=2021, covid=None, vaccine=None):  # O(n log(n))
        """return a new object of type HealthCenter 2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree."""
        
        result = HealthCenter2()
        q = BinaryQueue(self._root)  # Queue implementation using binary tree (using always the left child)
        currentself = self._root 

        while q._root:  # O(n). Traverse the tree-list in level order
            currentself=q.deQueue()
            # If the current patient meets the requirements, insert it to the HC2 (inserting has a cost of O(logn))
            if currentself.elem.year <= year and (currentself.elem.covid == covid or covid is None) and (currentself.elem.vaccine == vaccine or vaccine is None):
                result.insert(currentself.elem.name, currentself.elem)

            if currentself.left is not None:
                q.enQueue(currentself.left)

            if currentself.right is not None:
                q.enQueue(currentself.right)
        # Therefore, the method will have a cost of O (nlogn)
        # In the worst case (self is a degenerate tree), insertion has a cost of O(n) and the whole method would be O(n^2)
            
            
        return result

    def vaccine(self, name, vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False eoc"""
        patient = self.find(name)
        if (checkFormatHour(self._root.key)): # First we check if the time given is correct
            print(
                "This HC is ordered by appointment. This function only works with HC's ordered by name")
            return False
        if (patient is None): # Check if patient exists
            print("Patient does not exist")
            return False
        if (patient.elem.vaccine == 2): # If patient has already been fullly vaccinated, remove it and add it to vaccinated
            print("The patient has been already fully vaccinated")
            self.remove(patient.elem.name)
            vaccinated.insert(patient.elem.name, patient.elem)
            return False
        elif (patient.elem.vaccine == 0 or patient.elem.vaccine == 1):  
            self.remove(patient.elem.name)                          # If not, remove it from self,
            patient.elem.vaccine += 1                               # increment the vaccine and:
            if (patient.elem.vaccine == 1):                         #if the patient is not fully vaccinated, insert it again in self 
                self.insert(patient.elem.name, patient.elem)
            elif (patient.elem.vaccine == 2):
                vaccinated.insert(patient.elem.name, patient.elem)  #if he/she is fully vaccinated, insert it in vaccinated HC2
            return True
        # The complexity of the method is O (logn), as we only use functions insert and remove without loops. 
        # The worst case would be that both self and vaccinated were degenerate trees and that the patients were at the end of the tree. 
        # In that case, the global cost would be: 1 removal (n) + 2 insertions (2n) = 3n
        return None

    def makeAppointment(self, name, time, schedule):
        """This functions makes an appointment 
        for the patient whose name is name. It functions returns True is the appointment 
        is created and False eoc """
        if (checkFormatHour(time) is False):  # check that the time format is correct
            print("Time format is incorrect")
            return False
        # check that the patient exists in the invoking center
        patient = self.find(name)
        if (patient is None):
            print('The patient does not exist in the invoking Health Center')
            return False
        if (schedule.search(time) is False):  # if the time given is available, assign it
            patient.elem.setAppointment(time)
            schedule.insert(time, patient.elem)
            return True
        # if there are no time slots available, we return False
        if (schedule.size() == NUM_APPOINTMENTS):
            print("All slots are occuppied")
            return False
        if (patient.elem.vaccine == 2):  # if the patient is already vaccinated, return False
            print("Patient is already vaccinated")
            return False
        else:  # if there is at least one time slot available
            # using our changeTime function, initialize two variables with the time 5 minutes before/after respectively
            prevtime = changeTime(time, "prev")
            nexttime = changeTime(time, "next")
            while (1):  # we iterate until we find the time slot available (at most 143 iterations in the worst case: given time is the 08:00 and the only available is 19:55, or the other way around)
                # if prevtime is free and is in the correct hour range, we insert it
                if (schedule.search(prevtime) is False and checkFormatHour(prevtime)):
                    patient.elem.setAppointment(prevtime)
                    schedule.insert(prevtime, patient.elem)
                    return True
                # if nexttime is free and is in the correct hour range, we insert it
                elif (schedule.search(nexttime) is False and checkFormatHour(nexttime)):
                    patient.elem.setAppointment(nexttime)
                    schedule.insert(nexttime, patient.elem)
                    return True
                else:  # else, we have to substract 5 minutes to prevtime, and add 5 to nexttime
                    prevtime = changeTime(prevtime, "prev")
                    nexttime = changeTime(nexttime, "next")
            # Therefore, the complexity will be in the worst case:
            # 246*logn+n=O(n) in the worst case (143 iterations + 1 call of the insert function + 246 of the search function).
            # The insert function is O (n) if the tree is degenerate (a list), and search is O(logn).
            # So, overall, the complexity is O (logn)


if __name__ == '__main__':
    print('\n\ttest8_searchPatients: 0 dosages')

    oInput = HealthCenter2('data/LosFrailes2.tsv')
    print('Input:')
    oInput.draw(False)

    expected = HealthCenter2('data/LosFrailes2-0.tsv')
    print('Expected:')
    expected.draw(False)

    result = oInput.searchPatients(2021, None, 0)
    print('Result:')
    result.draw(False)