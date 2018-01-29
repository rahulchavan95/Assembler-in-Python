fp=open('today2.asm','r')
fp1=open('output.text','w+a')
sym_names=[]
sym_size=[]
sym_value=[]
total_size=[]
sym_lineno=[]
literal=[]
litline=[]
lithex=[]
new=[]
original=[]
symhashinst=[]
address=[]
instset=["mov","add","push","pop","jmp","jz","cmp"]
opcodes=[50,51,52,53,54,55,56]
reg=["eax","ebx","ecx","edx","esp","esi","edi"]
reg16=["ax","bx","cx","dx"]
reg8=["ah","al","bh","bl","ch","cl","dh","dl"]
ch=fp.readline()
lno=1
Def_Undef=[]
addr_start=0
	
	
def countchar(m):
	m1=' '.join(m)
	j=0
	for i in range(0,len(m1)):
		j+=1
	return j-2

def symboltable(ch,lno):
	#rint ch
	s=ch.split()
	#print s
	if len(s)>3:
		s[2]=" ".join(s[2:len(s)])
	for i in range(0,len(s)):
		if(s[i]=='dd'or s[i]=='resd'):
			sym_names.append(s[i-1])
			sym_value.append(s[i+1])
			t=s[i+1].count(',')+1
			total_size.append(t*4)
			sym_lineno.append(lno)
			Def_Undef.append('Defined')
						
		if(s[i]=='db'):
			sym_names.append(s[i-1])
			sym_value.append(s[i+1])
			m=s[i+1:]
			cc=len(s[2].strip('"'))
			total_size.append(cc)
			sym_lineno.append(lno)
			Def_Undef.append('Defined')
		
		if(s[i]=='dq'):
			sym_names.append(s[i-1])
			sym_value.append(s[i+1])
			t=s[i+1].count(',')+1
			total_size.append(t*8)
			sym_lineno.append(lno)
			Def_Undef.append('Defined')
			
		if(s[i].endswith(':')):
			sym_names.append(s[i].strip(':'))
			sym_value.append('-')
			Def_Undef.append('Defined')
			sym_lineno.append(lno)
			total_size.append('-')
			
		if(s[i]=='jmp'):
			if(s[i+1] not in sym_names):
				sym_names.append(s[i+1])
				sym_value.append('-')
				Def_Undef.append('Undefined')
				sym_lineno.append(lno)
				total_size.append('-')
				
				
def strip_dqword(str):
	if str.startswith('dword'):
		return "%s"%str.strip('dword[').strip(']')
	if str.startswith('byte'):
	       
	        #print str.strip('byte[').strip(']'),"->",str
		return "%s"%str.strip('byte[').strip(']')
	elif str.startswith('qword'):
		return "%s"%str.strip('qword[').strip(']')
	else:
		return str	
		
		
		
def literaltable(ch,lno):
	ff=ch.split()
	for i in range(0,len(ff)):
		#print ff[i]
		if (ff[i] in instset):
			a=ff[1].split(',')
			if len(a)==2:
			 #print a,"\t in literal"
			 if a[1].startswith("'") and a[1].endswith("'"):
			  if a[0] in reg:
			   
			   literal.append(a[1].strip("'"))
			   litline.append(lno)
			   h=hex(ord(a[1].strip("'")))
			   lithex.append(h)
			  elif a[0] in reg16:
			   literal.append(a[1].strip("'"))
			   litline.append(lno)
			   h=hex(ord(a[1].strip("'")))
			   lithex.append(h)
			 	
			  elif a[0] in reg8:
			   literal.append(a[1].strip("'"))
			   litline.append(lno)
			   h=hex(ord(a[1].strip("'")))
			   lithex.append(h)
			 elif a[1].isdigit():
			  if a[0] in reg:
			   literal.append(a[1])
			   litline.append(lno)
			   h=hex(int(a[1]))
		    	   lithex.append(h)
			  elif a[0] in reg16:
			   literal.append(a[1])
			   litline.append(lno)
			   h=hex(int(a[1]))
			   lithex.append(h)
			  elif a[0] in reg8:
			   literal.append(a[1])
			   litline.append(lno)
			   h=hex(int(a[1]))
			   lithex.append(h)
		
			#if len(a)>1 and a[1].startswith("'") and a[1].endswith("'"):
						# if a[0] in reg8:
			 # print a[1],"\tregister 8"
		
		
		
