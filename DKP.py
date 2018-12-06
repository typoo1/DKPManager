import sqlite3
import names
import time
import datetime
import random

import tkinter as tk
import tkinter.constants
from tkinter import ttk
import tkinter.messagebox as tkm
import Pmw
from tkinter import *
from tkinter import simpledialog



root = tk.Tk()
connection = sqlite3.connect("DKP.db")
crsr = connection.cursor()
crsr.execute("PRAGMA foreign_keys = ON")
CharacterMode = False
ModeText = tk.StringVar()
cEntry = tk.IntVar()
item = tk.StringVar()
item.set("Bank")
itemList = {}

ModeText.set("Character Mode")

class RoleDialog:
    roleName = StringVar()
    multiplier = IntVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.addRole).pack(side="right")
        self.cancle = Button(top, text="Cancel")

        self.el1 = Label(top, text="Role Name:").pack(side="top")
        self.e1 = Entry(top, textvariable=self.roleName).pack(side="top")
        self.el2 = Label(top, text="Multiplier:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.multiplier).pack(side="top")

    def addRole(self):
        addRole(self.roleName.get(), self.multiplier.get())
        self.top.destroy()

class ItemDialog:

    itemName = StringVar()
    ilvl = IntVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.addItem).pack(side="right")
        self.cancle = Button(top, text="Cancel")

        self.el1 = Label(top, text="Item Description:").pack(side="top")
        self.e1 = Entry(top, textvariable=self.itemName).pack(side="top")
        self.el2 = Label(top, text="ilvl:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.ilvl).pack(side="top")

    def addItem(self):
        addItem(self.itemName.get(), self.ilvl.get())
        self.top.destroy()

class PlayerDialog:

    playerName = StringVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.addPlayer).pack(side="right")
        self.cancle = Button(top, text="Cancel")

        self.el1 = Label(top, text="Player's Name:").pack(side="top")
        self.e1 = Entry(top, textvariable=self.playerName).pack(side="top")

    def addPlayer(self):
        addPlayer(self.playerName.get())
        self.top.destroy()

