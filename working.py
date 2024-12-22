import re 
import os
import yaml
import glob
import copy
import jinja2    
import pickle

folder_template = "templates"
file_template_default = os.path.join(folder_template, "oomlout_template_part_default.md.j2")
file_template_default_absolute = os.path.join(os.path.dirname(__file__), file_template_default)

cnt_manip  = 1

def main(**kwargs):
    
    folder = kwargs.get("folder", f"os.path.dirname(__file__)/parts")
    folder = folder.replace("\\","/")
    kwargs["folder_template"] = folder_template
    kwargs["file_template"] = file_template_default_absolute
    folder_template_absolute = os.path.join(os.path.dirname(__file__), folder_template)
    kwargs["folder_template_absolute"] = folder_template_absolute
    file_template_absolute = os.path.join(os.path.dirname(__file__), file_template_default)
    kwargs["file_template_absolute"] = file_template_absolute
    print(f"oomlout_oomp_utility_readme_generation for folder: {folder}")
    create_recursive(**kwargs)
    
def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    filter = kwargs.get("filter", "")
    count = 0

    mode = "semaphore"
    if mode == "semaphore":
        import threading
        semaphore = threading.Semaphore(1000)
        #semaphore = threading.Semaphore(1)
        threads = []

        def create_thread(**kwargs):
            with semaphore:
                create_recursive_thread(**kwargs)
        
        for item in os.listdir(folder):
            kwargs["item"] = item
            #thread = threading.Thread(target=create_thread, kwargs=copy.deepcopy(kwargs))
            thread = threading.Thread(target=create_thread, kwargs=pickle.loads(pickle.dumps(kwargs, -1)))  
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

def create_recursive_thread(**kwargs):   
    global cnt_manip 
    folder = kwargs.get("folder", "")
    item = kwargs.get("item", "")
    filter = kwargs.get("filter", "")
    item_absolute = os.path.join(folder, item)
    if filter in item:            
        if os.path.isdir(item_absolute):
            #if working.yaml exists in the folder
            if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                kwargs["directory"] = item_absolute
                manipulate_data(**kwargs)
                cnt_manip += 1
                if cnt_manip % 100 == 0:
                    print(f".", end="")

    

def manipulate_data(**kwargs):
    import os
    directory = kwargs.get("directory",os.getcwd())    
    file_template = kwargs.get("file_template", file_template_default_absolute)
    file_output = f"{directory}/readme.md"
    details = {}

    #      yaml part
    file_yaml = f"{directory}/working.yaml"
    details = {}
    if os.path.exists(file_yaml):
        with open(file_yaml, 'r') as stream:
            try:
                details = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:   
                print(exc)
    
    if details == None:
        print(f"error with file: {file_yaml}")
        return
    
    details["oomlout_oomp_utility_custom_data_manipulation"] = True

    oomp_id = details.get("id", "")
    md5_6_alpha = details.get("md5_6_alpha", "")



    details = add_link_label(details=details)
    details = add_oomlout_detail_hierarchy(details=details)
    #print 3x2 label link


    #add links in a list
    if True:
        links = ["link_main"]
        links.append("github_link")
        #links.append("distributor_amazon_link")        
        links_buy = []

        #add distributor links    
        distributors = ["orbital_fasteners","accu","amazon"]
        for distributor in distributors:
            #links.append(f"webpage_distributor_{distributor}")
            #links_buy.append(f"webpage_distributor_{distributor}")
            #links.append(f"distributor_{distributor}_link")
            links.append(f"link_distributor_{distributor}")
            links_buy.append(f"link_distributor_{distributor}")
        


        manufacturers = ["metalmate"]
        for manufacturer in manufacturers:
            links.append(f"webpage_manufacturer_{manufacturer}")

        #add in an itemized list
        count = 1
        for link in links:
            if link in details:
                details[f"link_{count}"] = details[link]
                details[f"link_{count}_name"] = link
                count += 1

        count = 1
        for link in links_buy:
            if link in details:
                details[f"link_buy_{count}"] = details[link]
                details[f"link_buy_{count}_name"] = link

                count += 1    
        
        if "distributor_current" in details:
            link = f"webpage_distributor_{details['distributor_current']}"
            details["link_buy"] = details[link]
            details["link_buy_name"] = link.replace("webpage_distributor_", "")

        #go        


    #add a price summary
    if True:
        #go through distribtors and populate price_distributor_1, price_distributor_2, etc
        qtys = [1, 100, 200, 1000, 10000]
        count = 1
        for distributor in distributors:        
            for qty in qtys:
                field_name = f"price_{qty}_distributor_{distributor}"
                if field_name in details:
                    price = details[field_name]
                    if price != "":
                        details[f"price_{qty}_distributor_{count}"] = price
            details[f"price_{count}_name"] = distributor
            count += 1
                        



    #save details to file
    if True:                        
        #print(f"saving details to file: {file_yaml}")
        with open(file_yaml, 'w') as outfile:
            yaml.dump(details, outfile, sort_keys=True)


    pass
