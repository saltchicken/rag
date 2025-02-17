from rag import Rag
from code_context import CodeContext


if __name__ == "__main__":
    context = CodeContext("../facer", ".py")
    rag = Rag()

    # for function in context.functions:
    #     rag.write_embedding(function["name"], function["docstring"], function['code'])
    # rag.create_table()
    # rag.write_embedding("This is a sentence about people")
    # rag.test_search("I am interested in George Washington")
    rag.search_docstring_embedding('Insert an embedding into the database')
    rag.search_code_snippet_embedding('Insert an embedding into the database')


