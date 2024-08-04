import os
import re
import shutil

from utils import FilesUtil
import pandas as pd

'''
做数据转换工作
输出全部存于data目录下
转换后的json数据存于data_tmp目录下
'''

    
def get_all_data_to_csv(data_dir, csv_file):
    '''
    将数据转换为csv文件
    需要的字段
    职位名称：positionName
    职位类型：positionType
    工作地点：workLocation
    薪资：salary
    经验要求：experienceRequirements
    学历要求：educationRequirements
    '''
    json_files = os.listdir(data_dir)
    all_data = []
    for file in json_files:
        if not file.endswith(".json"):
            continue
        data = FilesUtil.get_data_from_file(os.path.join(data_dir, file))
        for page_data in data:
            job_list = page_data["zpData"]["jobList"]
            for job in job_list:
                positionName = job["jobName"]
                try:
                    positionType = file.split("\\")[-1].split("_")[0]
                except:
                    positionType = file.split("/")[-1].split("_")[0]
                workLocation = job["areaDistrict"]
                if workLocation == "":
                    workLocation = job["cityName"]
                salary = job["salaryDesc"]
                if salary.find("元") >= 0:
                    salary = salary.split("元")[0]
                if salary.lower().find("k") >= 0:
                    salary_1 = salary.lower().split("k")[0]   
                    if salary.find("-") >= 0:
                        salary_s = int(salary_1.split("-")[0]) * 1000
                        salary_e = int(salary_1.split("-")[-1]) * 1000
                        salary = f"{salary_s}-{salary_e}"
                    else:
                        salary = f"{salary_1*1000}"
                labels = job["jobLabels"]
                try:
                    experienceRequirements, educationRequirements = labels
                except:
                    print("获取不到工作经验和学历要求:", labels)
                    experienceRequirements = job["jobExperience"]
                    educationRequirements = job["jobDegree"]
                row_data = [positionName, positionType, workLocation, salary, experienceRequirements, educationRequirements]
                all_data.append(row_data)
    df = pd.DataFrame(all_data, columns=["positionName", "positionType", "workLocation", "salary", "experienceRequirements", "educationRequirements"])
    FilesUtil.write_data_to_file(csv_file, df)


def get_data_by_position_type(data):
    '''
    根据编程语言类型进行分类计数, 条形图
    '''
    type_count = data.groupby("positionType").count()["positionName"]
    name_list = []
    num_list = []
    for i in type_count.index:
        name_list.append(i)
        num_list.append(int(type_count[i]))
    data_dict = {"name": name_list, "value": num_list}
    # print(data_dict)
    FilesUtil.write_data_to_file("data_tmp/position_type.json", data_dict)


def get_data_by_workLocation(data):
    '''
    根据工作地点进行分类计数, 饼图
    '''
    location_count = data.groupby("workLocation").count()
    name_list = []
    num_list = []
    for i in location_count.index:
        name_list.append(i)
        num_list.append(int(location_count.loc[i]["positionName"]))
    data_dict = {"name": name_list, "value": num_list}
    # print(data_dict)
    FilesUtil.write_data_to_file("data_tmp/work_location.json", data_dict)


def get_data_by_salary(data):
    '''
    根据岗位平均薪资进行分类计数, 折线图
    '''
    data["avg_salary"] = data["salary"].apply(
                        lambda x: (int(re.findall(r'\d+', x.split("-")[0])[0]) + int(re.findall(r'\d+', x.split("-")[-1])[0])) / 2 
                                if x.split("K")[0].find("-") >= 0
                                else int(re.findall(r'\d+', x)[0])
    )
    if 1 == 1: # 岗位平均薪资分类计数
        avg_salary_postionType = round(data.groupby("positionType").mean("avg_salary"), 2)
        data_dict = {"name": list(avg_salary_postionType.index), "value": list(avg_salary_postionType["avg_salary"])}
        # print(data_dict)
        FilesUtil.write_data_to_file("data_tmp/avg_salary_by_positionType.json", data_dict)
    if 1 == 1: # 地区平均工资计数
        salary_sum = round(data.groupby("workLocation").mean("avg_salary"),2)
        data_dict = {"name": list(salary_sum.index), "value": list(salary_sum["avg_salary"])}
        FilesUtil.write_data_to_file("data_tmp/avg_salary_by_workLocation.json", data_dict)

    if 1 == 1: # 经验平均薪资分类计数
        avg_salary_experience = round(data.groupby("experienceRequirements").mean("avg_salary"), 2).sort_values(by="avg_salary")
        data_dict = {"name": list(avg_salary_experience.index), "value": list(avg_salary_experience["avg_salary"])}
        # print(data_dict)
        FilesUtil.write_data_to_file("data_tmp/avg_salary_by_experience.json", data_dict)

    if 1 == 1: # 学历平均薪资分类计数
        avg_salary_education = round(data.groupby("educationRequirements").mean("avg_salary"), 2).sort_values(by="avg_salary")
        data_dict = {"name": list(avg_salary_education.index), "value": list(avg_salary_education["avg_salary"])}
        # print(data_dict)
        FilesUtil.write_data_to_file("data_tmp/avg_salary_by_education.json", data_dict)

def get_data_by_experience(data):
    '''
    根据工作经验要求进行分类计数, 折线图
    '''
    experience_count = data.groupby("experienceRequirements").count()
    name_list = []
    num_list = []
    for i in experience_count.index:
        name_list.append(i)
        num_list.append(int(experience_count.loc[i]["positionName"]))
    data_dict = {"name": name_list, "value": num_list}
    # print(data_dict)
    FilesUtil.write_data_to_file("data_tmp/experience.json", data_dict)


def get_all_data_to_json(data):

    '''
    将数据转换为json文件
    '''
    # data_dict = data.to_dict(orient="records")
    data_dict = {}
    for k in data.columns:
        data_dict[k] = list(data[k])
    FilesUtil.write_data_to_file("data_tmp/all_data.json", data_dict)


def tranform_data_to_json():
    '''
    将需要展示的数据分别进行计算，并转换为json文件
    '''
    data = pd.read_csv(r"data/all_data.csv")
    if os.path.exists("data_tmp"):
        shutil.rmtree("data_tmp")
    os.makedirs("data_tmp",exist_ok=True)

    # 职位类型分类计数
    get_data_by_position_type(data)
    # 工作地点分类计数
    get_data_by_workLocation(data)
    # 岗位平均薪资分类计数
    get_data_by_salary(data)
    # 工作经验要求分类计数
    get_data_by_experience(data)
    # 所有数据转换为json文件
    get_all_data_to_json(data)


if __name__ == '__main__':
    # data_dir = "data"
    # csv_file = f"{data_dir}/all_data.csv"
    # get_all_data_to_csv(data_dir, csv_file)
    tranform_data_to_json()
