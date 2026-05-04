"""
DDL转换核心逻辑
将源数据库DDL转换为目标数据库DDL
"""
import re
import sqlparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from app.models.type_mapping import get_type_mapping, TypeMapping
from app.core.logger import logger


@dataclass
class ColumnInfo:
    """列信息"""
    name: str
    source_type: str
    target_type: str
    length: Optional[str] = None
    scale: Optional[str] = None
    nullable: bool = True
    default_value: Optional[str] = None
    comment: Optional[str] = None
    is_primary: bool = False


@dataclass
class TableInfo:
    """表信息"""
    name: str
    columns: List[ColumnInfo] = field(default_factory=list)
    comment: Optional[str] = None
    primary_keys: List[str] = field(default_factory=list)


@dataclass
class ConvertResult:
    """转换结果"""
    success: bool
    converted_ddl: Optional[str] = None
    table_info: Optional[TableInfo] = None
    errors: List[str] = field(default_factory=list)


class DDLConverter:
    """DDL转换器"""

    def __init__(self, source_db: str, target_db: str):
        self.source_db = source_db.lower()
        self.target_db = target_db.lower()
        self.type_mapping = get_type_mapping(source_db, target_db)

    def convert(self, ddl: str) -> ConvertResult:
        """
        转换DDL

        Args:
            ddl: 源数据库DDL

        Returns:
            ConvertResult: 转换结果
        """
        try:
            # 标准化DDL
            normalized_ddl = self._normalize_ddl(ddl)

            # 解析表信息
            table_info = self._parse_table_info(normalized_ddl)

            if not table_info:
                return ConvertResult(
                    success=False,
                    errors=["无法解析DDL，请检查语法"]
                )

            # 转换列类型
            self._convert_column_types(table_info)

            # 生成目标DDL
            converted_ddl = self._generate_target_ddl(table_info)

            return ConvertResult(
                success=True,
                converted_ddl=converted_ddl,
                table_info=table_info
            )

        except Exception as e:
            logger.error(f"DDL转换失败: {str(e)}")
            return ConvertResult(
                success=False,
                errors=[f"转换失败: {str(e)}"]
            )

    def _normalize_ddl(self, ddl: str) -> str:
        """标准化DDL"""
        # 移除多余空格和换行
        normalized = re.sub(r'\s+', ' ', ddl.strip())

        # 统一大写关键字（保留字符串中的内容）
        keywords = [
            'CREATE', 'TABLE', 'NOT', 'NULL', 'DEFAULT', 'PRIMARY',
            'KEY', 'UNIQUE', 'INDEX', 'COMMENT', 'ENGINE', 'CHARSET',
            'COLLATE', 'IF', 'NOT', 'EXISTS', 'AUTO_INCREMENT'
        ]

        for keyword in keywords:
            # 只替换独立的关键字（不是字符串的一部分）
            pattern = r'\b' + keyword + r'\b'
            normalized = re.sub(pattern, keyword, normalized, flags=re.IGNORECASE)

        return normalized

    def _parse_table_info(self, ddl: str) -> Optional[TableInfo]:
        """解析表信息"""
        # 提取表名
        table_name_match = re.search(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`?(\w+)`?\.)?`?(\w+)`?',
            ddl,
            re.IGNORECASE
        )
        if not table_name_match:
            return None

        table_name = table_name_match.group(2)

        # 提取列定义部分
        columns_match = re.search(r'\((.*)\)', ddl, re.DOTALL | re.IGNORECASE)
        if not columns_match:
            return None

        columns_part = columns_match.group(1)

        # 分割列定义
        columns_info: List[ColumnInfo] = []
        primary_keys: List[str] = []
        table_comment = None

        # 提取表注释（只在括号外查找）
        # 先找到列定义的结束括号
        columns_end = columns_match.end()
        # 在列定义结束之后查找表注释
        comment_match = re.search(r'COMMENT\s*[=]?\s*[\'"](.+?)[\'"]', ddl[columns_end:], re.IGNORECASE)
        if comment_match:
            table_comment = comment_match.group(1)

        # 提取主键约束
        primary_match = re.search(r'PRIMARY\s+KEY\s*\(([^)]+)\)', columns_part, re.IGNORECASE)
        if primary_match:
            primary_keys = [pk.strip().strip('`\'"') for pk in primary_match.group(1).split(',')]

        # 解析列定义
        col_definitions = self._split_column_definitions(columns_part)

        for col_def in col_definitions:
            col_info = self._parse_column_def(col_def)
            if col_info:
                # 如果列定义中有PRIMARY KEY，则添加到primary_keys列表
                if col_info.is_primary and col_info.name not in primary_keys:
                    primary_keys.append(col_info.name)
                columns_info.append(col_info)

        return TableInfo(
            name=table_name,
            columns=columns_info,
            comment=table_comment,
            primary_keys=primary_keys
        )

    def _split_column_definitions(self, columns_part: str) -> List[str]:
        """分割列定义"""
        # 简单分割，不处理嵌套括号
        definitions = []
        current = ""
        depth = 0

        for char in columns_part:
            if char == '(':
                depth += 1
                current += char
            elif char == ')':
                depth -= 1
                current += char
            elif char == ',' and depth == 0:
                definitions.append(current.strip())
                current = ""
            else:
                current += char

        if current.strip():
            definitions.append(current.strip())

        # 过滤掉非列定义（如约束定义）
        result = []
        for df in definitions:
            df_stripped = df.strip()
            df_upper = df_stripped.upper()

            # 检查是否是列定义（第一个单词是列名，第二个是类型）
            words = df_stripped.split()
            if len(words) >= 2:
                # 第二个单词应该是类型，检查是否以括号或纯字母结尾（类型特征）
                second_word = words[1].upper().rstrip(',;')
                is_type_def = (
                    # 类型关键字
                    any(ty in second_word for ty in ['INT', 'BIGINT', 'SMALLINT', 'TINYINT', 'VARCHAR',
                                                     'CHAR', 'TEXT', 'DECIMAL', 'NUMERIC', 'FLOAT',
                                                     'DOUBLE', 'DATE', 'DATETIME', 'TIMESTAMP',
                                                     'TIME', 'BOOLEAN', 'BLOB', 'BINARY',
                                                     'SERIAL', 'BIGSERIAL', 'NUMBER', 'NVARCHAR', 'MONEY'])
                    # 或者类型带长度
                    or re.match(r'^[A-Z]+\(\d+', second_word)
                )

                if is_type_def:
                    result.append(df_stripped)
                else:
                    # 跳过独立的约束定义（如 PRIMARY KEY (id)）
                    if any(kw in df_upper for kw in ['PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY', 'INDEX']):
                        continue

        return result

    def _parse_column_def(self, col_def: str) -> Optional[ColumnInfo]:
        """解析列定义"""
        col_def = col_def.strip()

        # 分割单词
        words = col_def.split()
        if len(words) < 2:
            return None

        col_name = words[0].strip('`\'"')
        col_type = words[1].upper()

        # 提取长度和精度
        length = None
        scale = None

        length_match = re.search(r'\((\d+)(?:,(\d+))?\)', col_def)
        if length_match:
            length = length_match.group(1)
            scale = length_match.group(2)

        # 检查是否允许NULL
        nullable = True
        if 'NOT NULL' in col_def.upper():
            nullable = False

        # 提取默认值（使用更简单直接的方法）
        default_value = None
        # 匹配 DEFAULT 'string' 或 DEFAULT "string" 或 DEFAULT number/keyword
        # 先找单引号包裹的值
        single_quote_match = re.search(r"DEFAULT\s+'([^']*)'", col_def, re.IGNORECASE)
        if single_quote_match:
            default_value = single_quote_match.group(1)
        else:
            # 再找双引号包裹的值
            double_quote_match = re.search(r'DEFAULT\s+"([^"]*)"', col_def, re.IGNORECASE)
            if double_quote_match:
                default_value = double_quote_match.group(1)
            else:
                # 最后找无引号的值（数字或关键字）
                no_quote_match = re.search(r'DEFAULT\s+(\w+)\s*(?:NOT\s+NULL)?', col_def, re.IGNORECASE)
                if no_quote_match:
                    default_value = no_quote_match.group(1)

        # DEBUG: 输出DEFAULT值提取信息
        # logger.debug(f"DEFAULT提取: col_def={repr(col_def)}, default_value={repr(default_value)}")

        # 提取注释
        comment = None
        comment_match = re.search(r'COMMENT\s+[\'"](.+?)[\'"]', col_def, re.IGNORECASE)
        if comment_match:
            comment = comment_match.group(1)

        # 检查是否是主键列
        is_primary = False
        if 'PRIMARY KEY' in col_def.upper():
            is_primary = True

        return ColumnInfo(
            name=col_name,
            source_type=col_type,
            target_type="",  # 稍后转换
            length=length,
            scale=scale,
            nullable=nullable,
            default_value=default_value,
            comment=comment,
            is_primary=is_primary
        )

    def _convert_column_types(self, table_info: TableInfo):
        """转换列类型"""
        for col in table_info.columns:
            # 获取原始类型（不带长度）
            base_type = re.sub(r'\(.*\)', '', col.source_type).strip().lower()

            # 查找映射
            mapping = self.type_mapping.get(base_type)

            if mapping:
                target_type = mapping.target_type

                # 如果需要长度且存在长度，则添加
                if mapping.need_length and col.length:
                    target_type += f"({col.length}"
                    if col.scale:
                        target_type += f",{col.scale}"  # 修复：删除逗号后的空格
                    target_type += ")"
            else:
                # 没有映射，保持原样或使用STRING
                target_type = col.source_type.upper()
                logger.warning(f"未找到类型映射: {col.source_type} -> {target_type}")

            col.target_type = target_type

    def _generate_target_ddl(self, table_info: TableInfo) -> str:
        """生成目标DDL"""
        lines = []

        # CREATE TABLE 语句
        lines.append(f"CREATE TABLE IF NOT EXISTS `{table_info.name}` (")

        # 列定义
        col_lines = []
        for i, col in enumerate(table_info.columns):
            col_def = f"  `{col.name}` {col.target_type}"

            # 主键列必须为NOT NULL
            if col.is_primary or not col.nullable:
                if self.target_db != "clickhouse":
                    col_def += " NOT NULL"

            if col.default_value:
                col_def += f" DEFAULT {col.default_value}"

            if col.comment:
                if self.target_db == "clickhouse":
                    col_def += f" COMMENT '{col.comment}'"
                elif self.target_db == "doris":
                    col_def += f" COMMENT '{col.comment}'"
                # Greenplum comments are added separately

            col_lines.append(col_def)

        lines.append(',\n'.join(col_lines))
        lines.append(")")

        if self.target_db == "doris":
            # ENGINE = OLAP
            lines.append("ENGINE = OLAP")

            # UNIQUE KEY（如果有主键）
            if table_info.primary_keys:
                pk_cols = ', '.join([f"`{pk}`" for pk in table_info.primary_keys])
                lines.append(f"UNIQUE KEY ({pk_cols})")

            # 表注释
            if table_info.comment:
                lines.append(f"COMMENT '{table_info.comment}'")

            # 分布式配置
            if table_info.primary_keys:
                # 使用第一个主键列作为分桶键
                bucket_key = table_info.primary_keys[0]
                lines.append(f"DISTRIBUTED BY HASH(`{bucket_key}`) BUCKETS 10")
            else:
                # 如果没有主键，使用第一列作为分桶键
                if table_info.columns:
                    bucket_key = table_info.columns[0].name
                    lines.append(f"DISTRIBUTED BY HASH(`{bucket_key}`) BUCKETS 10")

            # Doris特有的表属性
            lines.append("PROPERTIES (")
            lines.append("  \"replication_allocation\" = \"tag.location.default: 1\"")
            lines.append(")")

        elif self.target_db == "clickhouse":
            lines.append("ENGINE = MergeTree()")
            if table_info.primary_keys:
                pk_cols = ', '.join([f"`{pk}`" for pk in table_info.primary_keys])
                lines.append(f"ORDER BY ({pk_cols})")
            else:
                lines.append("ORDER BY tuple()")

            # Clickhouse table comment
            if table_info.comment:
                lines.append(f"COMMENT '{table_info.comment}'")

        elif self.target_db == "greenplum":
            if table_info.primary_keys:
                pk_cols = ', '.join([f"`{pk}`" for pk in table_info.primary_keys])
                lines.append(f"DISTRIBUTED BY ({pk_cols});")
            else:
                if table_info.columns:
                    lines.append(f"DISTRIBUTED BY (`{table_info.columns[0].name}`);")
                else:
                    lines.append("DISTRIBUTED RANDOMLY;")

            # Greenplum table comment
            if table_info.comment:
                lines.append(f"COMMENT ON TABLE `{table_info.name}` IS '{table_info.comment}';")

            # Greenplum column comments
            for col in table_info.columns:
                if col.comment:
                    lines.append(f"COMMENT ON COLUMN `{table_info.name}`.`{col.name}` IS '{col.comment}';")

        return '\n'.join(lines)

    def _format_column_type(self, source_type: str) -> str:
        """格式化列类型"""
        return source_type.upper()
