from rag import Rag
from code_context import CodeContext


if __name__ == "__main__":
    context = CodeContext("../code_context", ".py")
    rag = Rag()

    # for function in context.functions:
    #     rag.write_embedding(function["name"], function["docstring"], function['code'])
    # rag.create_table()
    # rag.write_embedding("This is a sentence about people")
    # rag.test_search("I am interested in George Washington")
    rag.search_docstring_embedding('What function can I use to discard directories that I have specified as not needed')
    rag.search_code_snippet_embedding('What function can I use to discard directories that I have specified as not needed')


