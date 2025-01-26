from controller import Robot
import time
import asyncio

async def example():
    print("Start waiting...")
    await asyncio.sleep(5)  # Wait for 5 seconds asynchronously
    print("Finished waiting!")

def run_robot(robot):
    timestep = int(robot.getBasicTimeStep())
    max_speed = 6.28

    # Initialize motors
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")
    
    left_motor.setPosition(float("inf"))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float("inf"))
    right_motor.setVelocity(0.0)
    
    # Initialize proximity sensors
    prox_sensors = []
    for ind in range(8):
        sensor_name = "ps" + str(ind)
        prox_sensors.append(robot.getDevice(sensor_name))
        prox_sensors[ind].enable(timestep)
    
    # Initialize camera
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # Define the color sequence to follow
    COLOR_SEQUENCE = ["Green","#FF0000", "#FFFF00", "#FF00FF", "#A5691E", "#00FF00"]  # Red, Yellow, Pink, Brown, Green
    COLOR_SEQUENCE_2 = [ "Red","Yellow", "Pink", "Brown", "Green"]
    color_index = 0

    def detect_color_hex():
        """Detect the color in front of the robot using the camera."""
        image = camera.getImage()
        r = camera.imageGetRed(image, camera.getWidth(), camera.getWidth() // 2, camera.getHeight() // 2)
        g = camera.imageGetGreen(image, camera.getWidth(), camera.getWidth() // 2, camera.getHeight() // 2)
        b = camera.imageGetBlue(image, camera.getWidth(), camera.getWidth() // 2, camera.getHeight() // 2)
        color_detected = f"#{r:02X}{g:02X}{b:02X}"
        return color_detected  
      
    def detect_color():
        left_wall_detect = prox_sensors[5].getValue() > 110 
        if not (left_wall_detect):
            return "Unknown"
        

        hex_code = detect_color_hex().lstrip('#')
 
    
        # return hex_code
        yellow = [
            "AEAF6C", "B0B16C", "B5B66C", "AEB06C", "B9BA6C", "AEAF6C", "ADAE6E", "AFB070",
            "B0B170", "B4B572", "B0B173", "B3B474", "B3B476", "B1B277", "B8B976", "AEAF75",
            "9D9F73", "B5B673", "B5B673", "B1B274", "B3B475", "B1B276", "B7B877",
            "B5B676", "B1B275", "B4B574", "ADAE74", "ACAD74", "B2B374", "B2B375", "AAAC76",
            "B6B775", "B0B172", "B0B170", "B5B772", "B1B270", "DDDD1E", "D3D41C", "D0D11B",
            "D4D51C", "C7C81A", "CECF1B", "D6D71D", "E1E21E", "DFE01E", "CDCE1B", "D4D51C",
            "DBDB1D", "CBCC1B", "D1D21C", "BEBF19", "DCDD1E", "D1D21C", "CFD01B", "C5C71A",
            "CECF1C", "C3C419", "CCCD1B", "D9DA1D", "D8D91D", "DCDD1E", "CECF1B", "D1D31C",
            "D6D71D", "D5D61D", "D4D51D", "D4D51D", "D4D51D", "D4D51D", "D4D51D", "D4D51D",
            "D4D51D", "D4D51D", "D4D51D", "D4D61D", "D5D61D", "D2D31C", "D1D21B", "DADB1D",
            "DEDF1E", "D6D71C", "D0D11C", "DDDE1E", "E0E11F", "DBDC1E", "D2D41D", "D3D41D"
        ]
        if hex_code in yellow:
            return "Yellow"


        red =[
            "464B5E", "464C61", "464E68", "464E67", 
            "464D62", "464C62", "464C60", "460A0D", "470B0E", "460A0E", "464B5C","36222C"
        ]


        pink = [
            "A128A7", "A033A7", "A433AB", "A132A8", "A131A8", "A330A9", "A12FA8", "A233A8",
            "A33BA9", "A643AD", "A642AC", "A33BA9", "A23BA9", "A33BA9", "A43EAB", "A444AB",
            "A64AAC", "A64AAD", "A649AD", "A648AC", "A448AB", "A247A9", "A74DAD", "595067",
            "B375B9", "B075B6", "B375B8", "B375B8", "B175B7",
            "B875BD", "AE75B4", "B275B8", "B075B6", "AF75B5", "B875BD", "AD75B3", "A875AE",
            "B675BC", "A975AF", "B775BC", "AC75B2", "B275B7", "AC75B2", "B575BA", "B475BA",
            "AF74B5", "B173B6", "A971AF", "B970BE", "B06EB6", "B16EB6", "B16EB6", "B16EB7",
            "B16EB7", "B16EB7", "B16EB7", "B16EB7", "B16EB7", "B16EB7", "B16EB7", "B16CB7",
            "A867AE", "B367B9", "B367B9", "B367B9", "B467B9", "B367B9", "B367B9", "B367B9",
            "B467B9", "AB61B1", "AB61B1", "AB61B1", "AB61B1", "AB61B1", "AB61B1", "AB61B1",
            "B372B9", "B972BE", "B572BB", "B772BD", "AE72B4", "AD72B3", "B071B6", "B272B7",
            "AE71B4", "B272B7", "A871AF", "AE70B4", "B470BA", "AD71B3", "B171B7", "B071B6",
            "AE70B4", "B270B7", "AB6EB1", "B76FBD", "B06FB6", "AF6AB5", "A467AB", "A964AF",
            "AC64B2", "AB64B1", "AB64B1", "AB64B1", "AB64B1", "AB64B1", "AB64B1", "AB64B1",
            "AB64B1", "AB64B1", "AC5DB2", "AA6CB0", "AF6AB4", "AF6AB5"
        ]
        pink.extend([
            "D01AD5", "D11AD6", "D61BDA", "D21AD7", "CB19D1", "DB1CDF", "CB19D0", "D31BD8",
            "D61CDB", "C919CF", "D51BDA", "CA19CF", "CF1AD4", "D81CDD"
        ])
 
        brown = [
            "9A6A2F", "9A6A2E", "A17030", "9E6D2F", "93652C", "9E6E2F", "96672D", "A77532",
            "A77531", "96672C", "8F622A", "9C6C2E", "9F6E2F", "A57331", "9B6B2E", "9B6B2E",
            "A16F2F", "9B6B2D", "895E29", "92642B", "95662C", "99692D", "A47230", "AF7B34"
        ]

        green = [
           "1CDE1E", "1BD21D", "1AD01C",
            "1CE41F", "18BD1A", "18B41A", "18B31A", "1BDB1D", "19C21B", "19CA1B", "1AD31D",
            "1BDA1D", "18C31A", "1CE01E", "1BDF1E", "1AD61C", "1AD81C", "1AD11C", "1CE01E",
            "1BDE1E", "1ACF1C", "15A317", "107F12", "16BC18", "1AD51C", "16B917", "17C018",
            "16B718", "16B118", "1AD61C", "1BDA1D", "18C51A", "18C519", "1AD61C", "1AD41C",
            "19CF1B", "19CD1B", "17C019", "19CC1A", "1BDA1D", "1BDB1D", "1BDC1D", "1BDC1D",
            "1BDC1D", "1BDA1D", "19CE1B", "19D11C", "1CE11F"

            "1BD31D", "1ACF1C", "1AD51D", "19CB1B", "1AD71C", "18BC1A", "17B519", "1CE31E",
            "18BD1A", "15A916", "16B119", "1BE01E", "1AD71D", "1AD21C", "1AD01C", "19CA1C",
            "1ADA1D", "1AD51C", "1AD61C", "1CE21E", "1BDB1E", "19CE1B", "1BDC1D", "1AD31C",
            "19D11B", "19CF1B", "19CD1B", "18CB1B", "18CA1B", "19CC1B", "1BDD1E", "16BA18",
            "1BDA1D", "1AD41C", "1BD91D"
        ]
        if hex_code in green:
            return "Green"
        elif hex_code in brown:
            return "Brown"
        elif hex_code in pink:
            return "Pink"
        elif hex_code in yellow:
            return "Yellow"
        elif "460" in hex_code:
            return "Red"
        return "Unknown"

    while robot.step(timestep) != -1:
        # Wall-following logic
        left_wall = prox_sensors[5].getValue() > 80
        left_corner = prox_sensors[6].getValue() > 72
        front_wall = prox_sensors[7].getValue() > 80

        left_speed = max_speed
        right_speed = max_speed

        if front_wall:
            left_speed = max_speed
            right_speed = -max_speed
        else:
            if left_wall:
                left_speed = max_speed
                right_speed = max_speed
            else:
                left_speed = max_speed / 8
                right_speed = max_speed
            if left_corner:
                left_speed = max_speed
                right_speed = max_speed / 8

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

        # Detect the color of the wall in front
        detected_color = detect_color()
   

        color_to_print = COLOR_SEQUENCE_2[color_index]
        if color_to_print == "Red":
            print(f"Searching for: \033[31m{color_to_print}\033[0m")
        elif color_to_print == "Yellow":
            print(f"Searching for: \033[33m{color_to_print}\033[0m")
        elif color_to_print == "Green":
            print(f"Searching for: \033[32m{color_to_print}\033[0m")
        elif color_to_print == "Brown":
            print(f"Searching for: \033[38;5;94m{color_to_print}\033[0m")  # Brown is not standard, using Yellow
        elif color_to_print == "Pink":
            print(f"Searching for: \033[35m{color_to_print}\033[0m")
        else:
            print(detected_color)

        if color_index != 0:
            print("Detected colors: ", end="")
        for i in range(color_index):
            color = COLOR_SEQUENCE_2[i]
            if color == "Red":
                print(f"\033[31m{color}\033[0m", end=" ")
            elif color == "Yellow":
                print(f"\033[33m{color}\033[0m", end=" ")
            elif color == "Green":
                print(f"\033[32m{color}\033[0m", end=" ")
            elif color == "Brown":
               print(f"\033[33m{color}\033[0m", end=" ") # Brown is not standard, using Yellow
            elif color == "Pink":
                print(f"\033[35m{color}\033[0m", end=" ")
            else:
                print(color, end=" ")
        print("\n")


        # if color_to_print == "Red":
        #     print(f"Searching for: \033[31m{color_to_print} color\033[0m")
        # elif color_to_print == "Yellow":
        #     print(f"Searching for: \033[33m{color_to_print} color\033[0m")
        # elif color_to_print == "Green":
        #     print(f"Searching for: \033[32m{color_to_print} color\033[0m")
        # elif color_to_print == "Brown":
        #     print(f"Searching for: \033[33m{color_to_print} color\033[0m")  # Brown is not standard, using Yellow
        # elif color_to_print == "Pink":
        #     print(f"Searching for: \033[35m{color_to_print} color\033[0m")
        # else:
        #     print(f"Searching for: {color_to_print} color")

        if detected_color == COLOR_SEQUENCE_2[color_index]:
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(0.0)
            if detected_color == "Red":
                print(f"\033[31m{detected_color} color detected successfully\033[0m")
            elif detected_color == "Yellow":
                print(f"\033[33m{detected_color} color detected successfully\033[0m")
            elif detected_color == "Green":
                print(f"\033[32m{detected_color} color detected successfully\033[0m")
            elif detected_color == "Brown":
                print(f"\033[33m{detected_color} color detected successfully\033[0m")
            elif detected_color == "Pink":
                print(f"\033[35m{detected_color} color detected successfully\033[0m")
            color_index += 1
            start_time = time.time()
            wait = True
            while time.time() - start_time < 4:
                if wait:
                    print("Waiting for few seconds...")
                    wait = False

                if robot.step(timestep) == -1:
                    break
            left_motor.setVelocity(max_speed)
            right_motor.setVelocity(max_speed)
            
            
            # Stop the robot if all colors are detected
            if color_index >= len(COLOR_SEQUENCE_2):
                print("All the colors have been detected. Stopping the robot.")
                left_motor.setVelocity(0.0)
                right_motor.setVelocity(0.0)
                break  # Exit the loop

if __name__ == "__main__":   
    
    my_robot = Robot()
    run_robot(my_robot)