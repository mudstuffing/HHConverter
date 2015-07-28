import os
import decimal
import urllib.parse
from urllib.parse import urlencode
import hashlib
import os.path, time
from urllib.request import urlopen

#from urllib.parse import urlparse
#import from urllib.request import urlopen
#import urllib.request.


class tableObject():

	def __init__(self, dest_folder, dest_file, e):
		self.dest_folder = dest_folder
		if not os.path.exists(dest_folder):
			os.makedirs(dest_folder)
		self.dest_file = dest_folder + dest_file
		print (self.dest_file)
		print (self.dest_folder)
		self.TOURNEYID = 0
		self.players = {}
		self.pot = 0;
		self.board = ""
		self.old_holecards = ""
		self.oldformat = False
		self.numLines = 0
		self.handtype = ""
		self.street = ""
		self.pot = 0
		self.spot1 = 0
		self.spot2 = 0
		self.spot3 = 0
		self.showdown = False
		self.BUTTON = ""
		self.rake = 0
		self.totalpot = 0
		self.pot = 0
		self.board = ""
		self.playerstatus = {}
		self.playerwon = {}
		self.playershowed = {}
		self.HANDID = 0
		self.GAMETYPE = ""
		self.BUYIN = ""
		self.ANTE = 0
		self.YEAR = 0
		self.MONTH = 0
		self.DAY = 0
		self.TIME = 0
		self.BUTTON = ""
		self.street = ""
		self.SummaryPath = ""
		self.firstHand = False
		self.sidePotMode = False
		self.winnerfound = False
		self.safetycount = 0
		self.safeNewHand = False
		self.exchangeRate = float(e)
		#yo! there is no way to get a summary of a tournament from a SealsWithClubs tounrnament HH
		#So we need to query BitcoinPokerBlog for it. 
		#I'm not gonna let just anyone rape my data... so we are gonna send an api key
		self.api_key = "EDF8dN7ZKmZfQIj25LMahf8WAljnCvRAx2XG0lfBw9R+sWqWwKOfmSz8nHHvyZ/fDq16ox7rHaLn9DHyVL+1FETqLH9z57G4xP8iegtClFGnuaKHsAdFOsv7zGhqQcXf2m1xVhlUAfOVEL+mdBwfVupXhrdnSwuIY0NVS8nTnnLEGPteCmwvgLeZ05QOr+WeHuypVvPs8ifxgQMkihkErXzWMLch9pAJQsLNwIks76zjccdMfaca8Mc+N6qMgcsz7GWn9SH1ZpNvB+j8GbKX7tv8NZOfh4NIvnJ9tchYMCyE1lpkTCCOSGITeyF0D+cCvnKe5AgwCbOQ501c7bHvrw=="
		myfile = open(self.dest_file, "a+")
		myfile.write("Exchange rate is... " + str(self.exchangeRate) + "\n\n\n")
		myfile.close()
		
		
	def initTable(self):
		#reset all the variables
		x=2

	def round(self, dec, places, rounding=decimal.ROUND_HALF_UP):
		return dec.quantize(decimal.Decimal(str(10**-places)), rounding)

	def convertChips(self, a, ht):
		c = float(a)
		#c = decimal.Decimal(a)
		r = c
		if ht == "cash":
			c = self.round(decimal.Decimal((c/1000)*self.exchangeRate), 2) 
			r = "$" + str(c)
		#print ("\nConverting Chips: $handtype $c = $r\n");
		return r

	def doSidePot(self, hh):
		spNEWHH = ""
		try:
			if(self.winnerfound == False):
				self.safetycount = self.safetycount + 1
				if (hh.find("wins Side Pot 1") > -1): 
					p = hh.split(" ") 
					amt = p[5][1:-1]
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.spot1 = decimal.Decimal(self.spot1) + decimal.Decimal(amt)
					hh = hh.replace(" wins Side Pot 1 ", " wins the side pot ") #str_replace(" wins Side Pot 1 ", " wins the side pot ", $HH[$i]);
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")") #$HH[$i] = str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH + hh + "\n"
				elif (hh.find("splits Side Pot 1") > -1): #strpos($HH[$i], "splits Side Pot 1") > -1 ){
					p = hh.split(" ")
					amt = amt = p[5][1:-1]
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.spot1 = decimal.Decimal(self.spot1) + decimal.Decimal(amt)
					hh = hh.replace(" splits Side Pot 1 ", " ties for the side pot ") #str_replace(" splits Side Pot 1 ", " ties for the side pot ", $HH[$i]);
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")") #str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH +  hh + "\n"
				elif (hh.find("wins Side Pot 2") > -1): #strpos($HH[$i], "wins Side Pot 1") > -1 ){
					p = hh.split(" ") #explode(" ", $HH[$i]);
					amt = amt = p[5][1:-1]  #p[5]substr($p[5], 1, strlen($p[5]) - 2);
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.spot2 = decimal.Decimal(self.spot2) + decimal.Decimal(amt)
					hh = hh.replace(" wins Side Pot 2 ", " wins the side pot ") #str_replace(" wins Side Pot 1 ", " wins the side pot ", $HH[$i]);
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")") #$HH[$i] = str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH + hh + "\n"
				elif (hh.find("wins Side Pot 3") > -1): #strpos($HH[$i], "wins Side Pot 1") > -1 ){
					p = hh.split(" ") #explode(" ", $HH[$i]);
					amt = amt = p[5][1:-1]  #p[5]substr($p[5], 1, strlen($p[5]) - 2);
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.spot3 = decimal.Decimal(self.spot3) + decimal.Decimal(amt)
					hh = hh.replace(" wins Side Pot 3 ", " wins the side pot ") #str_replace(" wins Side Pot 1 ", " wins the side pot ", $HH[$i]);
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")") #$HH[$i] = str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH + hh + "\n"
				elif (hh.find("wins Main Pot") > -1):   #(strpos($HH[$i], "wins Main Pot") > -1 ){
					self.winnerfound = True;
					self.sidePotMode = False;
					p = hh.split(" ")
					amt = amt = p[4][1:-1]
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.pot = amt
					hh = hh.replace(" wins Main Pot ", " wins the main pot ") #str_replace(" wins Main Pot ", " wins the main pot ", $HH[$i]);
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")")   #str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH + hh + "\n"
				elif (hh.find("splits Main Pot") > -1):   #else if (strpos($HH[$i], "splits Main Pot") > -1 ){
					p = hh.split(" ")
					amt = amt = p[4][1:-1]
					self.playerwon[p[0].strip()] = decimal.Decimal(self.playerwon[p[0].strip()]) + decimal.Decimal(amt)
					self.pot = self.pot + amt
					hh = hh.replace(" wins Main Pot ", " ties for the main pot ") #spNEWHH = spNEWHH . str_replace(" wins Main Pot ", " ties for the main pot ", $HH[$i]) . "\r\n";
					hh = hh.replace("(" + amt + ")", "(" + str(self.convertChips(amt, self.handtype)) + ")")  #str_replace("($amt)", "(" . convertChips($amt, $handtype) . ")", $HH[$i]);
					spNEWHH = spNEWHH +  hh + "\n"
				elif (hh.find("Hand #") > -1):   #(strpos($HH[$i], "Hand #") > -1 ){
					self.winnerfound = True
					self.sidePotMode = False
					############################################1
					#DO SOMETHING #####################
					#######################################
				elif (hh.find("** Main Pot ") > -1):   #else if (strpos($HH[$i], "** Main Pot ") > -1 ){
					x=1
				elif (hh.find("** Side Pot") > -1):   #else if (strpos($HH[$i], "** Side Pot") > -1 ){
					x=1
				elif (hh.find(" shows ") > -1):   #else if (strpos($HH[$i], " shows ") > -1 ){
					p = hh.split(" ")
					self.playershowed[p[0].strip()] = p[2] + " " + p[3]
					spNEWHH = spNEWHH + hh + "\n"
				elif (hh.strip() == ""):	
					s = 1
				else:
					spNEWHH = spNEWHH + hh + "\n"
				if (self.safetycount>20):
					self.winnerfound = True
					self.sidePotMode = False
			for k in self.players.keys():
				if (str(self.playerwon[k]).isnumeric()):
					if (self.playerwon[k] == 0):
						self.playerstatus[k] = " showed " + self.playershowed[k] + " and lost "
					else:
						self.playerstatus[k] = " showed " + self.playershowed[k] + " and won (" + str(self.convertChips(self.playerwon[k], self.handtype)) + ") "
			#print(spNEWHH)
		except:
			print("Error occurred... prolly an incomplete hand.")
			self.firstHand = False
		return spNEWHH

	def processLine(self, HH):
		#print (HH)
		NEWHH = ""
		
		if (HH.find("Starting tournament") > -1):
			self.firstHand = True
			
		if (HH.find("Hand #") > -1):
			self.firstHand = True
			self.sidePotMode = False
		
		if (self.sidePotMode):
			HH = HH.replace("\r", "")
			HH = HH.replace("\n", "")
			#print (HH)
			NEWHH = self.doSidePot(HH)
		elif (self.firstHand):
			#l is the string o f the line
			#all the great conversion happens below...
			#print (self.convertChips(1345, "cash"))
			HH = HH.replace("\r", "")
			HH = HH.replace("\n", "")
			self.numLines = self.numLines + 1
			
			#if startign tournament....
			if (HH.find("Starting tournament") > -1):
				s = HH.split(" ")
				self.TOURNEYID = s[2]
				print(self.TOURNEYID)
			if (HH.find("Hand #") > -1):
				if (len(self.players) > 0):
					#try:
						#do the summary
						dollarsign = ""
						if (self.handtype == "cash"):
							dollarsign = "$"
							
						NEWHH = NEWHH + "*** SUMMARY ***\n"
						
						#do side pot 1
						if (self.spot1 > 0):
							totalpot = self.convertChips(decimal.Decimal(self.pot) + decimal.Decimal(self.spot1) + decimal.Decimal(self.spot2) + decimal.Decimal(self.spot3) + decimal.Decimal(self.rake), self.handtype)
							NEWHH = NEWHH + "Total pot " + dollarsign + str(totalpot) + " Main pot " + dollarsign + str(self.pot) + ". Side pot " + dollarsign + str(self.spot1) + ". "
							if (self.spot2 > 0):
								NEWHH = NEWHH + "Side pot " + dollarsign + str(self.spot2) + "."
							if (self.spot3 > 0):
								NEWHH = NEWHH + "Side pot " + dollarsign + str(self.spot3) + "."
							NEWHH = NEWHH + "| Rake " + dollarsign + str(self.rake) + "\n"
						else:
							if (str(self.pot).find("$") > -1):
								p = str(self.pot)
								r = str(self.rake)
								NEWHH = NEWHH + "Total pot " + dollarsign + str(decimal.Decimal(p[1:]) + decimal.Decimal(r[1:])) + " | Rake " + str(self.rake) + "\n"
							else:
								
								if str(self.rake) == "0" :
									r = "$0.00"
								else:
									r = str(self.rake)
								#print ("rake:" + r)
								#print ("ppot:" + str(self.pot))
								NEWHH = NEWHH + "Total pot " + dollarsign + str(decimal.Decimal(self.pot) + decimal.Decimal(r[1:])) + " | Rake " + str(self.rake) + "\n"
						
						if (self.board.strip() != ""):
							NEWHH = NEWHH + "Board: [" + self.board.strip() + "]\n"
						
						for k in self.players.keys():
							NEWHH = NEWHH + "Seat " + self.players[k] + ": " + k + " " + self.playerstatus[k] + "\n"
		
						NEWHH = NEWHH + "\n"
					#except:
						#print("Error occurred... prolly an incomplete hand.")
						#self.firstHand = False
										
				#now start the new hand and reset all info...
				s = HH.split(" ")
				self.HANDID = s[1].replace("#", "").replace("-", "")
				d = s[3].split("-") 
				self.YEAR = d[0];
				self.MONTH = d[1];
				self.DAY = d[2];
				self.TIME = s[4];
				self.players = {};
				self.pot = 0; 
				self.board = "";
				self.holecards = "";
				self.rake = 0;
				
			elif (HH.find("Game:") > -1):
				if (HH.find("NL Hold'em") > -1):    #strpos($HH[$i], "NL Hold'em") > -1){
					self.GAMETYPE = "No Limit Hold'em"
				else:
					self.GAMETYPE = "No Limit Hold'em"
				
				s = HH.split("(") #explode("(", $HH[$i]);
				d = s[1].split(")") #explode(")", $s[1]);
				if (d[0].find("+") > -1 ): # strpos($d[0], "+") > -1){
					s = d[0].split("+") #explode("+", $d[0]);
					s0 = decimal.Decimal(s[0])
					s1 = decimal.Decimal(s[1])
					self.BUYIN = str(self.convertChips(s0, "cash")) + " + $" + str(self.convertChips(s1, "cash")) # number_format($s[1]/100, 2);
					self.handtype = "tourney"
					#echo $handtype;
				else:
					#s = d[0].split("+") #explode("+", $d[0]);
					#print(s[0])
					#print(s[1])
					#s0 = decimal.Decimal(s[0])
					#s1 = decimal.Decimal(s[1])
					##s = d[0].split(" - ") #explode(" - ", $d[0]);
					#self.BUYIN = "$" + str(self.round(s0/100, 2)) + " + " + "$" + str(self.round(s1/100, 2)) # number_format($s[1]/100, 2);
					self.BUYIN = "" #not used cash...
					self.handtype = "cash";
					#echo $handtype;
				s = d[1].split(" ") #explode(" ", $d[1]);
				d = s[3].split("/") #	$d = explode("/", $s[3]);
				self.ANTE = "";
				if (len(s) > 4):
					if (s[4].strip() == "Ante"):   #			trim($s[4]) == "Ante"){
						self.ANTE = "Ante " + str(self.convertChips(s[5].strip(), self.handtype)) + " " #trim($s[5]), $handtype) . " ";
				#print(d[0], d[1])
				self.SMALLBLIND = self.convertChips(d[0], self.handtype)
				self.BIGBLIND = self.convertChips(d[1], self.handtype)
			
			elif (HH.find("Site: ") > -1):    #else if (strpos($HH[$i], "Site: ") > -1){
				#do nothing
				x = 0
			elif (HH.find("Table: ") > -1):
				s = HH.split(":") #explode(":", $HH[$i]);
				d = s[1].split("-") #explode("-", $s[1]);
				self.TOURNEYNAME = d[0].strip()
				if (len(d)>1):
					self.TABLEID = d[1].strip()
				else:
					self.TABLEID = ""
				if (self.handtype == "cash"):
					NEWHH = NEWHH + "\n\nFull Tilt Poker Game #" + str(self.HANDID) + ": " + str(self.TOURNEYNAME) + " - " + str(self.SMALLBLIND) + "/" + str(self.BIGBLIND) + " " + str(self.ANTE) + "- " + str(self.GAMETYPE) + " - " + str(self.TIME) + " ET - " + str(self.YEAR) + "/" + str(self.MONTH) + "/" + str(self.DAY) + "\n"
				else:
					NEWHH = NEWHH + "\n\nFull Tilt Poker Game #" + str(self.HANDID) + ": " + str(self.BUYIN) + " " + str(self.TOURNEYNAME) + " (" + str(self.TOURNEYID) + "), " + str(self.TABLEID) + " - " + str(self.SMALLBLIND) + "/" + str(self.BIGBLIND) + " " + str(self.ANTE) + "- " + str(self.GAMETYPE) + " - " + str(self.TIME) + " ET - " + str(self.YEAR) + "/" + str(self.MONTH) + "/" + str(self.DAY) + "\n"
				
				
				self.players = {}
				self.street = ""
				self.pot = 0
				self.spot1 = 0
				self.spot2 = 0
				self.spot3 = 0
				self.showdown = False
				self.BUTTON = ""
				self.rake = 0
				
			elif (HH.find("Seat ") > -1):
				HH = HH.replace(" - sitting out", "") #str_replace(" - sitting out", "", $HH[$i]);
				p = HH.split(" ") #explode(" ", $HH[$i]);
				amt = p[3][1:-1]       #substr($p[3], 1, strlen($p[3]) - 2);
				#print (amt)
				HH = HH.replace(p[3], "(" + str(self.convertChips(amt, self.handtype)) + ")")
				self.players[p[2].strip()] = p[1].replace(":", "")   #str_replace(":", "", $p[1]);
				#print (p[2] + "=" + self.players[p[2]] )
				self.playerstatus[p[2].strip()] = " "
				self.playerwon[p[2].strip()] = 0
				self.playershowed[p[2].strip()] = ""
				NEWHH = NEWHH + HH.replace(" - waiting for big blind", "").strip() + "\n"# trim(str_replace(" - waiting for big blind", "", $HH[$i])) . "\n";
				
			elif (HH.find("has the dealer button") > -1):
				p = HH.split(" ") #explode(" ", $HH[$i]); 
				self.BUTTON = "The button is in seat #" + self.players[p[0].strip()] + "\n"
			
			elif (HH.find("posts big blind") > -1):	
				p = HH.split(" ") 
				HH = HH.replace(" " + p[4], " " + str(self.convertChips(p[4], self.handtype)))
				NEWHH = NEWHH + HH.replace("posts big blind", "posts the big blind of") + "\n"#str_replace("posts big blind", "posts the big blind of", $HH[$i]) . "\n";
			
			elif (HH.find("posts small blind ") > -1):	
				p = HH.split(" ") 
				HH = HH.replace(" " + p[4], " " + str(self.convertChips(p[4], self.handtype)))
				NEWHH = NEWHH + HH.replace("posts small blind", "posts the small blind of") + "\n"
			
			elif (HH.find("posts ante") > -1):	
				p = HH.split(" ") 
				HH = HH.replace(" " + p[3], " " + str(self.convertChips(p[3], self.handtype)))
				NEWHH = NEWHH + HH.replace("posts ante", "antes") + "\n" 
			
			elif (HH.find("** Hole Cards **") > -1):	
				NEWHH = NEWHH + self.BUTTON;
				NEWHH = NEWHH + "*** HOLE CARDS ***\n"
				self.street = "folded before the Flop";
	
			elif (HH.find("** Flop **") > -1):	
				self.street =  " folded on the Flop"
				p = HH.split("[") 
				b = p[1].split("]") 
				NEWHH = NEWHH + "*** FLOP *** [" + b[0] + "]\n"
				self.board = self.board + b[0]
				
			elif (HH.find("** Turn **") > -1):	
				self.street =  " folded on the Turn"
				p = HH.split("[") 
				b = p[1].split("]") 
				NEWHH = NEWHH + "*** TURN *** [" + self.board + "] [" + b[0] + "]\n"
				self.board = self.board + b[0]
				
			elif (HH.find("** River **") > -1):	
				self.street =  " folded on the River"
				p = HH.split("[") 
				b = p[1].split("]") 
				NEWHH = NEWHH + "*** RIVER *** [" + self.board + "] [" + b[0] + "]\n"
				self.board = self.board + b[0]
				
			elif (HH.find(" Side Pot ") > -1):	
				#gonna have to do side pots some how by saving state...
				NEWHH = NEWHH + "*** SHOW DOWN ***\n"
				self.sidePotMode = True
				self.showdown = True
				self.winnerfound = False
				self.safetycount = 0
				self.firstHand = False
				NEWHH  = self.doSidePot(HH)
				
			elif (HH.find("** Pot Show Down **") > -1):	
				NEWHH = NEWHH + "*** SHOW DOWN ***\n"
				self.showdown = True;
			
			elif (HH.find("wins Pot") > -1):	
				try:
					p = HH.split(" ") #explode(" ", $HH[$i]);
					amt = p[3][1:-1] #amt = substr($p[3], 1, strlen($p[3]) - 2);
					self.playerwon[p[0].strip()] = amt
					amt = self.convertChips(amt, self.handtype)
					if (self.showdown):
						self.playerstatus[p[0].strip()] = "showed " + self.playershowed[p[0].strip()] + " and won (" + str(amt) + ") "
					else:
						self.playerstatus[p[0].strip()] = "collected (" + str(amt) + "), mucked"
					self.pot = amt
					NEWHH = NEWHH + p[0] + " wins the pot (" + str(amt) + ") \n"
				except:
					print("Error occurred... prolly an incomplete hand.")
					self.firstHand = False
				
			elif (HH.find(" folds") > -1):	
				p = HH.split(" ") 
				self.playerstatus[p[0].strip()] = self.street
				NEWHH = NEWHH +  HH + "\n"
				
			elif (HH.find(" calls") > -1):	
				p = HH.split(" ") 
				amt = self.convertChips(p[2].strip(), self.handtype)
				HH = HH.replace(" " + p[2], " " + str(amt)) #str_replace(" " . $p[2], " " . $amt, $HH[$i]);
				NEWHH = NEWHH +  HH.replace(" (All-in)", ", and is all in") + "\n" #str_replace(" (All-in)", ", and is all in", $HH[$i]) . "\n";
				
			elif (HH.find(" bets") > -1):	
				p = HH.split(" ") 
				amt = self.convertChips(p[2].strip(), self.handtype)
				HH = HH.replace(" " + p[2].replace(",", ""), " " + str(amt)) #.replace(",", "").strip())  # str_replace(" " . trim(str_replace(",", "", $p[2])), " " . $amt, $HH[$i]);
				NEWHH = NEWHH + HH.replace(" (All-in)", ", and is all in") + "\n"#  str_replace(" (All-in)", ", and is all in", $HH[$i]) . "\n"; 
				
			elif (HH.find(" raises") > -1):	
				p = HH.split(" ") 
				amt = self.convertChips(p[3].strip(), self.handtype)
				HH = HH.replace(" " + p[3].replace(",", ""), " " + str(amt)) #str_replace(" " . trim(str_replace(",", "", $p[3])), " " . $amt, $HH[$i]);
				NEWHH = NEWHH + HH.replace(" (All-in)", ", and is all in") + "\n" #str_replace(" (All-in)", ", and is all in", $HH[$i]) . "\n";
	
			elif (HH.find("Rake") > -1):	
				p = HH.split(" ") 
				amt = p[1][1:-1]
				#print("amt=" + amt)
				self.rake = self.convertChips(amt, self.handtype);
			
			elif (HH.find("splits Pot") > -1):	
				p = HH.split(" ") 
				amt = p[3][1:-1]
				fp = str(self.pot).replace("$", "") #str_replace("$", "", $pot);
				ev = 0
				if (self.handtype == "cash"):
					ev = eval("(" + fp + " * 100) + " + amt);
				else:
					ev = eval("(" + fp + ") + " + amt);
				amt = "(" + str(self.convertChips(amt, self.handtype)) + ")"
				self.pot = self.convertChips(ev, self.handtype)
				self.playerstatus[p[0].strip()] = "showed " + self.playershowed[p[0].strip()] + " and won " + amt + " "
				HH = HH.replace(p[3], amt) #str_replace($p[3], $amt, $HH[$i]);
				NEWHH = NEWHH + HH.replace("splits Pot", "ties for the pot") + "\n" #str_replace("splits Pot", "ties for the pot", $HH[$i]) . "\r\n";
				
			elif (HH.find(" refunded") > -1):	
				p = HH.split(" ") 
				amt = p[2].strip()
				amt = self.convertChips(amt, self.handtype)
				pl = p[0]
				NEWHH = NEWHH + "Uncalled bet of " + str(amt) + " returned to " + pl + "\n";
			
			elif (HH.find(" shows ") > -1):	
				try:
					p = HH.split(" ") 
					self.playershowed[p[0].strip()] = p[2] + " " + p[3]
					NEWHH = NEWHH + HH + "\n";
					if (self.playerwon[p[0].strip()] > 0):
						self.playerstatus[p[0].strip()] = "showed " + self.playershowed[p[0].strip()] + " and won (" + str(self.convertChips(self.playerwon[p[0].strip()], self.handtype)) + ") "
					else:
						self.playerstatus[p[0].strip()] = "showed " + self.playershowed[p[0].strip()] + " and lost "
				except:
					print("Error occurred... prolly an incomplete hand.")
					self.firstHand = False
					
			elif (HH.strip() == ""):	
				s = 1

			else:
				NEWHH = NEWHH +  HH + "\n"
				
		myfile = open(self.dest_file, "a+")
		myfile.write(NEWHH)
		myfile.close()
						

