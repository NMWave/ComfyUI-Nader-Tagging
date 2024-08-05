import re

class TagDuplicateRemover:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tag_field": ("STRING", {"forceInput": True}),
                "tag_delimiter": ("STRING", {"default":", "})
            }
        }
    
    RETURN_TYPES = ("STRING",)

    FUNCTION = "removeDuplicates"

    CATEGORY = "Naders Nodes"

    def removeDuplicates(self, tag_field, tag_delimiter):
        tag_list = tag_field.split(tag_delimiter)
        duplicates_removed_tags = tag_delimiter.join(dict.fromkeys(tag_list))
        return (
            duplicates_removed_tags,
        )

class CombineAlternatingTags:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tag_field1": ("STRING", {"forceInput": True}),
                "tag_field2": ("STRING", {"forceInput": True}),
                "tag_delimiter": ("STRING", {"default":", "})
            },
            "optional": {
                "tag_field3_opt": ("STRING", {"default": '', "multiline": False}),
                "tag_field4_opt": ("STRING", {"default": '', "multiline": False}),
                "tag_field5_opt": ("STRING", {"default": '', "multiline": False})
            }
        }
    
    RETURN_TYPES = ("STRING",)

    FUNCTION = "tagCombine"

    CATEGORY = "Naders Nodes"

    def tagCombine(self, tag_field1, tag_field2, tag_field3_opt, tag_field4_opt, tag_field5_opt, tag_delimiter):
        tags = [tag_field.split(tag_delimiter) if tag_field else [] for tag_field in [tag_field1, tag_field2, tag_field3_opt, tag_field4_opt, tag_field5_opt]]
        lengths = [len(tag) for tag in tags]
        total_len = sum(lengths)
        
        if total_len != 0:
            ratios = [l / total_len for l in lengths]
        else:
            ratios = [0, 0, 0, 0, 0]

        combined_tags = []
        indices = [0, 0, 0, 0, 0]

        # Calculate the number of rounds based on the smallest non-zero ratio
        rounds = int(1 / min(r for r in ratios if r > 0))

        for _ in range(rounds):
            for field in range(5):
                # Calculate the number of tags to take from this field in this round
                take = int(round(ratios[field] * rounds))
                for _ in range(take):
                    if indices[field] < lengths[field]:
                        combined_tags.append(tags[field][indices[field]])
                        indices[field] += 1

        # If there are still tags remaining after the round-robin allocation, append them to the end
        for field in range(5):
            while indices[field] < lengths[field]:
                combined_tags.append(tags[field][indices[field]])
                indices[field] += 1

        return (tag_delimiter.join(combined_tags),)



class SplitSentences:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sentence": ("STRING", {"forceInput": True}),
                "length": ("INT", {"default": 1, "min": 1})
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")

    FUNCTION = "splitSentences"

    CATEGORY = "Naders Nodes"

    def splitSentences(self, sentence, length):
        # Split the sentence into a list of sentences
        sentences = re.split(r'(?<=[.!?])\s+', sentence)
        
        # If the number of sentences is less than 'length', try to return one sentence
        if len(sentences) < length:
            if len(sentences) >= 1:
                return (sentences[0], ' '.join(sentences[1:]))
            else:
                return (sentence, "")
        
        # Otherwise, return only the first 'length' sentences and the remaining sentences
        split_sentences1 = ' '.join(sentences[:length])
        split_sentences2 = ' '.join(sentences[length:])
        
        return (split_sentences1, split_sentences2)

class SplitTags:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tag_field": ("STRING", {"forceInput": True}),
                "tag_amount_to_split": ("INT", {"default": 1, "min": 1}),
                "tag_delimiter": ("STRING", {"default": ", "})
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")

    FUNCTION = "splitTags"

    CATEGORY = "Naders Nodes"

    def splitTags(self, tag_field, tag_amount_to_split, tag_delimiter):
        # Split the tag_field into a list of tags
        tags = tag_field.split(tag_delimiter)
        
        # If the number of tags is less than 'tag_amount', return the original tag_field and an empty string
        if len(tags) < tag_amount_to_split:
            return (tag_field, "")
        
        # Otherwise, return only the first 'tag_amount' tags and the removed tags
        split_tags1 = tag_delimiter.join(tags[:tag_amount_to_split])
        split_tags2 = tag_delimiter.join(tags[tag_amount_to_split:])
        
        return (split_tags1, split_tags2)


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
    CATEGORY = "Naders Nodes"

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

class TokenCounter:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("Token_COUNT_INT",)
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)    
    FUNCTION = "countTokens"
    CATEGORY = "Naders Nodes"

    def countTokens(self, input_string):
        # Split the string into tokens
        tokens = input_string.split()

        # Count the number of tokens
        token_count = len(tokens)

        return token_count,



NODE_CLASS_MAPPINGS = {
    "Tag Duplicate Remover": TagDuplicateRemover,
    "Tag Alternating Combiner": CombineAlternatingTags,
    "Split Sentences": SplitSentences,
    "Split Tags": SplitTags,
    "Load Text List": LoadTextList,
    "Token Counter": TokenCounter
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "Tag Duplicate Remover": "Tag Duplicates Remover",
    "Tag Alternating Combiner": "Tag Alternating Combiner",
    "Shorten Sentences": "Shorten Sentences",
    "Split Tags": "Split Tags",
    "Load Text List": "Load Text List",
    "Token Counter": "TokenCounter"
}

# Test the class
#tag_remover = TagDuplicateRemover()
#print(tag_remover.removeDuplicates("background, tree, pond, apple, tree, bird"))