class LoadTextList:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_file_path": ("STRING", {"multiline": False, "default": ""}),
                "file_name_integer": ("INT", {"default": 0}),
                "file_extension": (["txt", "csv"],),
                "format_string": ("STRING", {"default": "{:04d}"})
            }
        }
        
    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("STRING","FILENAME_STRING")
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, False)    
    FUNCTION = "loadList"
    CATEGORY = "NMWave/io"

    def loadList(self, input_file_path, file_name_integer, file_extension, format_string):
        # Convert the file_name from an integer to a string
        file_name_integer = format_string.format(file_name_integer)

        filepath = input_file_path + "\\" + file_name_integer + "." + file_extension
        print(f"Load Values: Loading {filepath}")

        list = []
            
        if file_extension == "csv":
            with open(filepath, "r") as csv_file:
                for row in csv_file:
                    list.append(row)
                    
        elif file_extension == "txt":
            with open(filepath, "r") as txt_file:
                for row in txt_file:
                    list.append(row)
        else:
            pass
        
        # Append the file extension to the filename
        filename_with_extension = file_name_integer + "." + file_extension

        return(list, filename_with_extension)