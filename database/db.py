from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import aiomysql
import os

load_dotenv()

class MySQLDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect_to_support(self):
        db_host = os.getenv("MYSQL_HOST")
        db_port = int(os.getenv("MYSQL_PORT", 3306))
        db_user = os.getenv("MYSQL_USERNAME")
        db_password = os.getenv("MYSQL_PASSWORD")
        db_database = 'transfers'
        
        use_ssh = os.getenv("USE_SSH") == "True"
        pool = None

        self.use_ssh = use_ssh

        if use_ssh:  
            ssh_host = os.getenv("SSH_HOST")
            ssh_port = int(os.getenv("SSH_PORT", 22))
            ssh_user = os.getenv("SSH_USERNAME")
            ssh_password = os.getenv("SSH_PASSWORD")

            self.ssh_tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_host, db_port)
            )
            self.ssh_tunnel.start() 
            local_bind_port = self.ssh_tunnel.local_bind_port
            print(f"SSH tunnel established successfully: {local_bind_port}")

            self.pool = await aiomysql.create_pool(
                host='127.0.0.1',
                port=local_bind_port,
                user=db_user,
                password=db_password,
                db=db_database,
                autocommit=True
            )
        else:
            self.pool = await aiomysql.create_pool(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                db=db_database,
                autocommit=True
            )

    async def connect(self): 
        db_host = os.getenv("MYSQL_HOST")
        db_port = int(os.getenv("MYSQL_PORT", 3306))
        db_user = os.getenv("MYSQL_USERNAME")
        db_password = os.getenv("MYSQL_PASSWORD")
        db_database = os.getenv("DATABASE_NAME")
        use_ssh = os.getenv("USE_SSH") == "True"
        pool = None

        self.use_ssh = use_ssh

        if use_ssh:  
            ssh_host = os.getenv("SSH_HOST")
            ssh_port = int(os.getenv("SSH_PORT", 22))
            ssh_user = os.getenv("SSH_USERNAME")
            ssh_password = os.getenv("SSH_PASSWORD")

            self.ssh_tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_host, db_port)
            )
            self.ssh_tunnel.start()  
            local_bind_port = self.ssh_tunnel.local_bind_port
            print(f"SSH tunnel established successfully: {local_bind_port}")

            self.pool = await aiomysql.create_pool(
                host='127.0.0.1',
                port=local_bind_port,
                user=db_user,
                password=db_password,
                db=db_database,
                autocommit=True
            )
        else:
            self.pool = await aiomysql.create_pool(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                db=db_database,
                autocommit=True
            )

    async def close(self):
        self.pool.close()
        if self.use_ssh:  
            self.ssh_tunnel.stop()  
        await self.pool.wait_closed()

    async def execute_query(self, query, params=None, as_dict=False):
        cursor_type = aiomysql.DictCursor if as_dict else aiomysql.Cursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor_type) as cur:
                print("Executing SQL query:")
                print("SQL:", cur.mogrify(query, params))
                await cur.execute(query, params)
            await conn.commit()
    
    async def execute_query_select(self, query, params=None, as_dict=None):
        cursor_type = aiomysql.DictCursor if as_dict else aiomysql.Cursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor_type) as cur:
                print("Executing SQL query:")
                print("SQL:", cur.mogrify(query, params))
                await cur.execute(query, params)
                return await cur.fetchall()

database = MySQLDatabase()

