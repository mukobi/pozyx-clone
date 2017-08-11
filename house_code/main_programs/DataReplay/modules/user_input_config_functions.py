class UserInputConfigFunctions():
    @staticmethod
    def get_multiple_attributes_to_log(
            prompt1="What do you want to log?\n(pressure, acceleration, "
                    "magnetic, angular velocity, euler angles, quaternion, "
                    "linear acceleration, or gravity)\n",
            prompt2="\nWhat else do you want to log?\n(pressure, acceleration, "
                    "magnetic, angular velocity, euler angles, quaternion, "
                    "linear acceleration, or gravity)\n"
                    "Press enter to be done.\n"):
        possible_attributes = ["pressure", "acceleration", "magnetic", "angular velocity", "euler angles",
                               "quaternion", "linear acceleration", "gravity"]
        attributes_to_log_list = []
        user_input = ""
        # ask for first attribute to log
        while user_input not in possible_attributes:  # check if input is correct
            user_input = input(prompt1)
            attributes_to_log_list.append(user_input)
        # keep adding attributes to log as the user says
        while True:
            user_input = input(prompt2)
            # if user hits enter, stop asking
            if user_input == "":
                break
            if user_input in possible_attributes: # check if correct input
                attributes_to_log_list.append(user_input)
        return attributes_to_log_list

    @staticmethod
    def get_file_to_replay(
            prompt="Give the path to the file you want to replay.\n"):
        file = input(prompt)
        # allows whitespace in file names
        file = file.strip('"')
        return file

    @staticmethod
    def get_speed(
            prompt="Enter replay speed, 0 is as fast as possible, default 1\n"):
        str_speed = input(prompt)
        if str_speed == '':
            # enter was pressed
            return 1
        return int(str_speed)