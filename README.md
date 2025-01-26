# 自动选课助手

## 项目简介

自动选课助手是一款专为[rdfz](rdfz.jyyun.com)设计的自动化选课工具。它可以帮助用户在指定时间自动选择课程，提高选课的成功率。本项目仅供学习和交流使用，请勿用于任何商业或非法用途。

## 功能特点

- **自动化选课**：根据用户设定的时间，自动尝试选择指定课程。
- **多线程支持**：利用多线程技术，同时选择多个课程，提高效率。
- **友好的命令行界面**：提供清晰的提示信息和操作指南。
- **错误处理机制**：完善的错误处理机制，确保程序稳定运行。
- **彩色输出**：通过丰富的颜色输出，提升用户体验。

## 使用说明

### 环境准备

1. **安装Python**：确保已安装Python 3.x版本。
2. **安装依赖库**：使用以下命令安装所需的依赖库：
   ```bash
   pip install -r requirements.txt
   ```


### 配置文件

1. **创建配置文件**：在项目根目录下创建一个名为`cfg.json`的文件，并添加如下内容：
   ```json
   {
     "cookie": "你的Cookie"
   }
   ```

   - `cookie`：请参照`操作示例.mp4`中的步骤获取并填写你的Cookie。

### 运行程序

1. **设置选课时间**：运行程序后，输入你希望开始选课的时间（格式：`YYYY-MM-DD HH:MM:SS`），例如：
   ```bash
   输入选课时间（例：2024-09-21 08:00:00）：
   ```


2. **等待选课**：程序会显示倒计时，直到到达设定时间，然后自动开始选课。

3. **选课完成**：当所有课程选择完成后，程序会提示“选课完成”。

## 注意事项

- **合法性声明**：本项目仅供学习、交流使用，严禁用于商业或任何非法用途！
- **Cookie有效期**：请确保提供的Cookie有效且未过期。
- **系统保护**：为了保护学校系统的稳定性，程序会在选课过程中适当延时，避免对服务器造成过大压力。

## 技术细节

### 主要模块

- **utils.py**：包含各种辅助函数，如清除屏幕、暂停程序、退出程序、错误处理等。
- **get_course()**：从学校网站获取课程列表。
- **choose_course()**：尝试选择指定课程，成功后从待选课程列表中移除该课程。
- **main()**：主程序逻辑，负责接收用户输入、启动选课线程、显示进度等。

### 关键代码片段

```python
def choose_course(termId, c_name, courseId, versionNum, course_name_list):
    success = True if random.random() < 0.1 else False
    if success:
        print(blue(f"{c_name}选择成功"))
        course_name_list.remove(c_name)  # 从course_name_list中移除已选择的课程
    else:
        print(red(f"{c_name}选择失败"))
    return success
```
```python
while True:
    if time.time() > start_time + 30:
        for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
            t = threading.Thread(
                target=choose_course,
                args=("bbb", c_name, "aaa", "versionNum", course_name),
            )
            t.start()
        time.sleep(0.5)

    elif time.time() > start_time:
        for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
            t = threading.Thread(
                target=choose_course,
                args=("bbb", c_name, "aaa", "versionNum", course_name),
            )
            t.start()
        time.sleep(0.02)  # 保护学校系统

    else:
        print(
            f"\r\033[K{blue(f'chosen {course_name} waiting {- time.time() + start_time:.2f} seconds')}",
            flush=True,
            end="",
        )
        time.sleep(0.05)

    if len(course_name) == 0:
        print(blue("选课完成"))
        pause()
        leave()
```


## 贡献者

- **Yuanchuan Wang**
- **Haochen Li**

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。

---

感谢您的关注和支持！如果您有任何问题或建议，请随时联系开发者。祝您选课顺利！

---

**特别提醒**：请遵守相关法律法规，合理合法地使用本工具。