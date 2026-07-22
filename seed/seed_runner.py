import csv
from sqlmodel import Session, select, SQLModel  # SQLModel import added for create_all
from database import engine
from models.city import City, CityMetric 

print("Starting Seeding")

def run_seed() :
    print("Function Called")

    # FIX: Tables (city, citymetric) were never being created in Postgres,
    # causing "relation city does not exist" error. This line creates
    # all tables registered under SQLModel.metadata if they don't already exist.
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session : 
        with open(r"seed\cities_seed.csv") as f :  # FIX: raw string to avoid escape issues
            reader = csv.DictReader(f)
            for row in reader :
                stmt = select(City).where(City.name == row["name"])
                city = session.exec(stmt).first()
                if not city : 
                    city = City(
                        name = row["name"],
                        state = row["state"],
                        population = int(row["population"])
                    )
                    session.add(city) 
                    session.commit()
                    session.refresh(city)
                metric = CityMetric(
                    city_id = city.id ,
                    year = int(row["year"]),
                    cost_of_living = float(row["cost_index"]),
                    air_quality_index = float(row["air_index"]),
                    safety_score = float(row["safety_score"]),
                    healthcare_score = float(row["health_score"])
                )
                session.add(metric)
            session.commit()
        print("Seed Complete")
        

if __name__ == "__main__" : 
    run_seed()