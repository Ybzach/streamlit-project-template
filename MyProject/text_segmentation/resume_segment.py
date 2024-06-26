import fitz
import math

EDUCATION_TITLES = ['education', 'academic background', 'education background']
WORK_EXP_TITLES = ['professional experience', 'experience', 'work experience']
SKILL_TITLES = ['skills', 'interests']
PROJECTS_TITLES = ['projects', 'project']
EXCO_TITLES = ['extracurricular', 'involvement', 'volunteer']

class resumeSegmenter:
    def __init__(self):
        self.results = {}
        self.section_titles = {
                            'EDUCATION': EDUCATION_TITLES,
                            'EXPERIENCE': WORK_EXP_TITLES,
                            'SKILL': SKILL_TITLES,
                            'PROJECT': PROJECTS_TITLES,
                            'INVOLVEMENTS': EXCO_TITLES
                        }

    def scrape(self, resume):
        scraped = [] # list of tuples that store the information as (text, font size, font name) 
        resume.seek(0,0)
        pdf = fitz.open(stream=resume.read(), filetype="pdf")
        for page in pdf:
            dict = page.get_text("dict")
            blocks = dict["blocks"]
            i = 1
            for block in blocks:
                if "lines" in block.keys():
                    spans = block['lines']
                    for span in spans:
                        data = span['spans']
                        for lines in data:
                            scraped.append(lines)
                i+=1
                
        pdf.close()
        return scraped

    def is_heading(self, line, average_font_size):
        text = line['text'].strip()
        line_font_size = math.floor(line['size'])
        if text == '':
            return False
        elif len(text.split(" ")) > 3:
            return False
        elif "bold" not in line['font'].lower() and line_font_size <= average_font_size:
            return False
            
        return True

    def get_section(self, heading):
        for titles in self.section_titles:
            for title in self.section_titles[titles]:
                if title in heading.lower():
                    self.section_titles.pop(titles) # remove section from lookup dict after a match to avoid redundancy
                    return titles

    def get_average_font_size(self, resume):
        font_sizes = {}
        pass
        for line in resume:
            line_font_size = math.floor(line['size'])
            if line_font_size in font_sizes:
                font_sizes[line_font_size] += 1
            else:
                font_sizes[line_font_size] = 1

            most_frequent_font_size = max(font_sizes, key=font_sizes.get)
        return most_frequent_font_size

    def is_section_header(self, line, average_font_size):
        if self.is_heading(line,  average_font_size):
            return (self.get_section(line['text'].strip()))
            
    def segment(self, resume):
        resume = self.scrape(resume)
        average_font_size = self.get_average_font_size(resume)
        sections = {}
        for line in resume:
            section_type = self.is_section_header(line, average_font_size)
            # print(sections)
            if section_type != None:
                sections[section_type] = ''
                continue
            elif len(sections) <= 0: # skip headings that are at top of resume, but not in a section that we look for
                continue
            else:
                section_head, section_content = sections.popitem()
                sections[section_head] = section_content + line['text'].strip() + ' '
        self.results = sections
        return sections
