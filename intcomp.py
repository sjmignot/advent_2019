# OPCODES
ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADJUST_REL_BASE = 9
END = 99

# OPCODE to OPNAME
OPNAME = {
    1: 'add',
    2: 'mult',
    3: 'input',
    4: 'output',
    5: 'jump if true',
    6: 'jump if false',
    7: 'less than',
    8: 'equal',
    9: 'adjust rel base',
    99: 'end'   
}

# MODES
POS_MODE = 0
IM_MODE = 1
REL_MODE = 2

MODE_NAME = {
    0: 'POSITION',
    1: 'IMMEDIATE',
    2: 'RELATIVE'
}

# OP_FEATURES
operation_length = {
    ADD: 4,
    MULT: 4,
    INPUT: 2,
    OUTPUT: 2,
    END: 1,
    JUMP_IF_TRUE: 3,
    JUMP_IF_FALSE: 3,
    LESS_THAN: 4,
    EQUALS: 4,
    ADJUST_REL_BASE: 2
}

operation_num_inputs = {
    ADD: 3,
    MULT: 3,
    INPUT: 1,
    OUTPUT: 1,
    JUMP_IF_TRUE: 2,
    JUMP_IF_FALSE: 2,
    LESS_THAN: 3,
    EQUALS: 3,
    ADJUST_REL_BASE: 1
}

# JUMP SET
JUMPS = { JUMP_IF_TRUE, JUMP_IF_FALSE }

#WRITE SET
WRITES = {ADD, MULT, INPUT, LESS_THAN, EQUALS}

# DISPLAY FUNCITONS
def print_computer(comp_string):
    for i in range(0, len(comp_string), 10):
        print(f"[{i}]    {comp_string[i:i+10]}")

def print_step(opcode, win, input_modes, inputs, output, rel_base):
    print(f"{OPNAME[opcode]}")
    print(f"win: {win}")
    print(f"input modes: {[MODE_NAME[i] for i in input_modes]}")
    print(f"inputs: {inputs}")   
    print(f"output: {output}")
    print(f"rel base: {rel_base}\n")
         
# TESTS
tests = {
    (109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99):        
		[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
    (109, -1, 4, 1, 99): [-1],
    (109, -1, 104, 1, 99): [1],
    (109, -1, 204, 1, 99): [109],
    (109, 1, 9, 2, 204, -6, 99): [204],
    (109, 1, 109, 9, 204, -6, 99): [204],
    (109, 1, 209, -1, 204, -106, 99): [204],
    (109, 1, 3, 3, 204, 2, 99): [1000], #input value
    (109, 1, 203, 2, 204, 2, 99): [1000], # input value
    (104,1125899906842624,99): [1125899906842624],
}

def run_computer(comp_string, c_i, ip = 0, rel_base = 0, print_output=False, return_on_output=False):
    outputs = []
    while(True):
        opcode_and_settings = str(comp_string[ip]).zfill(5)
        opcode = int(opcode_and_settings[-2:])
       
        if(opcode == END):
            return ip, outputs
       
        input_modes = [int(opcode_and_settings[-3]), int(opcode_and_settings[-4]), int(opcode_and_settings[-5])]
       
        window_size = operation_length[opcode]
        win = comp_string[ip: ip+window_size]
        ip += window_size
       
        num_inputs = operation_num_inputs[opcode]
        inputs_prog = [win[i+1] if input_modes[i]==IM_MODE
            else comp_string[rel_base+win[i+1]] if input_modes[i]==REL_MODE
            else comp_string[win[i+1]]
            for i in range(num_inputs-1)]
       
        # WRITE OPERATIONS LOCATIONS (OUTPUT) NEVER IN POSITION MODE
        if(opcode in WRITES):
            inputs_prog.append(rel_base+win[-1] if input_modes[num_inputs-1]==REL_MODE else win[-1])
        else:
            inputs_prog.append(win[-1] if input_modes[operation_num_inputs[opcode]-1]==IM_MODE else comp_string[rel_base+win[-1]] if input_modes[num_inputs-1]==REL_MODE else comp_string[win[-1]])
        
        if(opcode == INPUT):
            inputs_prog.insert(0,c_i.pop(0))

        if(opcode == OUTPUT):
            outputs.append(inputs_prog[-1])
            if(print_output): print(inputs_prog[-1])
            if(return_on_output): return ip, outputs
            continue

        if(opcode in JUMPS):
            ip = {
                JUMP_IF_TRUE: inputs_prog[1] if inputs_prog[0] != 0 else ip,
                JUMP_IF_FALSE: inputs_prog[1] if inputs_prog[0] == 0 else ip,
            }[opcode]

        elif(opcode == ADJUST_REL_BASE):
            rel_base = {
                ADJUST_REL_BASE: rel_base+inputs_prog[0]
            }[opcode]

        else:
            comp_string[inputs_prog[-1]] = {
                ADD: (inputs_prog[0] + inputs_prog[1]),
                MULT: (inputs_prog[0] * inputs_prog[1]),
                INPUT: inputs_prog[0],
                LESS_THAN: 1 if inputs_prog[0] < inputs_prog[1] else 0,
                EQUALS: 1 if inputs_prog[0] == inputs_prog[1] else 0
            }[opcode]