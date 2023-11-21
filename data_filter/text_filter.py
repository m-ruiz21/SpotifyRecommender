import emoji
import string
import re

#TODO

class Filter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def over20PercentPunc(self, inputString):
        punctuation_set = set(string.punctuation)
        punctuation_count = sum(1 for char in inputString if char in punctuation_set)
        return (punctuation_count / len(inputString) * 100) > 20

    def process_text(self):
        with open(self.input_file, 'r', encoding='utf-8') as file:
            text = file.readlines()

        phrases_to_omit = ["http", ".com"]

        filtered_lines = []
        for line in text:
            # Remove lines containing junk punctuation
            if not self.over20PercentPunc(line):
                # Remove lines containing emojis
                if (emoji.emoji_count(line) == 0):
                    #Remove links
                    foundLink = False
                    for index, phrase in enumerate(phrases_to_omit):
                        if not re.search(phrase, line):
                            if (index == len(phrases_to_omit) - 1) and not foundLink:
                                filtered_lines.append(line)

        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.writelines(filtered_lines)

if __name__ == "__main__":
    input_descriptions = "descriptions.txt"  
    output_descriptions = "filtered_descriptions.txt"  

    input_titles = "full_title.txt"
    output_titles = "filtered_title.txt"

    textFilter = Filter(input_descriptions, output_descriptions)
    textFilter.process_text()

    textFilter2 = Filter(input_titles, output_titles)
    textFilter2.process_text()

    print(f"Filtering completed. Result saved")