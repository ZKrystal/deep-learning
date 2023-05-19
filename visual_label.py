import cv2
import numpy as np
import os

def visualize_yolo_labels(image_path, labels_path, class_names):
    # 读取图像
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # 读取YOLO标签
    with open(labels_path, 'r') as f:
        labels = f.read().strip().split('\n')

    for label in labels:
        # 解析标签
        class_id, x, y, w, h = map(float, label.split())

        # 转换坐标
        x = int((x - w/2) * width)
        y = int((y - h/2) * height)
        w = int(w * width)
        h = int(h * height)

        # 绘制边界框和类别
        color = (0, 255, 0)  # 绿色边界框
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
        class_name = class_names[int(class_id)]
        label = f'{class_name}'
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # 返回带有边界框的图像
    return image

# 示例用法
image_dir = r'../../dataoil/JPEGImages'  # 图像文件夹路径
labels_dir = r'../../dataoil/txt_data'  # YOLO标签文件夹路径
class_names = ['Oildepot']
# class_names = ['Fixed-wing Aircraft', 'Small Aircraft', 'Cargo Plane', 'Helicopter', 'Passenger Vehicle', 'Small Car', 'Bus',
#         'Pickup Truck', 'Utility Truck', 'Truck', 'Cargo Truck', 'Truck w/Box', 'Truck Tractor', 'Trailer',
#         'Truck w/Flatbed', 'Truck w/Liquid', 'Crane Truck', 'Railway Vehicle', 'Passenger Car', 'Cargo Car',
#         'Flat Car', 'Tank car', 'Locomotive', 'Maritime Vessel', 'Motorboat', 'Sailboat', 'Tugboat', 'Barge',
#         'Fishing Vessel', 'Ferry', 'Yacht', 'Container Ship', 'Oil Tanker', 'Engineering Vehicle', 'Tower crane',
#         'Container Crane', 'Reach Stacker', 'Straddle Carrier', 'Mobile Crane', 'Dump Truck', 'Haul Truck',
#         'Scraper/Tractor', 'Front loader/Bulldozer', 'Excavator', 'Cement Mixer', 'Ground Grader', 'Hut/Tent', 'Shed',
#         'Building', 'Aircraft Hangar', 'Damaged Building', 'Facility', 'Construction Site', 'Vehicle Lot', 'Helipad',
#         'Storage Tank', 'Shipping container lot', 'Shipping Container', 'Pylon', 'Tower']  # class names

# 遍历图像文件夹中的图像文件
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    labels_file = os.path.splitext(image_file)[0] + '.txt'
    labels_path = os.path.join(labels_dir, labels_file)

    # 可视化YOLO标签
    result_image = visualize_yolo_labels(image_path, labels_path, class_names)

    # 显示和保存结果图像
    # cv2.imshow('YOLO Labels', result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(os.path.join('resultss', image_file), result_image)



