#!/usr/bin/env python
# coding: utf-8

# # Leetcode Downloader
# 
# The following code downloads all your leetcode submissions (i.e Accepted, Wrong answers, Time Limit Exceeded, Run time error and Compiler error submissions) using Selenium for webscraping (just as in <a href="https://github.com/dhananjay1210/Leetcode-Downloader">here</a>.) and Python modules for computations and storage. 
# 
# ### 1. Do necessary Imports

# In[ ]:


# Imports
import os
from time import sleep
import errno
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# ### 2. Create necessary Maps 

# In[ ]:


os_dir_appender = {"windows" : '\\', "linux" : '/', "mac" : "/"}
status_dict = {"Accepted":0,
               "Wrong Answer":1,
               "Time Limit Exceeded":2,
               "Runtime Error":3,
               "Compile Error":4,
               "Memory Limit Exceeded":5}
extention_of = {"cpp" : ".cpp",
                "java" : ".java",
                "python" : ".py",
                "python3" : ".py",
                "c" : ".c",
                "csharp" : ".cs",
                "javascript" : ".js",
                "ruby" : ".ruby",
                "swift" : ".swift",
                "golang" : ".go",
                "scala" : ".scala",
                "kotlin" : ".kt",
                "rust" : ".rs",
                "mysql" : ".sql"}


# ### 3. Create Necessary directories in current directory 

# In[ ]:


print()
print()
print("************************************************************************")
print("************************************************************************")
print("*******                                                          *******")
print("*******              Welcome to Leetcode Downloader              *******")
print("*******                                                          *******")
print("************************************************************************")
print("************************************************************************")
print()
print()

# Input user's root path
root_path = os.getcwd()

# Input OS
user_os = ""
if sys.platform.startswith('linux'):
    user_os = 'linux'
elif sys.platform.startswith('darwin'):
    user_os = 'mac'
elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    user_os = 'windows'
if root_path[-1] not in os_dir_appender.values():
	root_path += os_dir_appender[user_os]
# Create directories
print("Creating necessary directories/files... ")
types_of_submissions = len(status_dict)

# Directory where your leetcode submission will be saved
code = root_path + "codes" + os_dir_appender[user_os]

# Directory where your leetcode submission links will be saved
code_links = root_path + "code_links" + os_dir_appender[user_os]

# Default Directory for chrome downloads
download_default_directory = root_path + "chrome_download" + os_dir_appender[user_os]

all_file_dir, all_file_list = ['' for _ in range(types_of_submissions)],['' for _ in range(types_of_submissions)]
for key,val in status_dict.items():
    key = key.replace(' ','_').lower()
    all_file_dir[val] = code + key + '_codes' + os_dir_appender[user_os]
    all_file_list[val] = key + '_code_link.txt'
    
dirs = [code, code_links, download_default_directory]
all_submission_links = [set() for _ in range(types_of_submissions)]
new_submissions = ['' for _ in range(types_of_submissions)]

for direc in dirs+all_file_dir:
    try:
        os.makedirs(direc)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
for idx,file in enumerate(all_file_list):
    file_path = code_links + file
    try:
        with open(file_path,'r') as f:
            links = (f.readlines())
            all_submission_links[idx] = set(map(lambda x: x.strip(),links))
    except IOError:
        with open(file_path,'w') as f:
            pass
      
print("Created necessary directories/files.")
print()


# ### 4. Login to your leetcode using Selenium & Chrome driver

# In[ ]:


# Leetcode acc_type,username, password
print("Leetcode account details. Username,password are case/whitespace sensitive.")
acc_type = ""
retry = 0
while retry < 5:
	print("Choose one of the login methods : leetcode/google")
	print()
	print("Enter account type : ",end = "")
	acc_type = input().strip().lower()
	if (acc_type not in ["leetcode","linkedin","google","github","facebook"]):
		print("Invalid account type")
		print()
		retry += 1
	else:
		print()
		print("Enter " + acc_type + " username : ",end = "")
		username = input()
		print("Enter " + acc_type + " password : ",end = "")
		pwd = input()
		break
