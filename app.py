from flask import Flask, request, render_template
from sqlalchemy import Table, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

application = Flask(__name__)

engine = create_engine('postgres://siagfnrgwjkkzy:793ca781975fda6951d8633a89b778b99a0106c2a4160e522a538bb888dde26d@ec2-54-235-167-210.compute-1.amazonaws.com:5432/dbdl723nqsshmo', echo=True)
Base = declarative_base(engine)

class Bank(Base):
    metadata = Base.metadata
    __tablename__ = Table('bank_branches', metadata)

    ifsc = Column(String, primary_key=True)
    address = Column(String)
    city = Column(String)
    bank_name = Column(String)
    bank_id = Column(Integer)
    district = Column(String)
    state = Column(String)
    branch = Column(String)

    def __init__(self, ifsc, address, city, bank_name, bank_id, district, state, branch):
        self.ifsc = ifsc
        self.address = address
        self.city = city
        self.bank_name = bank_name
        self.bank_id = bank_id
        self.district = district
        self.state = state
        self.branch = branch

def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@application.route("/ifsc", methods=['GET'])
def return_bank_details():
     bank_ifsc = request.args.get("ifsc")
     if bank_ifsc:
         session = loadSession()
         result = session.query(Bank).filter_by(ifsc=bank_ifsc).first()
         if result:
             return render_template('bank_details.html', result = result)
     return "ERROR: No such bank found!"

@application.route("/getbanks", methods=['GET'])
def return_banks():
     bank_name = request.args.get("bank")
     city = request.args.get("city")

     if bank_name and city:
         session = loadSession()
         result = session.query(Bank).filter_by(bank_name=bank_name).filter_by(city=city).all()
         if result:
             return render_template('banks.html', result = result)
     return "ERROR: No such banks found!"

if __name__ == "__main__":
     application.run()

