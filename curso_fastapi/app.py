from fastapi import FastAPI
from http import HTTPStatus
# from fastapi.responses import HTMLResponse
from curso_fastapi.schemas import Message


app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}

# ATIVIDADE_AULA-02
# @app.get('/hello', response_class=HTMLResponse)
# def page_welcome():
#     return """
#             <html>
#                 <head>
#                     <title> Nosso olá mundo!</title>
#                 </head>
#                 <body>
#                     <h1> Olá Mundo </h1>
#                 </body>
#             </html>
#         """
