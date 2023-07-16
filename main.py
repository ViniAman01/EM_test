from classes.school import SchoolOperations
from classes.driver import DriverOperations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# try:
#     number_schools = int(input("Digite um número de escolas para registrar no arquivo CSV (-1 para registrar todas as escolas do banco): "))
#     assert number_schools >= -1
#     type_school = int(input("\nDigite o tipo de escola:\n>Pública[0]\n>Privada[1]\n>Pública e Privada[2]\n: "))
#     assert type_school >= 0 and type_school <= 2
# except AssertionError:
#     print("\nValor fora de intervalo.")
#     exit()

class SearchInfo(BaseModel):
    type_school: str
    number_schools: int

@app.post("/receber-opcao")
async def executar_back(search_info: SearchInfo): 
    driver_chrome = DriverOperations()
    driver_chrome.start_driver()

    school = SchoolOperations(driver_chrome.driver)
    school.search_school(search_info.number_schools,search_info.type_school)
    return {"message": "Ação executada com sucesso"}
