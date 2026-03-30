from sqlalchemy import create_engine, MetaData

# Crear un motor de base de datos
engine = create_engine("mysql+pymysql://localhost:localhost@localhost:3306/app_login_register_fastapi")

# Crear los meta datos
meta_data = MetaData()