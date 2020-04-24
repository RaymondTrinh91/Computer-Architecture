"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
ADD = 0b10100000
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.ir = 0b00000000

        self.equal = 0
        self.less = 0
        self.greater = 0

        self.reg[7] = self.ram[0xF4]
        self.sp = self.reg[7]

        self.op_codes = {
            HLT: self.run_HLT,
            LDI: self.run_LDI,
            PRN: self.run_PRN,
            PUSH: self.run_PUSH,
            POP: self.run_POP,
            CALL: self.run_CALL,
            RET: self.run_RET,
            JMP: self.run_JMP,
            JEQ: self.run_JEQ,
            JNE: self.run_JNE
        }
        
        pass
    
    def run_JMP(self, op_a):
        self.pc = self.reg[op_a]

    def run_JEQ(self, op_a):
        if self.equal == 1:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    def run_JNE(self, op_a):
        if self.equal == 0:
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    def op_helper(self, inst):
        params = (inst & 0b11000000) >> 6
        if params == 1:
            op_a = self.ram_read(self.pc + 1)
            self.op_codes[inst](op_a)
        elif params == 2:
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            self.op_codes[inst](op_a, op_b)
        else:
            self.op_codes[inst]()
            
    def run_HLT(self):
        sys.exit()

    def run_LDI(self, op_a, op_b):
        self.reg[op_a] = op_b

    def run_PRN(self, op_a):
        print(self.reg[op_a])
    
    def run_PUSH(self, op_a):
        self.sp -= 1
        self.ram[self.sp] = self.reg[op_a]

    def run_POP(self, op_a):
        self.reg[op_a] = self.ram[self.sp]
        self.sp += 1

    def run_CALL(self, op_a):
        return_address = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = return_address

        self.pc = self.reg[op_a]

    def run_RET(self):
        return_address = self.ram[self.sp]
        self.sp += 1
        self.pc = return_address

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue
                    
                self.ram[address] = int(line, 2)
                address += 1

        # program = [
        #     0b10000010, # LDI R0,10
        #     0b00000000,
        #     0b00001010,
        #     0b10000010, # LDI R1,20
        #     0b00000001,
        #     0b00010100,
        #     0b10000010, # LDI R2,TEST1
        #     0b00000010,
        #     0b00010011,
        #     0b10100111,# CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101, # JEQ R2
        #     0b00000010,
        #     0b10000010, # LDI R3,1
        #     0b00000011,
        #     0b00000001,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST1 (address 19):
        #     0b10000010, # LDI R2,TEST2
        #     0b00000010,
        #     0b00100000,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110,# JNE R2
        #     0b00000010,
        #     0b10000010,# LDI R3,2
        #     0b00000011,
        #     0b00000010,
        #     0b01000111,# PRN R3
        #     0b00000011,
        #     # TEST2 (address 32):
        #     0b10000010 ,# LDI R1,10
        #     0b00000001,
        #     0b00001010,
        #     0b10000010,# LDI R2,TEST3
        #     0b00000010,
        #     0b00110000,
        #     0b10100111 ,# CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101 ,# JEQ R2
        #     0b00000010,
        #     0b10000010 ,# LDI R3,3
        #     0b00000011,
        #     0b00000011,
        #     0b01000111 ,# PRN R3
        #     0b00000011,
        #     # TEST3 (address 48):
        #     0b10000010,# LDI R2,TEST4
        #     0b00000010,
        #     0b00111101,
        #     0b10100111 ,# CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110 ,# JNE R2
        #     0b00000010,
        #     0b10000010 ,# LDI R3,4
        #     0b00000011,
        #     0b00000100,
        #     0b01000111 ,# PRN R3
        #     0b00000011,
        #     # TEST4 (address 61):
        #     0b10000010,# LDI R3,5
        #     0b00000011,
        #     0b00000101,
        #     0b01000111 ,# PRN R3
        #     0b00000011,
        #     0b10000010 ,# LDI R2,TEST5
        #     0b00000010,
        #     0b01001001,
        #     0b01010100,# JMP R2
        #     0b00000010,
        #     0b01000111,# PRN R3
        #     0b00000011,
        #     # TEST5 (address 73):
        #     0b00000001,# HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL: #MUL
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1    
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        reading = True
        while reading:
            self.ir = self.ram_read(self.pc)
            inst_len = ((self.ir & 0b11000000) >> 6) + 1
            inst_alu = ((self.ir & 0b00100000) >> 5)
            set_pc = ((self.ir & 0b00010000) >> 4)


            if inst_alu:
                self.alu(self.ir, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            elif self.op_codes.get(self.ir):
                self.op_helper(self.ir)
            else:
                print("UNKNOWN OPCODE", bin(self.ir))
                running = False

            if set_pc:
                pass
            else:
                self.pc += inst_len