def syminstr(ch,lno):
	o=ch.split()
	
	for i in range(0,len(o)):
		if (o[i] in instset):
		        #print o
			a=o[1].split(',')
			
			#print a[1]
			if(len(a)==1):
			 #print "o="
			 if a[0] in reg :
			  #print "rrrrr=",str(opcodes[instset.index(o[i])])
			  #addr_start=addr_start+getaddress(o[1])
			  #symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg32\t\t\t"+o[i]+" "+a[0]+"\t\t")
			   if o[0]=='push':
			    symhashinst.append("op#8\t"+"reg32\t\t\t"+o[i]+" "+a[0]+"\t\t")
			   elif o[0]=='pop':
			    symhashinst.append("op#9\t"+"reg32\t\t\t"+o[i]+" "+a[0]+"\t\t")
			  
			 elif a[0] in sym_names:
			  #symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"sym#%s"%str(sym_names.index(a[0])+1)+"\t\t\t"+o[i]+" "+a[0]+"\t\t\t")		  
			  if o[0]=='push':
			     symhashinst.append("op#8A\t"+"sym#%s"%str(sym_names.index(a[0])+1)+"\t\t\t"+o[i]+" "+a[0]+"\t\t\t")		
			  elif o[0]=='pop':
			     symhashinst.append("op#9A\t"+"sym#%s"%str(sym_names.index(a[0])+1)+"\t\t\t"+o[i]+" "+a[0]+"\t\t\t")		
			  elif o[0]=='jmp':
			     symhashinst.append("op#10A\t"+"sym#%s"%str(sym_names.index(a[0])+1)+"\t\t\t"+o[i]+" "+a[0]+"\t\t\t")		
			  elif o[0]=='jz':
			    symhashinst.append("op#11A\t"+"sym#%s"%str(sym_names.index(a[0])+1)+"\t\t\t"+o[i]+" "+a[0]+"\t\t\t")		
			 elif a[0] in reg16:
			  
			  #symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg16\t\t\t"+o[i]+" "+a[0]+"\t\t")
			   if o[0]=='push':
			    symhashinst.append("op#8B\t"+"reg16\t\t\t"+o[i]+" "+a[0]+"\t\t")
			   elif o[0]=='pop':
			    symhashinst.append("op#9B\t"+"reg16\t\t\t"+o[i]+" "+a[0]+"\t\t")
			   
			if(len(a)>1):
			 a[1]=strip_dqword(a[1])
		         print o,a
			 if (a[0] in reg and a[1] in sym_names):
				m=0
			
				while(sym_names[m]!=a[1]):
					m+=1
				b="sym#%s"%str(sym_names.index(a[1])+1)
			
				new.append(b)
				if o[0]=='mov':
				 symhashinst.append("op#5\t"+"reg32,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#6\t"+"reg32,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#7\t"+"reg32,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg32,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				original.append(o[i]+" "+a[0]+","+a[1])
				
			 elif (a[0] in reg16 and a[1] in sym_names):
				m=0
			
				while(sym_names[m]!=a[1]):
					m+=1
				b="sym#%s"%str(sym_names.index(a[1])+1)
			
				new.append(b)
				if o[0]=='mov':
				 symhashinst.append("op#5A\t"+"reg16,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#6A\t"+"reg16,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#7A\t"+"reg16,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg16,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				original.append(o[i]+" "+a[0]+","+a[1])	
				
			 
			 
			 elif (a[0] in reg8 and a[1] in sym_names):
				m=0
			
				while(sym_names[m]!=a[1]):
					m+=1
				b="sym#%s"%str(sym_names.index(a[1])+1)
			
				new.append(b)
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg8,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':
				 symhashinst.append("op#5B\t"+"reg8,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#6B\t"+"reg8,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#7B\t"+"reg8,"+str(b)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				
				original.append(o[i]+" "+a[0]+","+a[1])	
				
			 
			 
					 
			 
			 elif (a[0] in reg and a[1] in reg):
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg32,reg32"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':
				 symhashinst.append("op#5C\t"+"reg32,reg32"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#6C\t"+"reg32,reg32"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#7C\t"+"reg32,reg32"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				
				original.append(o[i]+" "+a[0]+","+a[1])
				
			
			
			 elif (a[0] in reg16 and a[1] in reg16):
			        if o[0]=='mov':			        
			         symhashinst.append("op#5D\t"+"reg16,reg16"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':			        
			         symhashinst.append("op#6D\t"+"reg16,reg16"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':			        
			         symhashinst.append("op#7D\t"+"reg16,reg16"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg16,reg16"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				original.append(o[i]+" "+a[0]+","+a[1])
				
			 elif (a[0] in reg8 and a[1] in reg8):
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg8,reg8"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':
				 symhashinst.append("op#5E\t"+"reg8,reg8"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#6E\t"+"reg8,reg8"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#7E\t"+"reg8,reg8"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")

				original.append(o[i]+" "+a[0]+","+a[1])
			
			
				
			 
			
			 elif(a[0] in reg and a[1].strip("'") in literal):
			 
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\treg32"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':
			         symhashinst.append("op#51\treg32"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
			        if o[0]=='add':
			         symhashinst.append("op#61\treg32"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
			        if o[0]=='cmp':
			         symhashinst.append("op#71\treg32"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
			 elif(a[0] in reg8 and 	a[1].strip("'") in literal):
			    
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':
				 symhashinst.append("op#52\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='add':
				 symhashinst.append("op#62\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='cmp':
				 symhashinst.append("op#72\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
			
		
				
			 elif(a[0] in reg8 and 	a[1] in literal):
			 
				#symhashinst.append(str(opcodes[instset.index(o[i])])+"\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				if o[0]=='mov':	
			          symhashinst.append("op#53\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")	
			        if o[0]=='add':	
			          symhashinst.append("op#63\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")	
			        if o[0]=='cmp':	
			          symhashinst.append("op#73\treg8"+",lit#%s"%str(literal.index(a[1].strip("'"))+1)+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")	
			 
			 
			 
			 
				
def getaddress(st):
	#rint st
	d=st.split(',')
	#
	
	#print d
	if len(d)==1:
	 return 2
	 '''if strip_dqword(d[0]) in reg:
	  return 2,d,lno
	 if strip_dqword(d[0]) in sym_names:
	  return 4,d,lno'''
	 
	else:
	 #print "ddd=",d
	 if d[0] in reg and d[1] in reg:
		return 4
	
	
	 elif d[0] in reg and strip_dqword(d[1]) in sym_names:
	
		for j in range(0,len(sym_names)):
			if sym_names[j]==strip_dqword(d[1]):
				return total_size[j]+2
				
	 elif strip_dqword(d[0]) in sym_names and d[1] in reg:
		for j in range(0,len(sym_names)):
			if sym_names[j]==strip_dqword(d[1]):
				return total_size[j]+2
	
	 elif d[0] in reg and d[1].strip("'") in literal:
		for j in range(0,len(literal)):
			if literal[j]==d[1].strip("'"):
				return total_size[j]+2
				
	
	 elif d[0] in reg8 and d[1].strip("'") in literal:
		for j in range(0,len(literal)):
			if literal[j]==d[1].strip("'"):
				return total_size[j]+2			
				
				
	 elif d[0].strip("'") in literal and d[1] in reg:
		for j in range(0,len(literal)):
			if literal[j]==d[1].strip("'"):
				return total_size[j]+2
	
	 elif d[0] in reg and d[1].isdigit():
		return 2
	
	 elif d[0] in reg8 and d[1].isdigit():
		return 2
	
	
	 elif d[0] in reg16 and d[1] in reg16:
		return 4
	
	 elif d[0] in reg8 and d[1] in reg8:
		return 4
	
	
	 elif d[0] in reg8 and d[1] in reg8:
		return 4
	
	 elif (d[0] in reg8 and strip_dqword(d[1]) in reg8) or (d[0] in reg8 and strip_dqword(d[1]) in sym_names):
	    	return 4
	 
	 elif d[0] in reg8 and d[1] in sym_names:
		return 4
		
	 elif d[0] in reg8 and d[1].strip("'") in literal:
		return 4
	 
	 
	 else:
	    #print strip_dqword(d[1]),"\t0\t",d[1]
	    return 0
	    
	 
def generateAddr(str):
 char_cnt=6
 char_cnt=char_cnt-len(str)
 str1=''
 for i in range(char_cnt):
  str1=str1+'0'
 #print str1
# print len(str)
 return str1+str


	    
	    

def magic(sym_lineno):
    s = ''.join(map(str, numList))
    return int(s)


sum=0
		
while(ch!=""):
	symboltable(ch,lno)
	literaltable(ch,lno)
	syminstr(ch,lno)

	st=ch.split()	
	#print st
	for i in range(len(st)):
		if(st[i] in instset):
			#print st
			addr=getaddress(st[i+1])
			#print addr,st
			sum=sum+addr
			#print sum
			address.append(sum)
	
	ch=fp.readline()
	lno+=1
	


#prints the symbol table
fp1.write("\n\t\t\t\tSYMBOL TABLE\n\n")
fp1.write("LINENO \t\t SYMBOLS \t\t VAlUES \t TOTAL SIZE \t\t D/UD")	
for i in range(len(sym_names)):
	fp1.write("\n"+str(sym_lineno[i])+'\t\t'+sym_names[i]+'\t\t\t'+str(sym_value[i])+'\t\t\t'+str(total_size[i])+'\t\t'+Def_Undef[i]+"\n")


#Prints the Literal table
fp1.write("\n\n\n\t\tLITERAL TABLE\n\n")	
fp1.write("LINENO \t LITERAL VALUE \t\t HEX VALUE")
for i in range(len(literal)):
	fp1.write("\n"+str(litline[i])+'\t\t'+literal[i]+'\t\t'+lithex[i]+'\n')
	
	
fp1.write("\n\n\n\t\t\tIntermediate Code\n\n")
for i in range(len(symhashinst)):
	fp1.write("\n"+symhashinst[i]+"\t"+generateAddr(str(address[i]))+"\n")


print "symbols= ",sym_names,len(sym_names)
print "values= ",sym_value,len(sym_value)
print "total size= ",total_size,len(total_size)
print "lineno= ",sym_lineno,len(sym_lineno)
print "literals= ",literal
print "litlineno= ",litline
print "literalhex= ",lithex
#print "symhash= ",new
print "original inst= ",original
print "sym instr= ",symhashinst
print "addresses= ",address,len(address)
print "Def_Undef=",Def_Undef,len(Def_Undef)



'''

			  elif (a[0] in reg16 and a[1] in reg16):
				symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg16,reg16"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				original.append(o[i]+" "+a[0]+","+a[1])
				
			  elif (a[0] in reg8 and a[1] in reg8):
				symhashinst.append(str(opcodes[instset.index(o[i])])+"\t"+"reg8,reg8"+"\t\t"+o[i]+" "+a[0]+","+a[1]+"\t\t")
				original.append(o[i]+" "+a[0]+","+a[1])
'''							
