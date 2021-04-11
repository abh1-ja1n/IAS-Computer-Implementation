memory = [[0 for i in range(40)] for j in range(1000)]

PC = [0 for x in range(12)]
AC = [0 for x in range(40)]
IR = [0 for x in range(8)]
IBR = [0 for x in range(20)]
MAR = [0 for x in range(12)]
MBR = [0 for x in range(40)]
MQ = [0 for x in range(40)]
HALT = False
k=0
JUMP_RIGHT = False


def list_to_string(s):
	string = ""
	for i in s:
		string += str(i)
	return string

def equalList(x, y):
	if(len(x)!=len(y)):
		return False
	i = min(len(x), len(y))
	for i in range(i):
		if(x[i]!=y[i]):
			return False
	return True



def binary_to_int(b_list):
	res = int("".join(str(x) for x in b_list), 2) 
	return res

def add_binary_nums(x,y):
        max_len = max(len(x), len(y))
        x = x.zfill(max_len)
        y = y.zfill(max_len)

        result = ''
        carry = 0

        for i in range(max_len-1, -1, -1):
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1       

        if carry !=0 : result = '1' + result

        return result.zfill(max_len)


def fetch():
	global PC, MAR, IR, IBR, memory, HALT, JUMP_RIGHT, k

	k+=1
	if(JUMP_RIGHT == True):
		MAR = PC[:]
		MBR = memory[binary_to_int(MAR)][:]
		IR = MBR[20:28]
		MAR = MBR[28:40]
		PC = list(add_binary_nums(list_to_string(PC),'1'))
		PC = list(map(int, PC))
		JUMP_RIGHT = False
		return


	if(equalList(memory[binary_to_int(PC)],[0 for x in range(40)])==True):
		HALT = True
	else:
		if(equalList(IBR,[0 for x in range(20)])==True):
			MAR = PC[:]
			MBR = memory[binary_to_int(MAR)][:]
			
			if(equalList(MBR[0:8],[0 for x in range(8)])==True):
				IR = MBR[20:28]
				MAR = MBR[28:40]
				PC = list(add_binary_nums(list_to_string(PC),'1'))
				PC = list(map(int, PC))
				#[x:y] y is not included
			else:
				IBR = MBR[20:40]
				IR = MBR[0:8]
				MAR = MBR[8:20]				

		else:
			IR = IBR[0:8]
			MAR = IBR[8:20]
			PC = list(add_binary_nums(list_to_string(PC),'1'))
			PC = list(map(int, PC))
			IBR = [0 for x in range(20)]



def load_mx():
	global AC, memory, MAR, MBR

	MBR = memory[binary_to_int(MAR)][:]
	AC = MBR[:]
	return

def store_mx():
	global AC, memory, MAR, MBR

	MBR = AC[:]
	memory[binary_to_int(MAR)] = MBR[:]
	return

def load_mq():
	global MQ, AC

	AC = MQ[:]
	return

def add_mx():
	global AC, memory, MBR, MAR


	MBR = memory[binary_to_int(MAR)][:]
	if(AC[0] == 1 and MBR[0] == 1):
		AC = list(add_binary_nums(''.join(str(AC[1:])), ''.join(str(MBR[1:]))).zfill(40))
	elif(MBR[0] == 1):
		AC = list(add_binary_nums(''.join(str(AC)), ''.join(str(MBR[1:]))))
	elif(AC[0] == 1):
		AC = list(add_binary_nums(''.join(str(AC[1:])), ''.join(str(MBR))))
	else:
		AC = list(add_binary_nums(''.join(str(AC)), ''.join(str(MBR))))

	AC = list(map(int, AC))
	return

def div_mx():
	global AC, memory, MBR, MAR, MQ

	MBR = memory[binary_to_int(MAR)][:]
	if(bin(int(binary_to_int(AC)/binary_to_int(MBR)))[0]=="-"):
		AC = list((bin(int(binary_to_int(AC)%binary_to_int(MBR))))[3:].zfill(40))
		AC = list(map(int, AC))
		AC[0] = 1
		MQ = list((bin(int(binary_to_int(AC)/binary_to_int(MBR))))[3:].zfill(40))
		MQ = list(map(int, MQ))
		MQ[0] = 1
	else:
		
		MQ = list((bin(int(binary_to_int(AC)/binary_to_int(MBR))))[2:].zfill(40))
		MQ = list(map(int, MQ))
		AC = list((bin(int(binary_to_int(AC)%binary_to_int(MBR))))[2:].zfill(40))
		AC = list(map(int, AC))
	return

