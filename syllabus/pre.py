"""
Pre-process a syllabus (class schedule) file. 
"""
import arrow
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)



def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = { }
    cooked = [ ]

    base = arrow.now()
    current_time = base

    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0]=="#" :
            log.debug("Skipping")
            continue
        parts = line.split(':')
        #print(parts)
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:# base is begin date
                base = arrow.get(content, "MM/DD/YYYY")
                current_time = base
                print("Base date {}".format(base.isoformat()))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:# entry has some content
                cooked.append(entry) # finish a week, cooked :)
                entry = { }

            week_num = int(content)
            current_time = base.shift(weeks = +(week_num - 1))

            entry['topic'] = "" # reset entry
            entry['project'] = ""
            entry['week'] = "<mark>" + content + r"</mark>" + "\n" + str(current_time.date())


        elif field == 'topic' or field == 'project': # begining of new content
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry: # just in case
        cooked.append(entry)

    return cooked


def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
