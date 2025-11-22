#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改超级管理员账号和密码脚本
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def change_admin_password():
    """修改超级管理员密码"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'xianyu_data.db')

    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False

    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 新管理员账号与密码
        admin_username = "osamku"
        new_password = "Aa533897."

        # 检查管理员是否存在
        cursor.execute("SELECT username FROM users WHERE username = ?", (admin_username,))
        admin_user = cursor.fetchone()

        if not admin_user:
            print(f"未找到超级管理员账户: {admin_username}")
            return False

        # 生成新密码哈希
        password_hash = generate_password_hash(new_password)

        # 更新密码
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (password_hash, admin_username)
        )
        conn.commit()

        print(f"超级管理员密码已成功修改！")
        print(f"   用户名: {admin_username}")
        print(f"   新密码: {new_password}")

        # 验证更新
        cursor.execute(
            "SELECT username, role, is_active FROM users WHERE username = ?",
            (admin_username,)
        )
        updated_user = cursor.fetchone()

        if updated_user:
            print("\n账户信息验证成功:")
            print(f"   用户名: {updated_user[0]}")
            print(f"   角色: {updated_user[1]}")
            print(f"   状态: {'活跃' if updated_user[2] else '未激活'}")

        conn.close()
        return True

    except Exception as e:
        print(f"修改密码时出错: {e}")
        return False


if __name__ == "__main__":
    print("=== 修改超级管理员密码 ===")
    success = change_admin_password()
    if success:
        print("\n请使用以下凭据登录:")
        print("用户名: osamku")
        print("密码: Aa533897.")
        print("\n登录页面: http://127.0.0.1:5001/login")
    else:
        print("\n修改失败！")

