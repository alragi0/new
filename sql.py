from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# تكوين اتصال قاعدة البيانات (استخدم معلومات الاتصال الخاصة بك)
db_url = "mysql://root:mTor5MxStNrF2lBm64EH@containers-us-west-157.railway.app:6763/railway"  # استبدل هذا بمعلومات الاتصال الخاصة بك

engine = create_engine(db_url)

# تعريف جلسات SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# إنشاء قاعدة الجدول
Base = declarative_base()

class SessionTable(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)

# إنشاء الجدول إذا لم يكن موجودًا بالفعل
Base.metadata.create_all(engine)
