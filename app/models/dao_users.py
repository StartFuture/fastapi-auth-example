import logging

from psycopg2 import sql
from pydantic import EmailStr

from app import parameters
from app.models.dao_pg import DataBasePG
from app.schemas.user import NewUser

class UserDao:

    @staticmethod
    def get_user_data_by_id(id_user: int):

        query = sql.SQL(
            '''
            select username, id_user, email from public.users
            where id_user = {id_user}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return cursor.fetchone()
    

    @staticmethod
    def get_user_recover(email: EmailStr):

        query = sql.SQL(
            '''
            select username, id_user, email, right(password_user, 6)
            from public.users
            where
            email = {email}
            ;
            '''
        ).format(
            email=sql.Literal(email)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return cursor.fetchone()
            

    @staticmethod
    def get_user_by_email(email: EmailStr):

        query = sql.SQL(
            '''
            select id_user, email, password_user
            from public.users
            where
            email = {email}
            ;
            '''
        ).format(
            email=sql.Literal(email)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return cursor.fetchone()


    @staticmethod
    def get_user_by_id(id_user: str):

        query = sql.SQL(
            '''
            select id_user, email, password_user
            from public.users
            where
            id_user = {id_user}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return True

    @staticmethod
    def register_user(username, email, password_hash):

        query = sql.SQL(
            '''
            INSERT INTO public.users
            (
                username,
                email,
                password_user
            )
            VALUES(
                {username},
                {email},
                {password_user}
            )
            ;
            '''
        ).format(
            username=sql.Literal(username),
            email=sql.Literal(email),
            password_user=sql.Literal(password_hash)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return True
    

    @staticmethod
    def update_password(new_password: str, id_user: int):

        query = sql.SQL(
            '''
            UPDATE public.users
            SET 
            password_user={new_password}
            WHERE 
            id_user={id_user}
            ;
            '''
        ).format(
            new_password=sql.Literal(new_password),
            id_user=sql.Literal(id_user)
        )

        with DataBasePG(
                hostname=parameters.DB_PG_HOST,
                username=parameters.DB_PG_USERNAME,
                port=parameters.DB_PG_PORT,
                password=parameters.DB_PG_PASSWORD,
                db=parameters.DB_PG_DATABASE,
                schema=parameters.DB_PG_SCHEMA
                ) as cursor:

            try: 
                    
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return True