if retry == 5:
	print()
	print("Maximum attempt reached.")
	print("You entered invalid account type...")
	print("Exiting...")
	sys.exit()
print()

#selenium configurations
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_default_directory,"safebrowsing.enabled": "false"}
chromeOptions.add_experimental_option("prefs",prefs)
if user_os == "windows":
	chromedriver = root_path + "chromedriver.exe"
else:
	chromedriver = root_path + "chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)


#user agent configurations
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'
print()

# Load website
driver.get("https://leetcode.com/accounts/login/")
sleep(3)
print("Website loaded")
print()


# Login to leetcode
if acc_type == "leetcode":
	already_present = driver.find_element_by_name("login").get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_name("login").send_keys(Keys.BACKSPACE);

	# user name will be entered
	driver.find_element_by_name("login").send_keys(username)
	sleep(1)

	# To Clear password field
	already_present = driver.find_element_by_name("password").get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_name("password").send_keys(Keys.BACKSPACE);

	# password will be entered
	driver.find_element_by_name("password").send_keys(pwd)
	sleep(1)

	driver.find_element_by_xpath("//button[@class='btn__2FMG fancy-btn__CYhs primary__3S2m light__3zR9 btn__1eiM btn-md__3VAX ']").click()
	# You may increase below timer to 10 if you have slow internet connection.
	sleep(5)
	
	try:
		err_msg = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p").text
		if "CAPTCHA" in err_msg:
			print("If captcha issue persist then connect to the VPN and rerun the code")
			print("                              OR                                   ")
			print("ENTER THE CAPTCHA AND THEN PRESS 'y' KEY FOLLOWED BY ENTER TO PROCEED : ",end = "")
			input()
			print()
			driver.find_element_by_xpath("//button[@class='btn__2FMG fancy-btn__CYhs primary__3S2m light__3zR9 btn__1eiM btn-md__3VAX ']").click()
			# You may increase below timer to 10 if you have slow internet connection.
			sleep(5)
			err_msg = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p").text
		if "username" in err_msg:
			print()
			print("Wrong username and/or password")
			print("Exiting...")
			print()
			sys.exit()
	except Exception as e:
		print("Login Successful")
		print()
		# You may increase below timer to 10 if you have slow internet connection.
		sleep(5)

elif acc_type == "google":
	driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/a[2]").click()
	sleep(5)
	google_username_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
	already_present = driver.find_element_by_xpath(google_username_xpath).get_attribute('value')
	for i in range(len(already_present)+1):
		driver.find_element_by_xpath(google_username_xpath).send_keys(Keys.BACKSPACE);
	# user name will be entered
	driver.find_element_by_xpath(google_username_xpath).send_keys(username)
	sleep(1)
	google_username_next_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div"
	driver.find_element_by_xpath(google_username_next_xpath).click()
	sleep(5)
	try:
		# If error occurs, then exit
		goole_uname_err_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[2]/div[2]/div/span"
		err_mes = driver.find_element_by_xpath(goole_uname_err_xpath).text
		if "Couldn't find" in err_mes:
			print("You entered wrong username.")
		else:
			print("Some error occured. Try after some time.")
		print("Exiting...")
		sys.exit()
	except Exception as e:
		# If username is correct then only proceed
		google_password_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
		already_present = driver.find_element_by_xpath(google_password_xpath).get_attribute('value')
		for i in range(len(already_present)+1):
			driver.find_element_by_xpath(google_password_xpath).send_keys(Keys.BACKSPACE);
		# password will be entered
		driver.find_element_by_xpath(google_password_xpath).send_keys(pwd)
		sleep(1)
		google_password_next_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div"
		driver.find_element_by_xpath(google_password_next_xpath).click()
		# You may increase below timer to 10 if you have slow internet connection.
		sleep(5)
		
		try:
			# If error occurs, then exit
			goole_err_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[2]/div[2]/span"
			err_mes = driver.find_element_by_xpath(goole_err_xpath).text
			if "Wrong password" in err_mes:
				print("You entered wrong password")
			else:
				print("Some error occured. Try after some time.")
			print("Exiting...")
			sys.exit()
		except Exception as e:
			# If password is correct then only proceed.
			# You may increase below timer to 10 if you have slow internet connection.
			sleep(5)
			
	
	
	print("Login Successful")
	print()
	# You may increase below timer to 10 if you have slow internet connection.
	sleep(5)


