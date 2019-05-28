"""
 Created by hanruida on 2019-03-23
"""
import codecs
import json


class Handler:

    @classmethod
    def combine_data(cls):
        new_list = []
        compare_before_list = json.loads(cls.read_json())
        for item in compare_before_list:
            if not new_list:
                new_list.append({
                    "batch_no": item["batch_no"],
                    "address": item["address"],
                    "info": [
                        {
                            "long": item["poi_long"],
                            "short": item["poi_short"],
                            "batch_name": item["batch_name"],
                            "desc": item["desc"]
                        }
                    ]
                })
            else:
                flag = False
                i = None
                for index in range(0, len(new_list)):
                    if item["batch_no"] == new_list[index]["batch_no"]:
                        flag = True
                        i = index
                if  flag:
                    flag1 = False
                    for info in new_list[i]["info"]:
                        if item["batch_name"] == info["batch_name"]:
                            flag1 = True
                    if not flag1:
                        new_list[i]["info"].append({
                            "long": item["poi_long"],
                            "short": item["poi_short"],
                            "batch_name": item["batch_name"],
                            "desc": item["desc"]
                        })
                else:
                    new_list.append({
                        "batch_no": item["batch_no"],
                        "address": item["address"],
                        "info": [
                            {
                                "long": item["poi_long"],
                                "short": item["poi_short"],
                                "batch_name": item["batch_name"],
                                "desc": item["desc"]
                            }
                        ]
                    })
        return new_list
        # print(json.dumps(new_list))
    @staticmethod
    def read_json():
        with codecs.open("target/gps.json", 'rb', encoding="utf8") as f:
            return f.read()

# Handler.combine_data()