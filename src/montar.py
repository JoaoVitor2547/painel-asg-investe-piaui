"""Junta src/template.html + dados/dados.json + logotipo e grava index.html (o painel, em um unico arquivo).
Uso: python3 src/montar.py   (rodar a partir da raiz do repositorio)"""
import base64
t = open('src/template.html', encoding='utf-8').read()
d = open('dados/dados.json', encoding='utf-8').read().replace('</', '<\\/')   # nao deixa os dados fecharem a tag <script>
logo = 'data:image/png;base64,' + base64.b64encode(open('assets/logo-investe-piaui.png', 'rb').read()).decode()
corpo = t.replace('/*DATA*/', d).replace('/*LOGO*/', logo)
open('build_fragmento.html', 'w', encoding='utf-8').write(corpo)             # versao sem <head>, usada so para pre-visualizacao
cabeca, resto = corpo.split('<header', 1)
pagina = ('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
          + cabeca + '</head>\n<body>\n<header' + resto + '\n</body>\n</html>\n')
open('index.html', 'w', encoding='utf-8').write(pagina)
print('index.html gerado:', len(pagina), 'bytes')
