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

        
    def text_font(self, file_read, letter):
        data_file = open(file_read, "r")
        data_file.seek(0)

        while True:
            line = data_file.readline()
            if not line:
                print("Letter not found")
                return
            if line.startswith("#" + str(letter.upper())):
                print("Found :" + str(letter.upper()))
                break
            
        while True:
                line = data_file.readline()
                if not line or line.startswith("#"):
                    break
                g_code = None
                x = None
                y = None
                z = None
                i = None
                j = None

                if line[0] == "G":
                    line = line.split(" ")
                    g_code =  line[0]

                    for element in line: 
                        if "X" in element:
                            x = float(element[1:])
                        if "Y" in element:
                            y = float(element[1:])
                        if "Z" in element:
                            z = float(element[1:])
                        if "I" in element:
                            i = float(element[1:])
                        if "J" in element:
                            j = float(element[1:])          
                    yield(g_code, x, y, z, i, j)
        data_file.close()


if __name__ == "__main__":

    gcode = Gcode()

    #command_generator = gcode.command_from_file("Dino.ngc")
    command_generator = gcode.command_from_file("TextFont.ngc")

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
