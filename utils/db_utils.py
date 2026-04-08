"""
Database Utilities
数据库操作工具（可选）
"""
import pymysql
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from loguru import logger


class DatabaseUtils:
    """
    数据库工具类
    支持连接池、事务管理
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "testdb",
        charset: str = "utf8mb4"
    ):
        """
        初始化数据库配置

        Args:
            host: 数据库主机
            port: 端口
            user: 用户名
            password: 密码
            database: 数据库名
            charset: 字符集
        """
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": charset,
            "cursorclass": pymysql.cursors.DictCursor
        }
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**self.config)
            logger.info(f"Database connected: {self.config['host']}:{self.config['port']}/{self.config['database']}")
            return self.connection
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    @contextmanager
    def get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行查询SQL

        Args:
            sql: SQL语句
            params: SQL参数

        Returns:
            查询结果列表
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    result = cursor.fetchall()
                    logger.debug(f"Query executed: {sql}")
                    return result
        except Exception as e:
            logger.error(f"Query execution failed: {sql} - {e}")
            raise

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行更新SQL

        Args:
            sql: SQL语句
            params: SQL参数

        Returns:
            影响的行数
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    affected_rows = cursor.execute(sql, params)
                    conn.commit()
                    logger.debug(f"Update executed: {sql}, affected rows: {affected_rows}")
                    return affected_rows
        except Exception as e:
            logger.error(f"Update execution failed: {sql} - {e}")
            raise

    def execute_insert(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行插入SQL

        Args:
            sql: SQL语句
            params: SQL参数

        Returns:
            插入的ID
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    conn.commit()
                    last_id = cursor.lastrowid
                    logger.debug(f"Insert executed: {sql}, last id: {last_id}")
                    return last_id
        except Exception as e:
            logger.error(f"Insert execution failed: {sql} - {e}")
            raise

    def execute_delete(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行删除SQL

        Args:
            sql: SQL语句
            params: SQL参数

        Returns:
            影响的行数
        """
        return self.execute_update(sql, params)

    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """
        批量执行SQL

        Args:
            sql: SQL语句
            params_list: SQL参数列表

        Returns:
            影响的行数
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    affected_rows = cursor.executemany(sql, params_list)
                    conn.commit()
                    logger.debug(f"Batch executed: {sql}, affected rows: {affected_rows}")
                    return affected_rows
        except Exception as e:
            logger.error(f"Batch execution failed: {sql} - {e}")
            raise

    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        查询单条记录

        Args:
            sql: SQL语句
            params: SQL参数

        Returns:
            查询结果字典
        """
        results = self.execute_query(sql, params)
        return results[0] if results else None

    def table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在

        Args:
            table_name: 表名

        Returns:
            表是否存在
        """
        sql = "SHOW TABLES LIKE %s"
        result = self.query_one(sql, (table_name,))
        return result is not None

    def count(self, table_name: str, where: str = "1=1") -> int:
        """
        统计表记录数

        Args:
            table_name: 表名
            where: WHERE条件

        Returns:
            记录数
        """
        sql = f"SELECT COUNT(*) as count FROM {table_name} WHERE {where}"
        result = self.query_one(sql)
        return result["count"] if result else 0

    def truncate(self, table_name: str):
        """
        清空表

        Args:
            table_name: 表名
        """
        sql = f"TRUNCATE TABLE {table_name}"
        self.execute_update(sql)
        logger.info(f"Table truncated: {table_name}")


# 全局实例
db_utils = None

def get_db_utils(config: Dict[str, Any]) -> DatabaseUtils:
    """
    获取数据库工具实例

    Args:
        config: 数据库配置

    Returns:
        DatabaseUtils 实例
    """
    global db_utils
    if db_utils is None:
        db_utils = DatabaseUtils(**config)
    return db_utils


__all__ = ["DatabaseUtils", "get_db_utils"]
