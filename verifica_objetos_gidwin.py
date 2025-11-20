import os
import re
import pyodbc
import shutil
import glob
from dotenv import load_dotenv

load_dotenv()

def conectar_bd_sql_server():
    try:
        conexao = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={os.getenv('SQL_SERVER')};"
            f"DATABASE={os.getenv('SQL_DATABASE')};"
            f"Trusted_Connection={os.getenv('SQL_TRUSTED_CONNECTION')};"
        )
        return conexao.cursor()
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None

def listar_arquivos_mxl(diretorio):
    try:
        return [f for f in os.listdir(diretorio) if f.endswith(".xml.err")]
    except FileNotFoundError:
        print(f"Directory not found: {diretorio}")
        return []

def extrair_parte_do_nome(arquivo):
    padrao = r"_([\w\d]+)\.xml\.err"
    match = re.search(padrao, arquivo)
    return match.group(1) if match else None

diretorio_share = os.getenv("DIRETORIO_SHARE")
diretorio_destino = os.getenv("DIRETORIO_DESTINO")
diretorio_tratado = os.getenv("DIRETORIO_TRATADO")
source_dir = os.getenv("SOURCE_DIR")
destination_dir = os.getenv("DESTINATION_DIR")

arquivos_mxl = listar_arquivos_mxl(diretorio_share)

for arquivo in arquivos_mxl:
    parte_do_nome = extrair_parte_do_nome(arquivo)
    if parte_do_nome:
        cursor = conectar_bd_sql_server()
        print(f"Nome do arquivo: {arquivo}, Parte do objeto: {parte_do_nome}")

        consulta_sql = f"SELECT * FROM tb_DeclaracoesDAR with (nolock) WHERE documentoTransporte = '{parte_do_nome}'"
        consulta_sql_other = f"select * from PRO_DU31 with(nolock) where d31_lopt = '{parte_do_nome}'"

        print(consulta_sql)

        cursor.execute(consulta_sql)
        resultado = cursor.fetchone()

        if not resultado:
            print(consulta_sql_other)
            cursor.execute(consulta_sql_other)
            resultado_other = cursor.fetchone()
            print(f"A parte do objeto '{parte_do_nome}' não foi encontrada na tabela.")

            if not resultado_other:
                shutil.move(
                    os.path.join(diretorio_share, arquivo),
                    os.path.join(diretorio_destino, arquivo),
                )
                print(f"Ficheiro '{arquivo}' enviado para Backup.")

                files = glob.glob(os.path.join(source_dir, f"*{parte_do_nome}*"))
                if files:
                    for file in files:
                        shutil.move(file, destination_dir)
                else:
                    print(
                        f"Nenhum arquivo contendo '{parte_do_nome}' foi encontrado em {source_dir}."
                    )
            else:
                print(f"A parte do objeto '{parte_do_nome}' foi encontrada na tabela.")
                shutil.move(
                    os.path.join(diretorio_share, arquivo),
                    os.path.join(diretorio_tratado, arquivo),
                )
                print(f"Ficheiro '{arquivo}' enviado para Tratado.")
        else:
            print(f"A parte do objeto '{parte_do_nome}' foi encontrada na tabela.")
            shutil.move(
                os.path.join(diretorio_share, arquivo),
                os.path.join(diretorio_tratado, arquivo),
            )
            print(f"Ficheiro '{arquivo}' enviado para Tratado.")

        cursor.close()
    else:
        print(f"Nome do arquivo: {arquivo}, Parte do objeto não encontrada.")