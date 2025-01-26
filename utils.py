#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auto course select for rdfz.jyyun.com
# Created: 2024-08-31
# Last modified: 2025-1-26
# Author: Yuanchuan Wang, Haochen Li
import json
import os
import platform
import sys
import threading
import time

import requests
from rich.color import Color
from rich.color_triplet import ColorTriplet
from rich.console import Console, RichCast
from rich.live import Live
from rich.spinner import Spinner
from rich.style import Style
from rich.table import Table

with open("./cfg.json", encoding="utf-8") as f:
    cfg = json.load(f)
    COOKIE = cfg["cookie"]

is_windows = True if platform.system() == "Windows" else False

FPS = 60
signal = True
lock = threading.Lock()

def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")


def pause():
    if is_windows:
        print(blue("按任意键继续。。。"))
        os.system(f"pause >nul")
    else:
        input("按Enter继续。。。")


def leave():
    try:
        sys.exit()
    except:
        exit()


def error(err):
    print(red(f"[!] Error : {err}"), end="")
    pause()
    clear()
    leave()


def _process(ori: int, mm: tuple[int, int]):
    assert 0 <= mm[0] <= mm[1] <= 255
    if ori > mm[1]:
        return mm[1]
    elif ori < mm[0]:
        return mm[0]
    else:
        return ori


def base_color(r, g, b, dr, dg, db, text,
               mmr: tuple[int, int] = (0, 255), mmg: tuple[int, int] = (0, 255), mmb: tuple[int, int] = (0, 255),
               _input=False) -> str:
    os.system("")
    faded = ""
    assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
    red, green, blue = r, g, b
    for line in text.splitlines():
        red, green, blue = r, g, b
        for character in line:
            red += dr
            green += dg
            blue += db
            red = _process(red, mmr)
            green = _process(green, mmg)
            blue = _process(blue, mmb)

            faded += f"\033[38;2;{red};{green};{blue}m{character}\033[0m"
        faded += "\n"
    faded = faded.strip()
    if _input:
        faded += f"\033[38;2;{red};{green};{blue}m"
    return faded


def red(text, _input=False):
    return base_color(255, 170, 0, 0, -10, 0, text, _input=_input)


def blue(text, _input=False):
    return base_color(44, 180, 255, 5, 2, 0, text, mmr=(0, 173), _input=_input)


def green(text, _input=False):
    return base_color(2, 180, 2, 2, 2, 0, text, _input=_input)


def water(text):
    return base_color(44, 150, 255, 2, 1, 0, text, mmr=(0, 173))


