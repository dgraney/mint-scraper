from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time
import sys
sys.path.append("..") 

# from Datatypes.Account import Account

class MintScraper():
    def __init__(self):
        self.driver = None
        self.mint_login_url='https://accounts.intuit.com/index.html?offering_id=Intuit.ifs.mint&namespace_id=50000026&redirect_url=https%3A%2F%2Fmint.intuit.com%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown%26ivid%3D8c25ea35-3c8f-41ff-ba6d-ad9a37d4ef4d'

    def connect(self,email=None,pwd=None):
        if email is None: email = input('Mint Email: ')
        if pwd is None: pwd = getpass.getpass('Mint Password: ')

        driver = webdriver.Chrome()
        driver.get(self.mint_login_url)
        driver.maximize_window()
        user_element = driver.find_element_by_id('ius-userid')
        password_element = driver.find_element_by_id('ius-password')
        user_element.send_keys(email)
        password_element.send_keys(pwd)
        password_element.submit()
        driver.implicitly_wait(10)
        time.sleep(10)
        self.driver = driver
        return self.driver

    def get_net_worth_data(self):
        # Assumes on main Mint Dashboard, already connected/logged in
        self._click_by_id('trend')
        self._click_by_id('views-0')
        self._click_by_id('show-more-less',sleep=3)
        
        data = self._get_csv_data()
        return data

    def get_all_account_history(self):
        self._click_by_id('trend')
        
        self._select_assets_over_time()
 
        accounts_references = []
        accounts_list_divs = self.driver.find_elements_by_id('acctddmenucategory')
        for ald in accounts_list_divs[:-1]: #Skip the random test one...
            for element in ald.find_elements_by_tag_name('li'):
                checkbox = element.find_element_by_tag_name('input')
                acct_source = element.find_element_by_tag_name('label').get_attribute("textContent")
                acct_name = element.find_element_by_class_name('description').get_attribute("textContent")

                if "All " in acct_source: continue
                accounts_references.append({
                    'cb':checkbox,
                    'source':acct_source,
                    'name':acct_name
                })
        
        print(accounts_references)

        datedropdown = self.driver.find_element_by_id('trends-datedropdown')
        all_time_li = datedropdown.find_elements_by_tag_name('li')[-1]
        self._click_element(all_time_li)

        # Uncheck all
        #self._click_by_id('show-more-less',sleep=3)
        for ref in accounts_references:
            self._click_element(ref['cb'],sleep=1)

        out = []
        for ref in accounts_references:
            # check the box
            self._click_element(ref['cb'],sleep=2)

            # get acct history
            data = self._get_csv_data()
            out.append({
                'source':ref['source'],
                'name':ref['name'],
                'data':data
            })

            # uncheck the box
            self._click_element(ref['cb'],sleep=1)
        
        return out
            
    def _get_csv_data(self):
        port_table = self.driver.find_element_by_id('csvForm')
        inputs = port_table.find_elements_by_tag_name('input')

        # headers = {}
        data = []
        headers = []
        for i,input in enumerate(inputs):
            if i == 0: 
                headers=input.get_attribute('value').split('~')
                continue
            data_dict = {}
            name = input.get_attribute('name')
            value = input.get_attribute('value')
            values = value.split('~')
            for i,header in enumerate(headers):
                print(i,header)
                if i !=0: 
                    data_dict[header] = self._acct_to_float(values[i])
                else:
                    data_dict[header] = values[i]
            data.append(data_dict)
        print(data)
        return data


    def _select_assets_over_time(self):
        # Select "Assets > Over Time"
        graph_selection_nav = self.driver.find_element_by_id('graphSelectionNav')

        asset_level = False
        for element in graph_selection_nav.find_elements_by_tag_name('a'):
            t = element.get_attribute("textContent")

            if 'Assets' in t: 
                self._click_element(element)
                asset_level = True

            if asset_level and 'Over Time' in t: 
                self._click_element(element)
                break

    def _click_by_id(self,id,sleep=5):
        self.driver.find_element_by_id(id).click()
        time.sleep(sleep)

    def _click_element(self,element,sleep=5):
        self.driver.execute_script("arguments[0].click();", element) 
        time.sleep(sleep)

    def _acct_to_float(self,s):
        for char in "$,()":
            s = s.replace(char,'')
        return float(s)
