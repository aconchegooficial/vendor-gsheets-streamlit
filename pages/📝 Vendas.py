import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pickle as pkl
import pandas as pd

from utils.Constants import *

st.set_page_config(layout="wide")

# ESTABLISHING A GOOGLE SHEETS CONNECTION
conn = st.connection("gsheets", type=GSheetsConnection)

# FETCH EXISTING DATA
existing_data = conn.read(worksheet="VENDAS", usecols=list(range(18)), ttl=5)
existing_data = existing_data.dropna(how="all")

# DISPLAY TITLE AND DESCRIPTION
st.title("Cadastro de Vendas 📝")
st.markdown("### Adicione as informações da venda abaixo:")

with st.form(key="crm_form"):
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("#### Dados Pessoais do Cliente:")
        date = st.date_input(label="Data")
        time = st.time_input(label="Hora")

        name = st.text_input(label="Nome")
        nickname = st.text_input(label="Apelido")
        recurrent = st.selectbox("Recorrência", options=RECURRENT_OPTIONS, index=None)
        phone = st.number_input(label="Telefone", min_value=0, max_value=99999999999)

        if len(phone) < 11:
            phone_validation = True
        else:
            phone = '(' + phone[:2] + ') ' + phone[2:]

    # st.divider()

    with c2:
        st.markdown("#### Dados Geográficos do Cliente:")
        city = st.selectbox("Cidade", options=CITIES, index=None)

        # add = st.selectbox("Advertising", options=CITIES, index=None)
        unity = st.selectbox("Unidade", options=CITIES, index=None)
        cep = st.number_input(label="CEP", min_value=0, max_value=99999999)

    # st.divider()

    with c3:
        st.markdown("#### Informações da Venda:")
        service_id = st.selectbox("Tipo de Serviço", options=SERVICES, index=None)
        sell_value = st.number_input(label="Valor", step=0.01, value=None)
        payied = st.number_input(label="Valor à Vista", step=0.01, value=None)
        comission = st.number_input(label="Comissão", step=0.01, value=None)

        os = st.number_input(label="Ordem de Serviço", step=1, value=None)
            
        add_info = st.text_area(label="Notas Adicionais")

        c3_c1, c3_c2 = st.columns(2, gap="small")

        with c3_c1:
            perfil = st.selectbox("Perfil", options=PERFIL_OPTIONS, index=None)
        with c3_c2:
            whatsapp = st.selectbox("WhatsApp", options=WHATSAPP_OPTIONS, index=None)

    status = st.selectbox("Status", options=STATUS, index=None)

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
                    "Apelido": nickname, 
                    "Recorrência": recurrent,
                    "Telefone": phone,
                    "Cidade": city,
                    "Unidade": unity,
                    "CEP": cep,
                    "Serviço": service_id,
                    "OS": os,
                    "Valor": sell_value,
                    "À Vista": payied,
                    "Comissão": comission,
                    "Descrição": add_info,
                    "WhatsApp": whatsapp,
                    "Perfil": perfil,
                    "Status": status
                }]
            )

            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # UPDATE DATAFRAME ON GOOGLE SHEETS
            conn.update(worksheet="VENDAS", data=updated_df)

            st.success("Nova Venda Cadastrada com Sucesso!")