def get_course(termid=""):
    html_url = (
        "https://rdfz.lezhiyun.com/xsxk/studentElective/redisEnterStudentSelect.do"
    )
    headers = {
        "cookie": COOKIE,
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    data = {"termid": termid}
    response = requests.get(url=html_url, headers=headers, data=data)
    return response.json()


def choose_course(termId, c_name, courseId, versionNum, course_name_list):
    html_url = (
        "https://rdfz.lezhiyun.com/xsxk/studentElective/redisStudentSelectCourse.do"
    )
    headers = {
        "cookie": COOKIE,
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    data = {"termId": termId, "courseId": courseId, "versionNum": versionNum}
    response = requests.post(url=html_url, headers=headers, data=data)
    data = response.json()
    success = data['success']
    if success:
        with lock:  # 使用线程锁保护对course_name_list的修改
            course_name_list.remove(c_name)  # 从course_name_list中移除已选择的课程


def generate_table(c_name, cname, spinner: Spinner) -> Table:
    """
    :param spinner:
    :param c_name: 没有选择成功的课程名称
    :param cname: 全部课程名称
    :return:
    """
    table = Table(min_width=100,
                  style=Style(color=Color.from_triplet(ColorTriplet(44, 180, 255))),
                  row_styles=(Style(color=Color.from_triplet(ColorTriplet(44, 180, 255))),),
                  header_style=Style(color=Color.from_triplet(ColorTriplet(44, 180, 255))))
    table.add_column("课程名称")
    table.add_column("状态")

    for row in cname:
        value = row in c_name
        table.add_row(
            f"{row}", spinner.render(time.time()) if value else "[green] √ 选择成功"
        )
    return table

def render(c_name, cname, spinner: Spinner, live:Live):
    global signal
    while signal:
        live.update(generate_table(c_name, cname, spinner))
        time.sleep(1 / FPS)

def main():
    global signal
    clear()
    console = Console(width=int(1e6))
    if is_windows:
        os.system("title 自动选课 by wyc")

    BOARD = """ 
       **                .@@                               .@*                                      
      *@@              .@@.                                .@@                  @@                  
     **.              ...@@.*.                        ..    @@.                 .@@          .@*.   
                        .@@*.                         @@ ..@@@@                          **@@@..*@. 
       @@@..        ..***@.         ..        ..     *@@@@@@@@.                  @@.  *. ...@*  *@@ 
          @*   ..***.....@*..*@@  .**@@       *@@   *@@@@@@@@*.*@.         .@@@@@...  *@. .@@*@@@*  
           @         *..*@*. .@. ..  @.       .@*   @@@*..*@@@@@*      .*@@@.  ...     *@* .@*@*    
  ...  .*  .        @. .*@..*@      @@..      .      ...*@@**@@.    .*         @@.      *@**@*      
 .@@.  @.  .       .@...*@*..  ....@@..*@*    *.    *@@@*  .@@@   .@*.                     .@@.**   
 @@@. .*   @.      .@*...@..   ** .@   .@*    *@   ***   .@@*@@@  @*          @@@.       @@@@@      
 @* @  *.  @        .. .*@**.  *..@    @@     .@       .@@@   @@@@*              ...        @@      
    .. *@**.         .*.*@*.   .@*   .@@       **     .**.    .@@.          .  ..*@@  .@.   @@  .*. 
     *@@**.             *@.    *@*. *@*    @@@@@@@*.                        *@*@.*@.  *@.   @@   .@@
   .@*.               .@@.   .*  *@@@.     ..****@@@@@@@******..**@*          @*.        .*@@     ..
  .*.                .**   .                        ..**@@@@@@@@@@@.                      ..        

    """
    print(water(BOARD))
    print(red("                  [Warning] 本项目仅供学习、交流使用，严禁用于商业或任何非法用途！"))
    print()

    if len(COOKIE) < 50:
        print(red("请写入参照 操作示例.mp4 写入cookie。"))
        pause()
        leave()

    TIME = input(blue("输入选课时间（例：2024-09-21 08:00:00）：", True))
    while True:
        try:
            start_time = time.mktime(time.strptime(TIME, "%Y-%m-%d %H:%M:%S"))
            break
        except:
            TIME = input(red("时间格式不正确（例：2024-09-21 08:00:00）：", True))

    try:
        courses = get_course()["data"]
    except KeyError:
        print(red("没有可选课程"))
        pause()
        leave()
    except requests.exceptions.JSONDecodeError:
        print(red("请写入参照 操作示例.mp4 写入cookie。"))
        pause()
        leave()

    versionNum = courses["versionNum"]
    activityList = courses["activityList"]

    for i, _list in enumerate(activityList):
        print(blue(f"{i}: {_list[list(_list.keys())[-1]]}"))

    if len(activityList) == 1:
        termId = activityList[0]["activityId"]
    else:
        i = input(blue("您要选择的时段：", True))
        while True:
            try:
                i = int(i) - 1
                break
            except ValueError:
                i = input(red("请输入数字：", True))
        termId = activityList[i]["activityId"]

    courses = get_course(termId)["data"]["allCourseInfo"]

    course_dict = {}
    course_info = {}
    for i, k_ in enumerate(courses.keys()):
        course = courses[k_]
        course_name = course["courseName"].replace(' ', '_')
        courseId = course["courseId"]
        print(blue(f"{i}: {course_name}"))
        course_dict[course_name] = courseId
        info_dict = []
        for key in ["teacherIntroducation", "courseRemark", "courseIntroducation"]:
            try:
                info_dict.append(course[key])
            except KeyError:
                info_dict.append("暂无")
        info_dict = (f"授课老师：{info_dict[0]}\n"
                     f"{info_dict[1]}"
                     f"课程简介：{info_dict[2]}")

        course_info[course_name] = info_dict

    course_name = input(blue("请输入所选课程名称：（以空格分隔 -q classname查看简介）", True)).split(" ")
    while True:
        if course_name[0].startswith('-q'):
            course_name = course_name[1:]
            if all([x in course_dict.keys() for x in course_name]):
                for k in course_name:
                    print(water(f"{k}:\n"
                                f"{course_info[k]}"))
                course_name = input(blue("请输入所选课程名称：（以空格分隔 -q classname查看简介）", True)).split(" ")
                continue
            else:
                course_name = input(red("所选课程名称不正确：（以空格分隔 -q classname查看简介）", True)).split(" ")
                continue

        elif not all([x in course_dict.keys() for x in course_name]):
            course_name = input(red("所选课程名称不正确：（以空格分隔 -q classname查看简介）", True)).split(" ")
            continue

    course_str = "、".join(course_name)
    cname = course_name.copy()
    with console.status(blue(f'chosen {course_str} waiting {- time.time() + start_time:.2f} seconds'),
                        spinner="dots12", refresh_per_second=FPS,
                        spinner_style=Style(color=Color.from_triplet(ColorTriplet(44, 180, 255)))) as status:
        while True:
            if time.time() > start_time - 0.11:
                break
            else:
                status.update(blue(f'chosen {course_name} waiting {- time.time() + start_time:.2f} seconds'))
                time.sleep(0.05)

    spinner = Spinner("dots12", "[red]正在选择中...",
                      style=Style(color=Color.from_triplet(ColorTriplet(44, 180, 255))))

    signal = True
    with Live(generate_table(course_name, cname, spinner), refresh_per_second=FPS) as live:
        render_thread = threading.Thread(target=render, args=(course_name, cname, spinner, live))
        render_thread.start()
        while True:
            if time.time() > start_time + 30:
                for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
                    t = threading.Thread(
                        target=choose_course,
                        args=(termId, c_name, course_dict[c_name], versionNum, course_name),
                    )
                    t.start()
                time.sleep(0.5)

            elif time.time() > start_time - 0.1:
                for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
                    t = threading.Thread(
                        target=choose_course,
                        args=(termId, c_name, course_dict[c_name], versionNum, course_name),
                    )
                    t.start()
                time.sleep(0.02)  # 保护学校系统

            if len(course_name) == 0:
                break

        signal = False
        render_thread.join()
    print(green("选课完成"))

    pause()
    leave()