def jump_mx_l():
	global AC, memory, MBR, MAR

	MBR = memory[binary_to_int(MAR)][:]
	PC = MBR[8:20]
	return

def jump_mx_r():
	global AC, memory, MBR, MAR

	MBR = memory[binary_to_int(MAR)][:]
	PC = MBR[28:40]
	JUMP_RIGHT = True
	return

def jumpc_mx_l():
	global AC, memory, MBR, MAR

	if(AC[0] == 0):
		MBR = memory[binary_to_int(MAR)][:]
		PC = MBR[8:20]
		MAR = PC[:]
	return

def jumpc_mx_r():
	global AC, memory, MBR, MAR

	if(AC[0] == 0):
		MBR = memory[binary_to_int(MAR)][:]
		PC = MBR[28:40]
		JUMP_RIGHT = True
	return

def lhs():
	global AC
	AC_new = [0 for x in range(40)]
	AC_new[0] = AC[0]
	for i in range(1,len(AC)-1):
		AC_new[i] = AC[i+1]
	AC = AC_new[:]

def rhs():
	global AC
	AC_new = [0 for x in range(40)]
	AC_new[0] = AC[0]
	for i in range(0,len(AC)-1):
		AC_new[i+1] = AC[i]
	AC = AC_new[:]


def execute():

	opcode = list_to_string(IR)
	print("Opcode " + opcode + " instruction running...")

	if(opcode == '00000001'):
		load_mx()
	elif(opcode == '00001010'):
		load_mq()
	elif(opcode == '00100001'):
		store_mx()
	elif(opcode == '00000101'):
		add_mx()
	elif(opcode == '00001100'):
		div_mx()
	elif(opcode == '00001101'):
		jump_mx_l()
	elif(opcode == '00001110'):
		jump_mx_r()
	elif(opcode == '00001111'):
		jumpc_mx_l()
	elif(opcode == '00010000'):
		jumpc_mx_r()
	elif(opcode == '00010100'):
		lhs()
	elif(opcode == '00010101'):
		rhs()

def feed_data(i, address):
	global memory

	if(i>=0):
		memory[address] = bin(i)[2:].zfill(40)
	else:
		memory[address] = bin(i)[3:].zfill(40)
		memory[address][0] = 1

def feed_address(address):
	return bin(address)[2:].zfill(12)

def hardcode():
	"""
	int a = 5;
	int b = 10;
	int c = 3;
	int res = (a+b)/c;

	In memory:

	251 5
	252 10
	253 3
	
	ASSEMBLY CODE:
		LOAD(M(251)) ADD(M(252))
		DIV(M(253))  LOAD(MQ)
		STOR(M(254)) 

	"""
	feed_data(5,251)
	feed_data(10,252)
	feed_data(3,253)

	mem = "00000001" + feed_address(251) + "00000101" + feed_address(252)
	memory[0] = list(map(int, list(mem)))

	mem = "00001100" + feed_address(253) + "00001010" + feed_address(0)
	memory[1] = list(map(int, list(mem)))

	mem = "00000000" + feed_address(0) + "00100001" + feed_address(254)
	memory[2] = list(map(int, list(mem)))


	#PROGRAM 2
	"""
	
	int a = -8;
	int c;
	if(a>0):
		c = c >> 1
	else:
		c = c << 1
	
	In memory:
	261 -8

	Assembly code:

	LOAD(M(261))  JUMP+(M(4):left)
	 RHS()         LHS()
	 STOR(M(264))

	"""

	mem = "00000001" + feed_address(261) + "00001111" + feed_address(6)
	memory[3] = list(map(int, list(mem)))

	mem = "00010100" + feed_address(0) + "00010101" + feed_address(0)
	memory[4] = list(map(int, list(mem)))

	mem = "00000000" + feed_address(0) + "00100001" + feed_address(264)



hardcode()
while(HALT == False):
	fetch()
	if(HALT == False):
		execute()

























