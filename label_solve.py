import os
import shutil

from PIL import Image

def get_labels(txt_folder_path):
    # 创建空列表来存储所有标签类别
    labels = []

    # 遍历文件夹内所有txt文件
    for file_name in os.listdir(txt_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(txt_folder_path, file_name)

            # 打开Yolo数据集txt格式的文件
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 提取所有标签类别
            for line in lines:
                label = line.split(' ')[0]
                if label not in labels:
                    labels.append(label)

    # 返回所有标签类别列表
    return labels


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

def transform(root_dir,img_file,out_file):

    input_folder = os.path.join(root_dir, img_file)
    output_folder = os.path.join(root_dir, out_file)
    # 循环遍历原始图片文件夹中的所有jpg图片
    num = 0
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            # 打开jpg图片文件
            img = Image.open(os.path.join(input_folder, filename))
            # 生成输出png图片的文件名
            output_filename = os.path.splitext(filename)[0] + '.png'

            # 保存png图片到输出图片文件夹
            # os.remove(os.path.join(input_folder, filename))
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            img.save(os.path.join(output_folder, output_filename))
            num = num + 1
            print("{}转化成功".format(os.path.splitext(filename)), num)


def replace_label(label_map,label_dir):

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


def extract_label(labels_dir,images_dir,output_dir,output_dir_label,wanted_classes):
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


if __name__ == '__main__':

    txt_folder_path = '../../data/Annotations'  # 标签目录
    root_dir = '../data/datas'  # 数据集根目录
    img_file = "images"    # 数据集图片路径
    out_file = "JPEGImages"   # 转换后保存路径

    # # 图片转格式
    # transform(root_dir,img_file,out_file)

    # # 调用函数并输出所有标签类别
    # labels = get_labels(txt_folder_path)
    # print(labels)
    # print(len(labels))

    # # 指定要删除的标签列表和txt文件夹路径
    # labels = ['0', '1', '4', '8', '11', '9', '13', '6', '2', '7', '10']
    # delete_labels(labels, txt_folder_path)

    # # 替换标签
    # label_map = {'100000001': '0', '100000002': '1'}
    # replace_label(label_map,txt_folder_path)

    # # 要提取的类别名称
    # wanted_classes = ['5', '3']
    # # yolo格式数据集label文件所在的文件夹路径
    # labels_dir = r'F:\study\POSTGRAUDENTNO1-2\DOTA_split\valsplit\labels'
    # # 图片所在的文件夹路径
    # images_dir = r'F:\study\POSTGRAUDENTNO1-2\DOTA_split\valsplit\images'
    # # 要保存提取结果的文件夹路径
    # output_dir = '../data/datas/JPEGImages'
    # output_dir_label = '../data/datas/txt_data'
    # extract_label(labels_dir, images_dir, output_dir, output_dir_label, wanted_classes)

