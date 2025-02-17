from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer

Base = declarative_base()

class Embedding(Base):
    __tablename__ = "facer_rag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    function_name = Column(String, nullable=False)
    docstring = Column(String, nullable=True)
    docstring_embedding = Column(Vector(384), nullable=True)
    code_snippet = Column(String, nullable=False)
    code_snippet_embedding = Column(Vector(384), nullable=False)

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

    def write_embedding(self, function_name, docstring, code_snippet):
        function_name_embedding = self.model.encode(function_name)
        if docstring:
            docstring_embedding = self.model.encode(docstring).tolist()
        else:
            docstring_embedding = None
        code_snippet_embedding = self.model.encode(code_snippet).tolist()

        code_entry = Embedding(function_name=function_name,
                               docstring=docstring,
                               docstring_embedding=docstring_embedding,
                               code_snippet=code_snippet,
                               code_snippet_embedding=code_snippet_embedding)
        self.session.add(code_entry)
        self.session.commit()

    def search_docstring_embedding(self, query):
        query_embedding = self.model.encode(query)
        query_vector = query_embedding.tolist()

        stmt = select(Embedding).order_by(Embedding.docstring_embedding.l2_distance(query_vector)).limit(2)
        results = self.session.execute(stmt).scalars().all()

        for res in results:
            print(res.function_name, res.code_snippet)

    def search_code_snippet_embedding(self, query):
        query_embedding = self.model.encode(query)
        query_vector = query_embedding.tolist()

        stmt = select(Embedding).order_by(Embedding.code_snippet_embedding.l2_distance(query_vector)).limit(2)
        results = self.session.execute(stmt).scalars().all()

        for res in results:
            print(res.function_name, res.code_snippet)

    # def test_search(self, text):
    #     embedding = self.model.encode(text)
    #
    #     query_vector = embedding.tolist()
    #     stmt = select(Embedding).order_by(Embedding.vector.l2_distance(query_vector)).limit(5)
    #     results = self.session.execute(stmt).scalars().all()
    #
    #     for res in results:
    #         print(res.id, res.name)

