#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auto course select for rdfz.jyyun.com
# Created: 2024-08-31
# Last modified: 2024-09-26
# Author: Haochen Li(post requests mainly)
# Author: Yuancuhan Wang (multiple threads, cmd line output, security)
"""
本项目旨在解放学生‌‍双手，选到心仪的‌‍课程。
本项目仅供学习、交流使用，严禁用于商业或任何非法用途！
请开发者务必控制程序的发行量，切勿给学校系统带来麻烦！！
请开发者务必控制程序的发行量，切勿给学校系统带来麻烦！！！

This project aims to free students' hands and help them find their desired courses.
This project is intended for learning and exchange purposes only and is strictly prohibited for any commercial or illegal use!
Developers must keep the distribution of the program under control to avoid causing any trouble for school systems!!
Developers must keep the distribution of the program under control to avoid causing any trouble for school systems!!!

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

(前两个字是王羲之的，后一个字是赵孟頫的，那第三个字是谁的呢？）。https://www.sfzd.cn

Change Log
========================
Version 1.0.0 (2024-09-25)
--------------------------------
- first release
- support for multiple threads
- make cmd line output more beautiful
- add security check to control the number of users

Versio 1.0.1 (2025-1-22)
--------------------------------
- removed security check
- stop when success
"""

from utils import main
import requests

try:
    main()
except requests.exceptions.ProxyError:
    print("\033[38;2;255;0;0m请关闭您的代理。\033[0m")
except Exception as e:
    print("\033[38;2;255;0;0msome error happened\033[0m")
except KeyboardInterrupt:
    print("\033[0m")
