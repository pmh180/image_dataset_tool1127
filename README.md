# Image Dataset Organizer
用于扫描文件夹内的图片，按照图片名前缀(cat,dog,pig)、图片尺寸大小分类，支持批量重命名为photo_*格式，并导出report.csv报表。

## 功能
- 递归扫描文件夹，识别 .jpg / .png / .bmp 图片
- 按文件名前缀分类（cat、dog、pig）
- 按图片最小边尺寸分类（small / medium / large）
- 批量重命名，格式：photo_0001.jpg
- 完善异常捕获：文件夹不存在、图片损坏、重命名冲突、CSV写入权限错误等
- 输出report.csv，记录原图名称、新名称、路径、宽高、尺寸分类、前缀分类

## 环境
Python 3.10+，依赖见requirements.txt

## 安装
```bash
pip install -r requirements.txt
# 只扫描 + 生成报告，不重命名
python dataset_organizer.py ./test_data

# 扫描 + 批量重命名 + 生成报告
python dataset_organizer.py ./test_data --rename

输出说明
report.csv：保存图片信息，字段：old_name,new_name,path,width,height,size_class,prefix_class
开启 --rename 后，图片会被重命名，保留原图文件

## report.csv 输出示例
old_name,new_name,path,width,height,size_class,prefix_class
cat.jpg,photo_0001.jpg,test_data\photo_0001.jpg,1280,2774,large,cat
dog.jpg,photo_0002.jpg,test_data\photo_0002.jpg,1280,2774,large,dog
pig.png,photo_0003.png,test_data\photo_0003.png,1290,2796,large,pig

## 注意事项
1. 建议先不带 `--rename` 执行一次，查看 csv 报告确认无误再重命名
2. 损坏、无法读取的图片会自动跳过，不会写入报表
3. 遇到文件名冲突会捕获异常，不会直接覆盖图片
4. 路径支持相对路径和绝对路径

项目结构
dataset_organizer.py   # 主脚本
requirements.txt
README.md
