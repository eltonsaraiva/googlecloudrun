
import streamlit as st
import pandas as pd

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridOptionsBuilder, GridUpdateMode, DataReturnMode


# Função que retorna o index do primeiro valor não nulo da Segunda coluna de uma planilha
def planilha_corte(df):
    # iloc retorna todas as linhas a coluna indice=1
    # isna retorna True se a linha é NaN
    # Verifica o menor valor da linha e retorna seu indice
    
    i = df.iloc[:,1].isna().idxmin()
    
    df.columns = df.iloc[i]
    df = df.iloc[i+1:]
    df.reset_index(drop=True, inplace=True)
    
    return df

def colunas_repetidas(df):
    col_repetidas_lista = []
    for i in df.keys():
        col_repetidas_lista.extend(df[i].columns.to_list())
        
    col_repetidas_lista = ["serial number" if item == "SERIAL_NR" else item for item in col_repetidas_lista]
    return list(set([item for item in col_repetidas_lista if col_repetidas_lista.count(item) > 1]))


def colunas_repetidas_lista(lista1, lista2):
    lista_1 = ["serial number" if item == "SERIAL_NR" else item for item in lista1]
    lista_1 = ["guid_name" if item == "GUID" else item for item in lista_1]

    lista_2 = ["serial number" if item == "SERIAL_NR" else item for item in lista2]
    lista_2 = ["guid_name" if item == "GUID" else item for item in lista_2] 

    colunas_compilada = lista_1 + lista_2

    return list(set([item for item in colunas_compilada if colunas_compilada.count(item) > 1]))



st.set_page_config(
    layout='wide',
    page_title='Analisador APPLE_DC',
    page_icon=':apple:'
)

table_styles=[
    dict(selector="td", props="font-size: 0.8em; text-align: right"),
    dict(selector="th", props="font-size: 0.8em; "),
    dict(selector='tr:hover', props='background-color: grey')
]



# Título da aplicação
st.title('Analisador APPLE_DC')

file_data = st.file_uploader('Carregue aqui o arquivo: ', type='xlsx', help='Adicione somente a planilha')

if file_data is not None:

    df = pd.read_excel(file_data, sheet_name=None)

    for x in df.keys():
        
        df[x] = planilha_corte(df[x])

    tab_nomes = [str(x) for x in df.keys()]
    tabs = st.tabs(tab_nomes)
    


    # CRIAÇÃO DO TAB -------------------------
    for tab, column_name in zip(tabs, df.keys()):
        with tab:
            st.subheader(f"Planilha nome - {column_name}")

            gb = GridOptionsBuilder.from_dataframe(df[column_name])
            
            gridOptions = gb.build() 
            column_defs = gridOptions["columnDefs"]
            for col_def in column_defs:
                col_name = col_def["field"]
                max_len = 300 # can add +5 here if things are too tight
                #col_def["width"] = max_len          
                #col_def['suppressSizeToFit'] = False
                
            gridOptions["autoSizeStrategy"] = {'type':'fitGridWidth',
                                               'defaultMinWidth': 200,
                                               'columnLimits':{
                                                   'minWidth': 900,
                                               }
                                               }
            
            AgGrid(df[column_name],
                   gridOptions=gridOptions )  # Example: display the column data
    # TERMINO DA CRIAÇÃO DO TAB --------------

    
    
    st.markdown("---")
    on_planilha_cruzada = st.toggle('Planilhas Cruzadas')

    if on_planilha_cruzada:
        st.subheader('Planilhar Cruzada')

        nomes_planilhas = df.keys()

        col1, col2 = st.columns(2)

        nome_planilha_selecionada = col1.selectbox('Escolha a 1ª Planilha: ',
                                                options=nomes_planilhas,
                                                    help='Escolha uma das planilhas carregadas',
                                                    key='select11',
                                                    index=None,
                                                    placeholder='Selecione uma planilha',
                                                    )
                

        nome_planilha_selecionada2 = col2.selectbox('Escolha a 2ª Planilha: ', 
                                                    options=nomes_planilhas,
                                                    help='Escolha uma das planilhas carregadas',
                                                    key='select22',
                                                    index=None,
                                                    placeholder='Selecione uma planilha para cruzar'
                                                    )

        if nome_planilha_selecionada and nome_planilha_selecionada2:
            if nome_planilha_selecionada == nome_planilha_selecionada2:
                st.warning('Escolha planilhas diferentes.', icon="⚠️")
                st.stop()

            if nome_planilha_selecionada2:

                col_repetidas = colunas_repetidas_lista(df[nome_planilha_selecionada].columns.to_list(),
                                                df[nome_planilha_selecionada2].columns.to_list())

                if col_repetidas == []:
                    st.warning('Não existem colunas iguais nas duas planilhas.', icon="⚠️")
                    st.stop()
                
                col1, col2 = st.columns(2)

                # coluna_selecionada = col1.selectbox('Escolha uma coluna: ',
                #                                   # options=df[nome_planilha_selecionada].columns.to_list() + df[nome_planilha_selecionada2].columns.to_list(),
                #                                   options = col_repetidas,
                #                                   # default=df[nome_planilha_selecionada].columns.to_list()[0],
                #                                   # index=None,
                #                                   placeholder='Selecione uma coluna',
                #                                   )
                
                #col2.markdown(f'\nColunas iguais/semelhantes {col_repetidas}')


                
                df[nome_planilha_selecionada] = df[nome_planilha_selecionada].rename(columns={'SERIAL_NR': 'serial number',
                                                                        'GUID': 'guid_name'})
                df[nome_planilha_selecionada2] = df[nome_planilha_selecionada2].rename(columns={'SERIAL_NR': 'serial number',
                                                                        'GUID': 'guid_name'})
                

                df_merged2 = df[nome_planilha_selecionada].merge(df[nome_planilha_selecionada2],
                                                                left_on=col_repetidas[0],
                                                                right_on=col_repetidas[0],
                                                                how='outer'
                                                                )
                
                coluna_index = col2.multiselect('Escolha uma coluna para Ordenar: ',
                                                # options=df[nome_planilha_selecionada].columns.to_list() + df[nome_planilha_selecionada2].columns.to_list(),
                                                options = df_merged2.columns ,
                                                default=col_repetidas[0],
                                                # index=None,
                                                placeholder='Selecione uma coluna',
                                                )
                

                if coluna_index:
                    st.subheader('')
                    print(df_merged2)
                    df_merged2 = df_merged2.set_index(coluna_index)
                    st.dataframe(df_merged2)

                else:

                    st.subheader('Planilha Cruzada else')
                    print(df_merged2)
                    st.dataframe(df_merged2)

    st.markdown("---")
    on_identificadores = st.toggle('Identificadores')

    if on_identificadores:
        identificador_imei = list(df['Device Key']['IMEI'])

        identificador_imei_selecao = st.selectbox('Selecione o IMEI',
            options=identificador_imei,
            index=None,
            help='Selecione um IMEI para começar',
            placeholder='Selecione',
        )
        
        if identificador_imei_selecao:
            #st.dataframe(df['Device Key'][df['Device Key']['IMEI'] == identificador_imei_selecao])
            st.markdown(f'Serial number: {df["Device Key"][df["Device Key"]["IMEI"] == identificador_imei_selecao]["SERIAL_NR"].values[0]}')
            st.markdown(f'GUID: {df["Device Key"][df["Device Key"]["IMEI"] == identificador_imei_selecao]["GUID"].values[0]}')
        

  