class HHConverter():

	def __init__(self, string):
		self.NewPath=string
		self.tableList = {}
		self.sHHpath = os.path.abspath(self.NewPath)


            
    
	def processDirectory(self, d, e):
		#process the directory
		#loop through directory and sub directory
		for root, dirs, files in os.walk(d):
			#print(root)
			files_in_dir = os.listdir(root)
			for name in files_in_dir:
				if name.endswith(".txt"):
					#print ("++++++++++++Now gogin through lines for .... " + root + "/" + name)
					id = time.ctime(os.path.getmtime(root + "/" + name))
					print(id)
					ppath = os.path.abspath(os.path.join(root, os.pardir))
					tOb = tableObject(ppath + "\\" + self.NewPath + "\\", name, e)
					
					f = open(root + "/" + name, 'r')
					for line in f:
						#s = 1
						tOb.processLine(line)
					if not os.path.exists(ppath + "\\Backup\\"):
						os.makedirs(ppath + "\\Backup\\")
					f.close()
					try:
						os.rename(root + "/" + name, ppath + "\\Backup\\"+ "/" + name)
					except:
						x=1
						
                        

		#files_in_dir = os.listdir(d)
		#for file_in_dir in files_in_dir:
			#print (file_in_dir)
			#process each file
				#the filename will give you info on where to save it. 
				# tableO = tableObject("the destination folder")
				#read each line of file
			#tableO.processLine("the line")

	def processCommand(self, c):
		#split command up and extract variables
		#loop and see if we have a table started for this hand?
		#if table started then
		#tableO = ??
		#if not a table create a table object and
		#tableO = tableObject("the destination folder")
		#processLine(d.text)
		cmd = urllib.parse.parse_qs(c)
		#print (str(cmd))
		#print ("command = " + cmd['Command'][0])
		if (cmd['Command'][0] == "History"):
			tOb = {}
			if cmd['Table'][0]  in self.tableList:
				tOb = self.tableList[cmd['Table'][0]];
				#print("existing table " + cmd['Table'][0])
			else:
				tOb = tableObject(self.sHHpath, str(cmd['Table'][0]).replace("/", "") + ".txt")
				self.tableList[cmd["Table"][0]] = tOb
				#print("new table " + cmd['Table'][0])
			tOb.processLine(cmd['Text'][0])
		else:
			print (str(cmd))
			
	def processCommandFile(self, fpath):
		#process the text file that has command strings. 
		self.sHHpath = os.path.abspath(os.path.join(fpath, os.pardir)) + "/" + self.NewPath + "/"
		#print (self.sHHpath)
		f = open(fpath, 'r')
		for line in f:
			#print (line)
			self.processCommand(line)
			
		