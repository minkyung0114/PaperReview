import json
import xmltodict
import os
data_path = r"C:\Users\Administrator\Desktop\경기대ORING자료"
data_path = data_path.replace("\\","/")

xml_path = os.listdir(data_path)


for file in xml_path:



    #json_path = file.replace(".xml",",json")
    #json_path = os.path.join(data_path, json_path)


    if file.endswith(".xml"):
        xml_file = os.path.join(data_path,file)
        xml_file = xml_file.replace("\\","/")
        #print(f"xml_file:{xml_file}")
        json_file = xml_file.replace(".xml",".json")

        with open(xml_file, encoding='utf-8') as f:
            doc = xmltodict.parse(f.read())
            #print(f"doc:{doc}")

            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(doc, file, indent="\t")


        '''
        json_data = json.loads(json.dumps(doc))
        print(json_data)
        '''
