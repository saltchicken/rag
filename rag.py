from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer

Base = declarative_base()

class Embedding(Base):
    __tablename__ = "rag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    vector = Column(Vector(384))

class Rag():
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.db = "postgres"
        DATABASE_URL = f"postgresql://postgres@10.0.0.7:5432/{self.db}"
        self.engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def create_table(self):
        Base.metadata.create_all(self.engine)

    def write_embedding(self, text):
        embedding = self.model.encode(text)
        new_embedding = Embedding(name=text, vector=embedding.tolist())
        self.session.add(new_embedding)
        self.session.commit()


    def test_search(self, text):
        embedding = self.model.encode(text)

        query_vector = embedding.tolist()
        stmt = select(Embedding).order_by(Embedding.vector.l2_distance(query_vector)).limit(5)
        results = self.session.execute(stmt).scalars().all()

        for res in results:
            print(res.id, res.name)

