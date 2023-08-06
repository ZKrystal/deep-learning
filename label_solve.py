import json
import os
import shutil

from PIL import Image


def get_labels(txt_folder_path):
    # 创建空字典来存储标签类别及其出现的次数
    label_counts = {}
    # 遍历文件夹内所有txt文件
    for file_name in os.listdir(txt_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(txt_folder_path, file_name)

            # 打开Yolo数据集txt格式的文件
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 统计标签类别出现的次数
            for line in lines:
                label = line.split(' ')[0]
                if label not in label_counts:
                    label_counts[label] = 1
                else:
                    label_counts[label] += 1
    # 输出每个标签类别及其出现的次数
    # for label, count in label_counts.items():
    #     print(f"{label}: {count} times")
    # # 返回标签类别及其出现次数的字典
    return label_counts


def delete_labels(labels, txt_folder_path):
    # 遍历文件夹内所有txt文件
    for file_name in os.listdir(txt_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(txt_folder_path, file_name)

            # 打开Yolo数据集txt格式的文件
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 删除指定标签类别
            new_lines = []
            for line in lines:
                if line.split(' ')[0] not in labels:
                    new_lines.append(line)

            # 保存修改后的文件
            with open(file_path, 'w') as f:
                f.writelines(new_lines)

            print(f"{labels}已被删除：{file_path}")


def transform(root_dir, img_file, out_file):
    input_folder = os.path.join(root_dir, img_file)
    output_folder = os.path.join(root_dir, out_file)
    # 循环遍历原始图片文件夹中的所有jpg图片
    num = 0
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            # 打开jpg图片文件
            img = Image.open(os.path.join(input_folder, filename))
            # 生成输出png图片的文件名
            output_filename = os.path.splitext(filename)[0] + '.tif'

            # 保存png图片到输出图片文件夹
            # os.remove(os.path.join(input_folder, filename))
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            img.save(os.path.join(output_folder, output_filename))
            num = num + 1
            print("{}转化成功".format(os.path.splitext(filename)), num)


def replace_label(label_map, label_dir):
    # 遍历标签文件夹中的所有文件
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            # 打开文件并读取所有行
            with open(os.path.join(label_dir, filename), 'r') as f:
                lines = f.readlines()

            # 遍历所有行并替换旧标签为新标签
            new_lines = []
            for line in lines:
                label = line.split(' ')[0]
                if label in label_map:
                    new_label = label_map[label]
                    new_line = new_label + line[len(label):]
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)

            # 将新标签写入文件
            with open(os.path.join(label_dir, filename), 'w') as f:
                f.writelines(new_lines)


def extract_label(labels_dir, images_dir, output_dir, output_dir_label, wanted_classes):
    if not os.path.isdir(output_dir): os.makedirs(output_dir)
    if not os.path.isdir(output_dir_label): os.makedirs(output_dir_label)
    # 遍历label文件夹中的所有文件
    for filename in os.listdir(labels_dir):
        # 读取label文件内容
        with open(os.path.join(labels_dir, filename), 'r') as f:
            lines = f.readlines()

        # 获取图片文件名和路径
        image_filename = os.path.splitext(filename)[0] + '.jpg'
        image_path = os.path.join(images_dir, image_filename)

        # 检查label文件中的每个物体
        for line in lines:
            # 分割字符串，获取物体的类别
            class_name = line.split()[0]

            # 如果这个类别是我们要提取的类别之一
            if class_name in wanted_classes:
                # 将图片文件复制到输出文件夹
                shutil.copy(image_path, os.path.join(output_dir, image_filename))

                # 将label文件复制到输出文件夹
                shutil.copy(os.path.join(labels_dir, filename), os.path.join(output_dir_label, filename))

                # 退出检查，因为这张图片中已经有符合要求的物体了
                break


def separate_files(input_folder, json_output_folder, tif_output_folder):
    if not os.path.exists(json_output_folder):
        os.makedirs(json_output_folder)
    if not os.path.exists(tif_output_folder):
        os.makedirs(tif_output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.lower().endswith('.json'):
            shutil.move(file_path, os.path.join(json_output_folder, filename))
        elif filename.lower().endswith('.tif'):
            shutil.move(file_path, os.path.join(tif_output_folder, filename))


def clean_images(json_folder_path, image_folder_path):
    # 获取json文件夹中所有json文件的文件名（不包含扩展名）
    json_filenames = {os.path.splitext(file)[0] for file in os.listdir(json_folder_path) if file.endswith('.json')}

    # 获取图片文件夹中的所有文件名（不包含扩展名）
    image_filenames = {os.path.splitext(file)[0] for file in os.listdir(image_folder_path)}

    # 遍历图片文件夹中的文件名，删除没有对应JSON文件的图片
    for image_filename in image_filenames:
        image_extensions = [".png", ".jpg", ".jpeg", ".tif"]
        for ext in image_extensions:
            image_file_path = os.path.join(image_folder_path, f"{image_filename}{ext}")
            if image_filename not in json_filenames and os.path.exists(image_file_path):
                os.remove(image_file_path)
                print(f"Deleted {image_file_path}")


def count(folder_path):
    # 统计类别的字典
    label_count = {}
    # 遍历文件夹下的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # 打开 JSON 文件
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

                # 获取"label"字段的值
                shapes = data.get("shapes")

                if shapes:
                    for shape in shapes:
                        label = shape.get("label")

                        # 统计类别的出现次数
                        if label:
                            if label in label_count:
                                label_count[label] += 1
                            else:
                                label_count[label] = 1

    # 输出统计结果
    dicts = {}
    datayaml = []
    i = 0
    for label, count in label_count.items():
        print(f"类别 '{label}' : {count} 次")
        dicts.update({f'{label}': i})
        datayaml.append(label)
        i = i + 1
    print(dicts)
    print(datayaml)


def copy_files_by_extension(source_dir, destination_dir, file_extension):
    """
    将源文件夹中指定扩展名的文件复制到目标文件夹
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(file_extension.lower()):
            source_path = os.path.join(source_dir, filename)
            destination_path = os.path.join(destination_dir, filename)
            shutil.copy(source_path, destination_path)
            print(f"已复制文件: {filename}")


def split_files_into_folders(images_dir, json_dir, num_folders, split_folder, name):
    # 获取images和json文件夹中的所有文件
    images_files = os.listdir(images_dir)
    json_files = os.listdir(json_dir)

    # 确保两个文件夹中的文件数量一致
    if len(images_files) != len(json_files):
        print("Error: The number of files in 'images' and 'json' folders must be the same.")
        return

    # 计算每个文件夹应该包含的文件数量
    files_per_folder = len(images_files) // num_folders

    # 创建新的文件夹
    for i in range(num_folders):
        new_images_dir = os.path.join(split_folder, name[i], f"images")
        new_json_dir = os.path.join(split_folder, name[i], f"json")
        os.makedirs(new_images_dir, exist_ok=True)
        os.makedirs(new_json_dir, exist_ok=True)

        # 将文件复制到新的文件夹中
        for j in range(i * files_per_folder, (i + 1) * files_per_folder):
            image_file = images_files[j]
            json_file = json_files[j]
            shutil.copy(os.path.join(images_dir, image_file), os.path.join(new_images_dir, image_file))
            shutil.copy(os.path.join(json_dir, json_file), os.path.join(new_json_dir, json_file))

if __name__ == '__main__':
    txt_folder_path = r'H:\yaogan\第一次标签\liu_txt'  # txt标签目录
    folder_path = r"H:\7-27机场部件数据集\json"  # json标签目录
    root_dir = r'F:\datasets\data'  # 数据集根目录
    img_file = "images"  # 数据集图片路径
    out_file = "tupian"  # 转换后保存路径


    # 图片转格式
    # transform(root_dir,img_file,out_file)

    # 统计json格式下label
    # count(folder_path)

    # 调用函数并输出所有标签类别
    # labels = get_labels(txt_folder_path)
    # print(labels)
    # print(len(labels))

    # # 指定要删除的标签列表和txt文件夹路径
    # labels = ['0', '1', '4', '8', '11', '9', '13', '6', '2', '7', '10']
    # delete_labels(labels, txt_folder_path)

    # 替换标签
    # label_map = {'1': '0', '2': '1','3': '2', '4': '3','5': '4'}
    # replace_label(label_map, txt_folder_path)

    # #要提取的类别名称
    # wanted_classes = ['5', '3']
    # # yolo格式数据集label文件所在的文件夹路径
    # labels_dir = r'F:\study\POSTGRAUDENTNO1-2\DOTA_split\valsplit\labels'
    # # 图片所在的文件夹路径
    # images_dir = r'F:\study\POSTGRAUDENTNO1-2\DOTA_split\valsplit\images'
    # # 要保存提取结果的文件夹路径
    # output_dir = '../data/datas/JPEGImages'
    # output_dir_label = '../data/datas/txt_data'
    # extract_label(labels_dir, images_dir, output_dir, output_dir_label, wanted_classes)

    # # 删除
    # # 用于存储json文件的文件夹路径
    # json_folder_path = r'H:\yaogan\第一次标签\liu_json'
    # # 用于存储图片的文件夹路径
    # image_folder_path = r'H:\yaogan\第一次标签\liu'
    # # 获取json文件夹中所有json文件
    # clean_images(json_folder_path, image_folder_path)

    ''' 
      分离json和tif
    '''
    # source_folder = r"F:\候机楼\王浩舟\2"    # 标签和图片所在
    # tif_destination_folder = "F:\候机楼\images"   # 存放图片
    # json_destination_folder = r"F:\候机楼\lables"  # 存放标签
    # image_type = ".tif"
    # label_type = ".json"
    #
    # # 复制tif文件到目标文件夹
    # copy_files_by_extension(source_folder, tif_destination_folder, image_type)
    # # 复制json文件到目标文件夹
    # copy_files_by_extension(source_folder, json_destination_folder, label_type)


    '''等分数据集'''
    images_folder = r"H:\7-27机场部件数据集\data/images"  # images文件夹路径
    json_folder = r"H:\7-27机场部件数据集\data/json"  # json文件夹路径
    split_folder = r"H:\7-27机场部件数据集/datasplit"
    num_folders = 7  # 将文件分成几个文件夹
    name = ["刘文昊", "王成源", "王浩舟", "冉明武", "杜洋", "阳先鸿", "李海梁"]
    split_files_into_folders(images_folder, json_folder, num_folders, split_folder, name)
