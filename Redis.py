import redis

# 데이터베이스(redis)에 접속
# 이제 연결을 해제할 필요가 없음
# host 와 port 를 사용해서 연결
with redis.StrictRedis(host = 'localhost', port = 6379) as conn:
    # 문자열 저장
    # 결과가 redis에 반영됨
    conn.set("name" , "종호")
    # 문자열 가져오기
    # 메모리에 인코딩 되어서 저장되기에 bytes로 리턴
    data = conn.get("name")
    # '종호' 가 아니라 b'\xec\...' 가 출력됨
    # 인코딩 결과가 출력됨
    print(data)
    # 한글로 출력하기 위해 decode 처리
    print(data.decode('utf-8'))

# Connection Pool 을 이용한 접속
# 결과는 이전과 같음
redis_pool = redis.ConnectionPool(host = 'localhost', port = 6379,
                                  max_connections = 3)
with redis.StrictRedis(connection_pool= redis_pool) as conn:
    conn.set("name" , "종호")
    data = conn.get("name")
    print(data)
    print(data.decode('utf-8'))

    # 만료 시간 설정 가능
    conn.set("name", "종호", 10) # 만료시간이 10초
    # 만료 시간 확인
    # 10초이므로 10이 출력됨
    print(conn.ttl("name"))


    # 먼저 데이터를 사용하고 그 후에 만료 시간을 설정
    conn.set("age", 25)
    conn.expire("age", 10) # 만료시간 10초
    # b'25' 가 정상적으로 출력됨
    print(conn.get("age"))
    # 10초가 지난 후에 다시 출력
    time.sleep(10)
    # 만료 시간이 지난 데이터를 출력하므로 데이터가 없어서 None 이 출력됨
    print(conn.get("age"))


    # 리스트에 데이터를 저장
    conn.rpush("students", "stu1")
    conn.lpush("students", "stu2") # lpush 를 해서 가장 앞(왼쪽)으로 감
    conn.rpush("students", "stu3")

    # 리스트에 저장된 데이터 가져오기
    for stu in conn.lrange("students", 0, -1):
        print(stu) # stu2, stu1, stu3 순서대로 출력