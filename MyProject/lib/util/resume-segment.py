import fitz

EDUCATION_TITLES = ['education', 'academic background', 'education background']
WORK_EXP_TITLES = ['professional experience', 'experience', 'work experience']
SKILL_TITLES = ['skills', 'interests']
PROJECTS_TITLES = ['projects', 'project']
EXCO_TITLES = ['extracurricular', 'involvement', 'volunteer']

SECTION_TITLES = {'education': EDUCATION_TITLES,
                  'experience': WORK_EXP_TITLES,
                  'skill': SKILL_TITLES,
                  'project': PROJECTS_TITLES,
                  'exco': EXCO_TITLES
                  }

def scrape(filePath):
    results = [] # list of tuples that store the information as (text, font size, font name) 
    pdf = fitz.open(filePath) # filePath is a string that contains the path to the pdf
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
                        #     results.append((lines['text'].strip(), lines['size']lines['size'], lines['font']))
                        results.append(lines)
                        # results.append((i, lines['text']))
                            # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
            # results.append(block)
            i+=1
            
    pdf.close()
    return results

def is_heading(line):
    text = line['text'].strip()
    if text == '':
        return False
    elif len(text.split(" ")) > 3:
        return False
    elif "bold" not in line['font'].lower():
        return False
        
    return True

def get_section(heading):
    for titles in SECTION_TITLES:
        for title in SECTION_TITLES[titles]:
            if title in heading.lower():
                SECTION_TITLES.pop(titles) # remove section from lookup dict after a match to avoid redundancy
                return titles

def is_section_header(line):
    if is_heading(line):
        return (get_section(line['text'].strip()))
        

if __name__ == "__main__":
    openResume = r"C:\\Users\User\Desktop\Lecture Notes\Y3T2 Degree\FYP1\streamlit-project-template\MyProject\lib\openresume-resume.pdf"
    myResume = r"C:\Users\User\Desktop\Lecture Notes\Y3T2 Degree\FYP1\streamlit-project-template\MyProject\lib\Yaw Boon Zhe - Resume.pdf"
    resume = scrape(openResume)

    sections = {}
    for line in resume:
        section_type = is_section_header(line)
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
    for section in sections:
        print(section)
        print(sections[section])
        print()

    # print(sections)
                
    
    # scrape_html(myResume)
    # print(get_section("EDUCATION"))