# ### 5. Download all the submission links from your leetcode  

# In[ ]:


leetcode_submission_link = "https://leetcode.com/submissions/" 
driver.get(leetcode_submission_link)
sleep(3)
print("Webpage for all submission loaded.")
print()

try:
	if driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/h4").text:
		print("Submission links loaded successfully...")
		print()
except Exception as e:
	print("Login attempt failed. Please try again.")
	print("Exiting...")
	sys.exit()

print("Downloading links of submission...")

while(True):
    for row in driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div/table/tbody/tr"):
        third_row_value = row.find_elements(By.TAG_NAME, "td")[2]               # get status column value from table
        status = third_row_value.find_elements(By.TAG_NAME, "strong")[0].text   # extract status from strong field
        submission_link = third_row_value.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
        
        if status in status_dict:
            idx = status_dict[status]
            if submission_link not in all_submission_links[idx]:
                new_submissions[idx] += submission_link + '\n'
        
    try:
        # Load next submission page
        next_page = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div/nav/ul/li[2]")[0].find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
        print("Loading next page...",next_page)
        driver.get(next_page)
        # You may increase below timer to 6 if you have slow internet connection.
        sleep(3)
    except Exception as e:
        # If this is last submission page, then exit
        print("Next page not available.")
        print()
    break
# print(new_submissions)        
for idx,link in enumerate(new_submissions):
    with open(code_links + all_file_list[idx],'a') as f:
        new_submissions[idx] = new_submissions[idx].strip()
        f.writelines(new_submissions[idx])
#         f.writelines('\n')
print("All submission link saved in folder : ",code_links)
print()


# ### 6. Download the codes from the submission links 

# In[ ]:


print("Downloading your codes...")
for i in range(len(all_file_list)):
    file_name = all_file_list[i]
    file_dir = all_file_dir[i]
    links = []
    cnt = 0
    if new_submissions[i]:
        links = new_submissions[i].split('\n')
#     print('links: ',links)
    for submission_link in links:
        sub_id = submission_link.split("/")[-2]
#         print('subid:',sub_id)
        driver.get(submission_link)

        # Increase this timer to 8 if you have slow internet connection
        sleep(6)
        if len(driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/h4/a")) > 0:
            prog_name = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/h4/a")[0].text

            for invd in ['?','/','\\',':','*','<','>','|','"']:
                if invd in prog_name:
                    prog_name = prog_name.replace(invd, "")
            code_in_list = []
            code_lines = driver.find_elements_by_class_name("ace_line")
            prog_lang = driver.find_elements_by_id("result_language")[0].text.strip()
            
            #create directory
            try:
                os.makedirs(file_dir + prog_name.replace(' ','_'))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            # create file
            file_path = file_dir + prog_name.replace(' ','_') + os_dir_appender[user_os] + prog_name + "_" + str(sub_id) + extention_of[prog_lang]
            with open(file_path , 'w') as f2:
                pass

            # write code
            with open(file_path, 'a') as f2:
                for line in code_lines:
                    f2.writelines(line.text)
                    f2.writelines("\n")
        cnt += 1
    print(str(cnt) + " " + file_name.split('.')[0] + " downloaded." )

print()
print("All codes downloaded in folder : ",code)	 
driver.close()

