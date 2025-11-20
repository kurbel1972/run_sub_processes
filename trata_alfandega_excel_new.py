import os
import pandas as pd
import cx_Oracle
import shutil
from dotenv import load_dotenv

load_dotenv()

# Diretório onde os arquivos Excel estão localizados
diretorio = os.getenv("DIRETORIO_EXCEL")
padrao_nome_arquivo = os.getenv("PADRAO_NOME_ARQUIVO")

# Configurações da conexão Oracle
user = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")
dsn = os.getenv("ORACLE_DSN")
lib_dir_base = os.getenv("ORACLE_LIB_DIR")

oracle_client_iniciado = False

for nome_arquivo in os.listdir(diretorio):
    print("Verifica se o arquivo atende ao padrão desejado")
    if nome_arquivo.startswith(padrao_nome_arquivo):
        try:
            print("Lê o arquivo Excel em um DataFrame")
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)

            df = pd.read_excel(
                caminho_arquivo,
                usecols="A:A",
                header=None,
                skiprows=0,
                names=["A"],
            )

            print("Oracle Client a iniciar...")

            if not oracle_client_iniciado:
                cx_Oracle.init_oracle_client(lib_dir=lib_dir_base)
                oracle_client_iniciado = True

            with cx_Oracle.connect(user, password, dsn) as connection:
                with connection.cursor() as cursor:
                    print("Oracle Client iniciado...")

                    delete_rows = "delete eiusr.teste_tempo"
                    cursor.execute(delete_rows)

                    for indice, linha in df.iterrows():
                        print(f"Dados da linha {indice + 1}:", end=" ")
                        print(" ".join(map(str, linha.tolist())))
                        print("\n" + "-" * 50 + "\n")

                        print(f"Dados da linha {indice + 1} (valores individuais):")
                        for coluna, valor in linha.items():
                            print(f"{coluna}: {valor}")
                        print("\n" + "-" * 50 + "\n")

                        insert_query = f"INSERT INTO eiusr.teste_tempo (seccao) VALUES ('{linha['A']}')"
                        print(insert_query)
                        cursor.execute(insert_query)

                    connection.commit()

                    update_data = "update eiusr.triiaob set situacao = '3' where  situacao in ('2','1','4') and s10 in (select seccao from eiusr.teste_tempo)"
                    cursor.execute(update_data)
                    connection.commit()

        except Exception as e:
            print(f"Erro ao processar o arquivo {nome_arquivo}: {e}")
        else:
            novo_caminho_arquivo = os.path.join(diretorio, "Processados", nome_arquivo)
            shutil.move(caminho_arquivo, novo_caminho_arquivo)
            print(f"Arquivo {nome_arquivo} movido para o diretório Processados.")