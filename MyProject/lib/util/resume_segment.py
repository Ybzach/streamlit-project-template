import fitz

EDUCATION_TITLES = ['education', 'academic background', 'education background']
WORK_EXP_TITLES = ['professional experience', 'experience', 'work experience']
SKILL_TITLES = ['skills', 'interests']
PROJECTS_TITLES = ['projects', 'project']
EXCO_TITLES = ['extracurricular', 'involvement', 'volunteer']

class resumeSegmenter:

    def __init__(self):
        self.results = {}
        self.section_titles = {
                            'education': EDUCATION_TITLES,
                            'experience': WORK_EXP_TITLES,
                            'skill': SKILL_TITLES,
                            'project': PROJECTS_TITLES,
                            'exco': EXCO_TITLES
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
                            # if (lines['text'].strip() != ''): # only store font information of a specific keyword
                            #     scraped.append((lines['text'].strip(), lines['size']lines['size'], lines['font']))
                            scraped.append(lines)
                            # scraped.append((i, lines['text']))
                                # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
                # scraped.append(block)
                i+=1
                
        pdf.close()
        return scraped

    def is_heading(self, line):
        text = line['text'].strip()
        if text == '':
            return False
        elif len(text.split(" ")) > 3:
            return False
        elif "bold" not in line['font'].lower():
            return False
            
        return True

    def get_section(self, heading):
        for titles in self.section_titles:
            for title in self.section_titles[titles]:
                if title in heading.lower():
                    self.section_titles.pop(titles) # remove section from lookup dict after a match to avoid redundancy
                    return titles

    def is_section_header(self, line):
        if self.is_heading(line):
            return (self.get_section(line['text'].strip()))
            
    def segment(self, resume):
        resume = self.scrape(resume)

        sections = {}
        for line in resume:
            section_type = self.is_section_header(line)
            # print(line)
            # print(sections)
            if section_type != None:
                sections[section_type] = ''
                continue
            elif len(sections) <= 0: # skip headings that are at top of resume, but not in a section that we look for
                continue
            else:
                section_head, section_content = sections.popitem()
                sections[section_head] = section_content + line['text'].strip() + ' '
                # print("sections: ", sections)
        self.results = sections


if __name__ == "__main__":
    openResume = r"D:\FYP1\streamlit-project-template\MyProject\lib\openresume-resume.pdf"
    myResume = r"D:\FYP1\streamlit-project-template\MyProject\lib\Yaw Boon Zhe - Resume.pdf"
    # resume = scrape(openResume)

    segmenter = resumeSegmenter(myResume)
    segment_results = segmenter.results
    for section in segment_results:
        print(section)
        print(segment_results[section])
        print()

    # print(sections)
                
    
    # scrape_html(myResume)
    # print(get_section("EDUCATION"))