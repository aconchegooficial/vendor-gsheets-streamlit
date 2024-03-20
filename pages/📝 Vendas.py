import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pickle as pkl
import pandas as pd

from utils.Constants import *

# =============================================================================================== #

st.set_page_config(layout="wide")


# ======================== CONECTIONS ======================== #
# ESTABLISHING A GOOGLE SHEETS CONNECTION
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="VENDAS", usecols=list(range(18)), ttl=5)
existing_data = existing_data.dropna(how="all")

# ======================== DASHBOARD LAYOUT ======================== #
# DISPLAY TITLE AND DESCRIPTION
st.title("Cadastro de Vendas 📝")
st.markdown("### Adicione as informações da venda abaixo:")

# ======================== EXTERNAL IMPORTS ======================== #
with open("utils/city_to_unity.pkl", "rb") as f: 
    city_to_unity = pkl.load(f)

# CONTROL COMMANDS
phone_validation = False
cep_validation = False

main_container = st.container(border=True)

with main_container:
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
            st.markdown("#### Dados Pessoais do Cliente:")
            date = st.date_input(label="Data")
            time = st.time_input(label="Hora", step=60)

            name = st.text_input(label="Nome")
            nickname = st.text_input(label="Apelido")
            recurrent = st.selectbox("Recorrência", options=RECURRENT_OPTIONS, index=None)
            phone = st.number_input(label="Telefone", min_value=0, max_value=99999999999, value=None)
            st.text("Ex: 31998765432")

            if phone != None:
                phone = str(phone)
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
            cep = st.number_input(label="CEP", min_value=0, max_value=99999999, value=None)
            
            if cep != None:
                cep = str(cep)
                if len(cep) < 8:
                    cep_validation = True
                else:
                    cep = cep[:2] + '.' + cep[2:5] + '-' + cep[5:]

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

    submit_button = st.button(label="Cadastrar Venda") 

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
        elif phone_validation:
            st.warning("Por favor, informe o DDD no campo de telefone.")
            st.stop()
        elif cep_validation:
            st.warning("Por favor, insira um CEP valido.")
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
