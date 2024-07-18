
import streamlit as st

# Título da aplicação
st.title('Bem-vindo ao meu app Streamlit!')

# Entrada de texto para o nome do usuário
nome = st.text_input('Digite seu nome:')

# Botão para exibir a mensagem de boas-vindas
if st.button('Enviar'):
    st.write(f'Olá, {nome}! Seja bem-vindo ao nosso aplicativo.')

# Exibir uma imagem
st.image('https://via.placeholder.com/150', caption='Imagem de exemplo')

# Slider para selecionar um valor
valor = st.slider('Selecione um valor', 0, 100, 50)
st.write(f'Você selecionou: {valor}')

# Título da aplicação
st.title('Bem-vindo ao meu app Streamlit!')

# Entrada de texto para o nome do usuário
nome3 = st.text_input('Digite seu nome:')

# Botão para exibir a mensagem de boas-vindas
if st.button('Enviar'):
    st.write(f'Olá, {nome3}! Seja bem-vindo ao nosso aplicativo.')

# Título da aplicação
st.title('Bem-vindo ao meu app Streamlit!')

# Entrada de texto para o nome do usuário
nome1 = st.text_input('Digite seu nome:')

# Botão para exibir a mensagem de boas-vindas
if st.button('Enviar'):
    st.write(f'Olá, {nome1}! Seja bem-vindo ao nosso aplicativo.')
