import os
import yaml
import glob
import copy
import jinja2    

folder_template = "templates"
file_template_default = os.path.join(folder_template, "oomlout_template_part_default.md.j2")
file_template_default_absolute = os.path.join(os.path.dirname(__file__), file_template_default)

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
    create_readme_recursive(**kwargs)
    
def create_readme_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    filter = kwargs.get("filter", "")
    count = 0
    for item in os.listdir(folder):
        item_absolute = os.path.join(folder, item)
        if filter in item:            
            if os.path.isdir(item_absolute):
                #if working.yaml exists in the folder
                if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                    kwargs["directory"] = item_absolute
                    manipulate_data(**kwargs)
                    count += 1
                    if count % 100 == 0:
                        print(f"count: {count}")

    

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
    
    
    details["oomlout_oomp_utility_custom_data_manipulation"] = True

    oomp_id = details.get("id", "")
    md5_6_alpha = details.get("md5_6_alpha", "")

    #print 3x2 label link
    if True:
        details["link_oomlout_label_3x2"] = f"http://192.168.1.245:1112/?label=oomp%20{md5_6_alpha}"
        details["link_oomlout_label_2x1"] = f"http://192.168.1.242:1112/?label=oomp%20{md5_6_alpha}"
        details["link_oomlout_label_6x4"] = f"http://192.168.1.55:1112/?label=oomp%20{md5_6_alpha}"

    #add links in a list
    if True:
        links = ["link_main"]
        links.append("github_link")
        links_buy = []

        #add distributor links    
        distributors = ["orbital_fasteners","accu"]
        for distributor in distributors:
            links.append(f"webpage_distributor_{distributor}")
            links_buy.append(f"webpage_distributor_{distributor}")
        
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
                        details[f"price_{qty}_name"] = distributor
                        



    #save details to file
    if True:                        
        print(f"saving details to file: {file_yaml}")
        with open(file_yaml, 'w') as outfile:
            yaml.dump(details, outfile, sort_keys=True)

    pass


if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    folder = "Z:\\oomlout_oomp_current_version_fast_test\\parts"
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    #folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    kwargs["folder"] = folder
    main(**kwargs)