# encoding:utf-8
"""
数据库配置文件
"""

# 源数据库配置

SOURCE_CONFIG = {
    'host': '10.245.146.44',
    'port': 3306,
    'user': 'root',
    'passwd': 'platform',
    'db': 'monitoring_host_process',
    'charset': 'utf8',
    'use_unicode': True
}

# 提取符合条件的进程信息，另外注意不在status是新添加进来的进程信息
sql = """
        SELECT
	process_info.pid,
	host_info.host_ip,
	host_info. PORT,
	host_info.login_name,
	host_info.pwd,
	process_info.process_id,
	process_info.log_route,
	process_info.log_name
FROM
	process_info,
	host_info
WHERE
	process_info.host_id = host_info.host_id
AND process_info.save = 1
AND process_info.process_id IN (
	SELECT
		process_id
	FROM
		(
			SELECT
				TIMESTAMPDIFF(
					MINUTE,
					max(process_status.create_time),
					CURRENT_TIME
				) >= process_info.`interval_time` AS t,
				process_status.process_id
			FROM
				`process_status`,
				process_info
				WHERE process_info.process_id = process_status.process_id
                  AND process_info.save = 1
			GROUP BY
				process_id
		) tt
	WHERE
		t > 0
	UNION
		SELECT
			process_info.process_id
		FROM
			process_info
		LEFT JOIN process_status ON process_info.process_id = process_status.process_id
		WHERE
			process_status.process_id IS NULL
)
"""