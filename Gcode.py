class Gcode():
    def __init__(self):
        pass

    def command_from_file(self, file_read):
        data_file = open(file_read, "r")
        data_file.seek(0)
        while True:
                line = data_file.readline()
                if not line:
                    break
                x = None
                y = None
                g_code = None
                z = None
                i = None
                j = None
                
                if line[0] == "G":
                    line = line.split(" ")
                    g_code =  line[0]
                    for element in line: 
                        if element[0] == "X":
                            x = float(element[1:])
                        if element[0] == "Y":
                            y = float(element[1:])
                        if element[0] == "Z":
                            z = float(element[1:])
                        if element[0] == "I":
                            i = float(element[1:])
                        if element[0] == "J":
                            j = float(element[1:])
                    yield(g_code, x, y, z, i, j)
        print("closing")
        data_file.close()

if __name__ == "__main__":

    gcode = Gcode()

    command_generator = gcode.command_from_file("Dino.ngc")

    while True:
        try:
            command = command_generator.next()
        except:
            print("File END")
            break
        if command[0] == "G00":
            pass
        if command[0] == "G01":
            pass
        if command[0] == "G02":
            print("Circle", command[4], command[5])
