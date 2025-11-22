#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建新的超级管理员账户
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def create_admin_user():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'xianyu_data.db')

    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        username = "osamku"
        password = "Aa533897."
        password_hash = generate_password_hash(password)
        role = "admin"
        is_active = 1  # 1 = 可用

        # 检查是否已存在
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone()

        if exists:
            print(f"用户 {username} 已存在，不重复创建。")
            return False

        # 插入新管理员
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, is_active) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, is_active)
        )
        conn.commit()

        print("超级管理员创建成功！")
        print(f"   用户名: {username}")
        print(f"   密码: {password}")
        print(f"   角色: {role}")
        print("   状态: 已激活")

        conn.close()
        return True

    except Exception as e:
        print(f"创建管理员出错: {e}")
        return False


if __name__ == "__main__":
    print("=== 创建新管理员账号 ===")
    if create_admin_user():
        print("\n请使用以下凭据登录：")
        print("用户名：osamku")
        print("密码：Aa533897.")
        print("\n登录页面：http://127.0.0.1:5001/login")
    else:
        print("\n创建失败！")
