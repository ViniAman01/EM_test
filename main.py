from classes.school import SchoolOperations
from classes.driver import DriverOperations

if __name__ == "__main__":
    try:
        number_schools = int(input("Digite um número de escolas para registrar no arquivo CSV (-1 para registrar todas as escolas do banco): "))
        assert number_schools >= -1
        type_school = int(input("\nDigite o tipo de escola:\n>Pública[0]\n>Privada[1]\n>Pública e Privada[2]\n: "))
        assert type_school >= 0 and type_school <= 2
    except AssertionError:
        print("\nValor fora de intervalo.")
        exit()

    types_schools = ['Public','Private','Public Private']

    driver_chrome = DriverOperations()
    driver_chrome.start_driver()

    school = SchoolOperations(driver_chrome.driver)
    school.search_school(number_schools,types_schools[type_school])
