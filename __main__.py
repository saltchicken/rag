from rag import Rag


if __name__ == "__main__":
    rag = Rag()
    # rag.create_table()
    # rag.write_embedding("This is a sentence about people")
    rag.test_search("I am interested in George Washington")


