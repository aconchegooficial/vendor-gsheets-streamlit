import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

from utils.Constants import *
from services.Database import *
from design.Design import *


# DISPLAY TITLE AND DESCRIPTION
st.title(titles['PAGE TITLE'])
st.markdown(titles['PAGE SUBTITLE'])

conn, existing_data = connection()

st.divider()

with st.form(key="crm_form"):
    st.markdown("#### Dados Pessoais do Cliente:")
    date = st.date_input(label="Data")
    time = st.time_input(label="Hora")

    name = st.text_input(label="Nome")
    phone = st.number_input(label="Telefone", min_value=0, max_value=99999999999)

    st.divider()

    st.markdown("#### Dados Geográficos do Cliente:")
    city = st.selectbox("Cidade", options=CITIES, index=None)
    unity = st.selectbox("Unidade", options=CITIES, index=None)
    cep = st.number_input(label="CEP", min_value=0, max_value=99999999)

    st.divider()

    st.markdown("#### Informações da Venda:")
    service_id = st.selectbox("Tipo de Serviço", options=SERVICES, index=None)
    sell_value = st.number_input(label="Valor", step=0.01, value=None)
    payied = st.number_input(label="Valor à Vista", step=0.01, value=None)
    comission = st.number_input(label="Comissão", step=0.01, value=None)
        
    add_info = st.text_area(label="Notas Adicionais")

    submit_button = st.form_submit_button(label="Cadastrar Venda") 

    if submit_button:
        if not date or not time or not name or not phone:      
            st.warning("Por favor, preencha todos os dados do cliente.")
            st.stop()
        elif not city or not unity or not cep:
            st.warning("Por favor, preencha todos os dados geográficos.")
            st.stop()
        elif not service_id or not sell_value or not payied or not comission:
            st.warning("Por favor, preencha todas as informações de venda.")
            st.stop()
        else:
            vendor_data = pd.DataFrame(
                [{
                    "Data": date.strftime("%d-%m-%Y"),
                    "Horário": time,
                    "Nome": name,
                    "Telefone": phone,
                    "Cidade": city,
                    "Unidade": unity,
                    "CEP": cep,
                    "Serviço": service_id,
                    "Valor": sell_value,
                    "À Vista": payied,
                    "Comissão": comission,
                    "Descrição": add_info
                }]
            )

            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # UPDATE DATAFRAME ON GOOGLE SHEETS
            conn.update(worksheet="DATABASE", data=updated_df)

            st.success("Nova Venda Cadastrada com Sucesso!")
