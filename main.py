import selenium, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

teachersNo = dict()
teachersYes = dict()    
teachersBoth = set()

def letsgo(code, endhost, startvar, endvar):
    f = open("result.csv", "a") #creates a result.csv-file
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get("https://ilmonet.fi/#!code=A" + str(code)) 
    sys.stdout.write(str(code)+ "\n")
    teacher = ""
    link = ""
    hasLink = False
    try:
        elem = driver.find_elements_by_class_name("course-more-field")
        for e in elem:
            if "rare:" in e.text:
                teacher = e.text.split("re: ")[1]
                sys.stdout.write(e.text + "\n")
            if "arbismyrorna" in e.get_attribute('innerHTML'):
                hasLink = True
                sys.stdout.write(e.get_attribute('innerHTML').split('.fi/')[1].split('" target')[0] + "\n")
                link = e.get_attribute('innerHTML').split('.fi/')[1].split('" target')[0]
        if hasLink:
            if teacher in teachersYes.keys():
                teachersYes[teacher].append(str(code) + ": " + str(link))
            else:
                teachersYes[teacher] = []
                teachersYes[teacher].append(str(code) + ": " + str(link))
            if teacher in teachersNo:
                teachersBoth.add(teacher)
                link = link + " NB check earlier"
        else:
            if teacher not in teachersNo.keys():
                teachersNo[teacher] = []
            teachersNo[teacher].append(code)
            if teacher in teachersYes.keys():
                teachersBoth.add(teacher)
                link = "NB missing?"
    except Exception as e:
        sys.stdout.write(str(e))
    sys.stdout.flush()
    driver.close()
    f.write(str(code) + "\t " + teacher + "\t " + link + "\n")
    if code == endhost:
        letsgo(startvar, endhost, startvar, endvar)
    elif code < endvar:
        f.close()
        letsgo (code+1, endhost, startvar, endvar)
    else:
        f.close()
        sys.stdout.flush()
        return

code = int(input("Startcode: \n"))
endhost =int(input("Last code for the autumn: \n"))
startvar = int(input("First code for the spring: \n"))
endvar = int(input("Last code for the spring: \n"))
print("Thank you.")
sys.stdout.flush()
letsgo(code, endhost, startvar, endvar)