class CharacterDialog:

    characterName = StringVar()
    playerID = IntVar()
    level = IntVar()
    class_ = StringVar()
    role = StringVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.addCharacter).pack(side="right")
        self.cancle = Button(top, text="Cancel")
        self.sPID = Button(top, command=self.searchPID, text="Search players").pack(side="bottom")
        self.sRole = Button(top, command=self.searchRole, text="Search Roles").pack(side="bottom")

        self.el1 = Label(top, text="Player ID (numeric):").pack(side="top")
        self.e1 = Entry(top, textvariable=self.playerID).pack(side="top")
        self.el2 = Label(top, text="Character Name:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.characterName).pack(side="top")
        self.el2 = Label(top, text="Level:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.level).pack(side="top")
        self.el2 = Label(top, text="Class:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.class_).pack(side="top")
        self.el2 = Label(top, text="Role:").pack(side="top")
        self.e2 = Entry(top, textvariable=self.role).pack(side="top")

    def addCharacter(self):
        addCharacter(self.class_.get(), self.level.get(), self.role.get(), self.characterName.get(),
                     self.playerID.get())
        self.top.destroy()

    def searchPID(self):
        query = simpledialog.askstring("Input", "What is the player's name?", parent=self.top)
        temp = crsr.execute("SELECT player_id FROM Player WHERE player_name=?", (query,)).fetchone()
        if temp is not None:
            self.playerID.set(temp[0])
        else:
            tkm.showwarning("No player found", "Player was not found, please add player first or try again")

    def searchRole(self):
        query = simpledialog.askstring("Input", "What role are you looking for?", parent=self.top)
        temp = crsr.execute("SELECT role FROM Role WHERE role=?", (query,)).fetchone()
        if temp is not None:
            self.role.set(temp[0])
        else:
            tkm.showwarning("No role found", "Role not found, please try again or add the role")

class RaidDialog:

    ammount = IntVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.distribute).grid(row=1, column=4)

        self.raidScrollBar = tk.Scrollbar(top, orient=tk.VERTICAL)
        self.raidlistBox = tk.Listbox(top, exportselection=0, selectmode="multiple", yscrollcommand=self.raidScrollBar.set)
        self.raidScrollBar.config(command=self.raidlistBox.yview)
        self.raidLabel = tk.Label(top, text="Select all participants:")
        self.raidLabel.grid(row=0, column=2)
        self.raidlistBox.grid(row=1, column=2)
        self.raidScrollBar.grid(row=1, column=3, sticky='ns')
        self.el1 = Label(top, text="Ammount to distribute:").grid(row=0, column=0, sticky='s')
        self.e1 = Entry(top, textvariable=self.ammount).grid(row=1, column=0, sticky='n')

        self.updateListbox()

    def updateListbox(self):
        characters=listCharacters()
        self.raidlistBox.delete(0, tk.END)
        for item in characters:
            self.raidlistBox.insert(tk.END, item)


    def distribute(self):
        orderedRoleList = list()
        orderedMultiList = list()
        orderedSellerList = list()
        for Id in self.raidlistBox.curselection():
            orderedSellerList.append(self.findPlayer(Id))
        for Id in self.raidlistBox.curselection():
            orderedRoleList.append(crsr.execute("SELECT role FROM Characters WHERE character_id=?",
                                                ((Id+1),)).fetchone()[0])
        for roles in orderedRoleList:
            orderedMultiList.append(crsr.execute("SELECT dkp_multi FROM Role WHERE role=?",
                                                ((roles),)).fetchone()[0])
        for i in range(len(orderedMultiList)):
            addTransaction(orderedSellerList[i], 1, (self.ammount.get()*orderedMultiList[i]), 1)

        tkm.showinfo("Transactions complete", "Successfully gave DKP to " + str(len(orderedMultiList)+ "Players."))
                         # ""Gave " + str(orderedSellerList[i]) + " " + str(self.ammount.get()*orderedMultiList[i]) + " DKP")

    def findPlayer(self, Charid):
        temp = crsr.execute("SELECT player_id FROM Characters WHERE character_id=?", (Charid+1,))
        return (temp.fetchone()[0])

class SearchDialog:

    fromDate = StringVar()
    toDate = StringVar()

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        self.ok = Button(top, text="OK", command=self.search).pack(side="right")
        self.cancle = Button(top, text="Cancel")

        self.el0 = Label(top, text="Search Transactions")
        self.el1 = Label(top, text="From Date(YYYYMMDD):").pack(side="top")
        self.e1 = Entry(top, textvariable=self.fromDate).pack(side="top")
        self.el1 = Label(top, text="To Date(YYYYMMDD):").pack(side="top")
        self.e1 = Entry(top, textvariable=self.toDate).pack(side="top")

    def search(self):
        fyear = self.fromDate.get()[0:4]
        fmon = self.fromDate.get()[4:6]
        fday = self.fromDate.get()[6:]
        fdate = fyear+"-"+fmon+"-"+fday+" 00:0000"

        tyear = self.toDate.get()[0:4]
        tmon = self.toDate.get()[4:6]
        tday = self.toDate.get()[6:]
        tdate = tyear + "-" + tmon + "-" + tday + " 00:0000"
        print(tdate)

        temp = crsr.execute("SELECT * FROM Transactions WHERE date >=? and date <=?",
                            (fdate,tdate))
        for item in temp:
            print("Transaction_id: " + str(item[0]))
            print("buyer_id: " + str(item[1]))
            print("seller_id: " + str(item[2]))
            print("cost: " + str(item[3]))
            print("datetime: " + str(item[4]))
            print("item_id: " + str(item[5]))
            print()

class Window(tk.Frame):

    # Initilizes the window.
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.getItemList()

        menuBar = tk.Menu(root)
        addMenu = tk.Menu(menuBar, tearoff=0)
        addMenu.add_command(label="Role", command=self.addRole)
        addMenu.add_command(label="Item", command=self.addItem)
        addMenu.add_command(label="Player", command=self.addPlayer)
        addMenu.add_command(label="Character", command=self.addCharacter)
        menuBar.add_cascade(label="Add", menu=addMenu)
        menuBar.add_command(label="Raid", command=self.raid)
        menuBar.add_command(label="Search", command=self.search)
        root.config(menu=menuBar)

        self.frame = ttk.Frame(self.master).grid(row=0, column=0)


        self.testButton = tk.Button(self.frame, command=self.listPrint, text="Test").grid(row=1, column=0)
        self.characterButton = tk.Button(self.frame, command=self.switchmode, textvariable=ModeText).grid(row=2,
                                                                                                          column=0)
        self.TransactButton = tk.Button(self.frame, command=self.transact, text="Transact").grid(row=1, column=0)
        self.costLabel = tk.Label(self.frame, text="Cost of item").grid(row=1, column=1, sticky='s')
        self.costEntry = tk.Entry(self.frame, textvariable=cEntry).grid(row=2, column=1)
        self.inspectBuyer = Button(self.frame, command=self.inspectB, text="Buyer's balance").grid(row=3,column=0)
        self.inspectSeller = Button(self.frame, command=self.inspectS, text="Seller's's balance").grid(row=3, column=1)


        self.buyLabel = tk.Label(self.frame, text="Buyer")
        self.buyLabel.grid(row=0, column=4)
        self.buyScrollBar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.buylistBox = tk.Listbox(self.frame, exportselection=0, yscrollcommand=self.buyScrollBar.set)
        self.buyScrollBar.config(command=self.buylistBox.yview)
        self.buylistBox.grid(row=1, column=4, rowspan=3)
        self.buyScrollBar.grid(row=1, column=5, rowspan=3, sticky='ns')

        self.sellScrollBar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.selllistBox = tk.Listbox(self.frame, exportselection=0, yscrollcommand=self.sellScrollBar.set)
        self.sellScrollBar.config(command=self.selllistBox.yview)
        self.sellLabel = tk.Label(self.frame, text="Seller")
        self.sellLabel.grid(row=0, column=6)
        self.selllistBox.grid(row=1, column=6, rowspan=3)
        self.sellScrollBar.grid(row=1, column=7,rowspan=3, sticky='ns')

        self.itemlabel = tk.Label(self.frame, text="Item Selector:").grid(row=0, column=8, padx=5)
        self.itemDropDown = tk.OptionMenu(self.frame, item, *itemList).grid(row=1, column=8)
        # self.refresh = Button(self.frame, command=self.updateall).grid(row=2, column=8)
        self.updateListbox()

    # def updateall(self):
    #     self.updateListbox()
    #     self.updateItemList()
    #     for item in self.itemDropDown:
    #     menu = self.itemDropDown["menu"]
    #     menu.delete(0, END)
    #     for string in itemList:
    #         menu.add_command(label=string, command=lambda value=string: item.set(value))
    def inspectB(self):
        if(CharacterMode):
            buyer = findPlayer(self.buylistBox.get(self.buylistBox.curselection()))
            tkm.showinfo("Buyer's Balance", "The currently selected buyer has " + str(getBalance(buyer)) + " DKP")
        else:
            buyer = int(self.buylistBox.curselection()[0]) + 1
            tkm.showinfo("Buyer's Balance", "The currently selected buyer has " + str(getBalance(buyer)) + " DKP")

    def inspectS(self):
        if(CharacterMode):
            seller = findPlayer(self.selllistBox.get(self.selllistBox.curselection()))
            tkm.showinfo("Seller's Balance", "The currently selected seller has " + str(getBalance(seller)) + " DKP")
        else:
            seller = int(self.selllistBox.curselection()[0]) + 1
            tkm.showinfo("Seller's Balance", "The currently selected seller has " + str(getBalance(seller)) + " DKP")

    def getBuyer(self):
            return(self.buylistBox.get(self.buylistBox.curselection()))

    def getSeller(self):
        return(self.selllistBox.get(self.selllistBox.curselection()))

    def listPrint(self):
        selected = self.selllistBox.get(self.selllistBox.curselection())
        selected1 = self.buylistBox.get(self.buylistBox.curselection())
        print(selected)
        print(selected1)

    def updateListbox(self):
        players=listPlayers()
        self.buylistBox.delete(0, tk.END)
        self.selllistBox.delete(0, tk.END)
        for item in players:
            self.buylistBox.insert(tk.END, item)
            self.selllistBox.insert(tk.END, item)

    def updateListboxChar(self):
        characters=listCharacters()
        self.buylistBox.delete(0, tk.END)
        self.selllistBox.delete(0, tk.END)
        for item in characters:
            self.buylistBox.insert(tk.END, item)
            self.selllistBox.insert(tk.END, item)

    def switchmode(self):
        global CharacterMode
        if(CharacterMode):
            CharacterMode = False
            self.updateListbox()
            ModeText.set("Character Mode")
        else:
            CharacterMode = True
            self.updateListboxChar()
            ModeText.set("Player Mode")

    def transact(self):
        buyer = self.getBuyer()
        seller = self.getSeller()
        cost = cEntry.get()
        if(CharacterMode):
            addTransChar(seller, buyer, cost, self.getItemID(item.get()))
        else:
            addTransaction(self.selllistBox.curselection()[0]+1, self.buylistBox.curselection()[0]+1, cost,
                           self.getItemID(item.get()))

    def getItemList(self):
        global itemList
        temp = crsr.execute("SELECT description FROM Item")
        for row in temp:
            itemList[row[0]] = ""
        return itemList

    def updateItemList(self):
        global itemList
        itemList.clear()
        self.getItemList()
        root.update()

    def getItemID(self, itemDes):
        return(crsr.execute("SELECT item_id FROM Item WHERE description=?",(itemDes,)).fetchone()[0])

    def addRole(self):
        d = RoleDialog(root)
        root.wait_window(d.top)

    def addItem(self):
        d = ItemDialog(root)
        root.wait_window(d.top)
        # self.itemDropDown.children["menu"].delete(0, END)
        self.updateItemList()

    def addPlayer(self):
        d = PlayerDialog(root)
        root.wait_window(d.top)
        if(CharacterMode):
            self.updateListboxChar()
        else:
            self.updateListbox()

    def addCharacter(self):
        d = CharacterDialog(root)
        root.wait_window(d.top)
        if (CharacterMode):
            self.updateListboxChar()
        else:
            self.updateListbox()

    def raid(self):
        d = RaidDialog(root)
        root.wait_window(d.top)

    def search(self):
        d = SearchDialog(root)
        root.wait_window(d.top)

def addRole(rolename, multiplier):
    crsr.execute("INSERT INTO Role(role, dkp_multi) VALUES(?, ?)", (rolename, multiplier))
    connection.commit()
    
def addCharacter(class_, level, role, charactername, player_ID):
    crsr.execute("INSERT INTO Characters(class, level, role, character_name, player_id) VALUES(?, ?, ?, ?, ?)",
        (class_, level, role, charactername, player_ID))
    connection.commit()

def addItem(description, ilvl):
    crsr.execute("INSERT INTO Item(description, ilevel) VALUES(?, ?)", (description, ilvl))
    connection.commit()
    
def addPlayer(playername):
    crsr.execute("INSERT INTO Player(DKP, player_name) VALUES(0, ?)", (playername,))
    connection.commit()

def displayPlayers():
    cursor = crsr.execute("SELECT player_id, DKP, player_name FROM Player")
    for row in cursor:
        print("Player_ID= " + str(row[0]))
        print("DKP= " + str(row[1]))
        print("player_name= " + str(row[2]))
        print()

def displayRoles():
    cursor = crsr.execute("SELECT role, dkp_multi FROM Role")
    for row in cursor:
        print("Role= " + str(row[0]))
        print("DKP_Multi= " + str(row[1]))
        print()

def displayCharacters():
    cursor = crsr.execute("SELECT character_id, class, level, role, character_name, player_id FROM Characters")
    for row in cursor:
        print("characterid= " + str(row[0]))
        print("class= " + str(row[1]))
        print("level= " + str(row[2]))
        print("role " + str(row[3]))
        print("character Name= " + str(row[4]))
        print("Player= " + str(row[5]))
        print()

def populateRoles():
    addRole("Healer", 1)
    addRole("DPS", 1)
    addRole("Tank", 1)
    addRole("Test", 100)
    
def populatePlayers():
    for i in range(50):
        name = names.get_full_name()
        val= random.randrange(0, 10000)
        sql_command = "INSERT INTO Player(character_id, DKP, player_name) VALUES(?, ?, ?)"
        crsr.execute(sql_command, (i, val, name))
    connection.commit()

def giveDKP(PlayerID, ammount):
    crsr.execute("UPDATE Player set DKP = (DKP + ?) where player_id = ?", (ammount, PlayerID))

def takeDKP(PlayerID, ammount):
    current = crsr.execute("SELECT DKP FROM Player WHERE player_id=?", (PlayerID,))
    if (current.fetchone()[0] >= ammount):
        crsr.execute("UPDATE Player set DKP = (DKP - ?) WHERE player_id=?", (ammount, PlayerID))

def addTransaction(Seller, cost):
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    crsr.execute("INSERT INTO Transactions(buyer_id, seller_id, cost, date, item_id) VALUES(1, ?, ?, ?, 1)",
                 (Seller, cost, date))
    giveDKP(Seller, cost)
    takeDKP(1, cost)
    connection.commit()
    
def getBalance(PlayerID):
    current = crsr.execute("SELECT DKP FROM Player WHERE player_id=?", (PlayerID,)).fetchone()
    return(current[0])

def getBalanceChar(CharacterName):
    PlayerID = findPlayer(CharacterName)
    current = crsr.execute("SELECT DKP FROM Player WHERE player_id=PlayerID")
    return(Current.fetchone()[0])

def addTransaction(Seller, Buyer, Cost, Item_id):
    if(getBalance(Buyer) >= Cost):
        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S"))
        crsr.execute("INSERT INTO Transactions(buyer_id, seller_id, cost, date, item_id) VALUES(?, ?, ?, ?, ?)",
                     (Buyer, Seller, Cost, date, Item_id))
        giveDKP(Seller, Cost)
        takeDKP(Buyer, Cost)
        connection.commit()
    else:
        tkm.showwarning("Error", "Buyer doesn't have enough DKP for transaction")
        return()
        
def findPlayer(Charname):
    temp = crsr.execute("SELECT player_id FROM Characters WHERE character_name=?", (Charname,))
    return(temp.fetchone()[0])

def addTransChar(Sellerc, Buyerc, Cost, Item_id):
    Seller = findPlayer(Sellerc)
    Buyer = findPlayer(Buyerc)
    addTransaction(Seller, Buyer, Cost, Item_id)

def listPlayers():
    temp= crsr.execute("SELECT player_name FROM Player")
    items = list()
    for item in temp:
        items.append(str(item[0]))
    return items

def listCharacters():
    temp= crsr.execute("SELECT character_name FROM Characters")
    items = list()
    for item in temp:
        items.append(str(item[0]))
    return items

def getName(id):
    return(crsr.execute("SELECT player_name FROM Player WHERE player_id=?", (id,)).fetchone()[0])

# displayRoles()
# addPlayer("Tester")
# addCharacter("Paladin", 50, "Healer", "Testeee", 1)
# displayPlayers()
# displayCharacters()
# giveDKP(1, 100000000)
# addTransChar("Strongface", "Testee", 1000, 2)

Win = Window(master=root)
root.mainloop()

connection.commit()

connection.close()