def add_link_label(details):   
    md5_6_alpha = details.get("md5_6_alpha", "")
         
    details["link_oomlout_label_3x2"] = f"http://192.168.1.245:1112/?label=oomp%20{md5_6_alpha}"
    details["link_oomlout_label_3x2_oomp_table"] = f"http://192.168.1.107:1112/?label=oomp%20{md5_6_alpha}"
    details["link_oomlout_label_2x1"] = f"http://192.168.1.242:1112/?label=oomp%20{md5_6_alpha}"
    details["link_oomlout_label_6x4"] = f"http://192.168.1.55:1112/?label=oomp%20{md5_6_alpha}"

    return details

def add_oomlout_detail_hierarchy(details):
    details_in_order = []
    details_in_order.append("classification")
    details_in_order.append("type")
    details_in_order.append("size")
    details_in_order.append("color")
    details_in_order.append("description_main")
    details_in_order.append("description_extra")
    details_in_order.append("manufacturer")
    details_in_order.append("part_number")

    hierarchy_list = []
    count = 0
    for detail in details_in_order:
        if detail in details:
            test_detail = details.get(detail, "")
            if test_detail != "":
                if "github" not in hierarchy_list:
                    split_value = False
                    test_strings = []
                    test_strings.append(r'_mm_width')
                    test_strings.append(r'_mm_height')
                    test_strings.append(r'_mm_length')
                    test_strings.append(r'_diameter')
                    test_strings.append(r'_mm_depth')
                    test_strings.append(r'_gram')
                    for test_string in test_strings:
                        if test_string in test_detail:
                            #add a check for number before the string
                            test_string_re = rf"(\d+){test_string}"
                            match = re.search(test_string_re, test_detail)
                            if match:
                                value = match.group(0)
                                if value != "":
                                    #value = value.replace("_mm_", "")
                                    hierarchy_list.append(f"{value}")
                                    split_value = True
                if not split_value:
                    #LIST OF CHANGES
                    test_detail = test_detail.replace("screw_", "s")
                    hierarchy_list.append(test_detail)
                    count += 1              
                    


    hierarchy_list_new = []
    for item in hierarchy_list:
        #teardown ones
        split_list = []
        split_list.append("oomp_teardown")
        split_list.append("oobb_holder")
        split = False
        for split in split_list:
            if split in item:
                hierarchy_list_new.append(split)
                item = item.replace(f"{split}_", "").replace("oomlout_", "")
        
        #if more than 4 "_" then split                
        while item.count("_") > 4:
            items = item.split("_")
            first_four = f"{items[0]}_{items[1]}_{items[2]}_{items[3]}"
            hierarchy_list_new.append(first_four)
            item = item.replace(f"{first_four}_", "")            
        
        
        hierarchy_list_new.append(item)
    hierarchy_list = hierarchy_list_new

    
    count = 1
    for item in hierarchy_list:
        item = item.replace("oomlout_","")
        
        


        details[f"oomlout_detail_hierarchy_{count}"] = item
        details[f"oomlout_detail_hierarchy_{count}_upper"] = item.upper()
        details[f"oomlout_detail_hierarchy_{count}_upper_length_4"] = item.upper().replace("_MM_","")[:4]
        count += 1
    pass
    return details

if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    folder = "Z:\\oomlout_oomp_current_version_fast_test\\parts"
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    #folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    kwargs["folder"] = folder
    main(**kwargs)