# 🎮 Jogo Geográfico Experimental — Mapa Maluco

Jogo educacional e experimental baseado em mapas interativos, dados climáticos reais e sistemas de decisão que **não revelam sua lógica interna**.



## 🧩 Sobre o Projeto

**Mapa Maluco** é um jogo geográfico experimental desenvolvido para web, no qual o jogador explora mapas, desenha áreas, interage com pontos e interpreta mapas de calor gerados a partir de dados reais e curiosidades aparentemente irrelevantes.

O sistema reage às ações do jogador, mas **não explica como toma decisões**, incentivando exploração, pensamento crítico e interpretação espacial.



## 🎯 Objetivo do Jogo

- Explorar mapas interativos
- Interpretar padrões espaciais
- Tomar decisões sem conhecer as regras explícitas
- Aprender geografia, clima e território de forma lúdica

> O jogo não busca respostas corretas, mas estimular a observação e a curiosidade.



## 🧠 Conceito Central

- Uso de **dados reais** (clima, localização)
- Apresentação lúdica e ambígua das informações
- Sistema de decisão invisível ao jogador
- Consequências visuais e narrativas, não numéricas



## 🗺️ Mecânicas Principais

### 🧭 Exploração do Mapa
- Navegação livre
- Zoom e deslocamento
- Alternância entre mapas base

### ✏️ Seleção de Área
- Desenho de polígonos interativos
- Seleção de regiões específicas
- Áreas influenciam eventos e análises

### 📍 Pontos de Interesse
- Marcadores no mapa
- Curiosidades irrelevantes
- Feedbacks enigmáticos do sistema

### 🔥 Heatmap (Mapa de Calor)
- Representação visual de influência climática ou presença
- Sem valores numéricos explícitos
- Interpretação subjetiva pelo jogador



## 🌦️ Dados Utilizados

### 📆 Clima do Dia Anterior
- Temperatura média
- Cobertura média de nuvens
- Dados obtidos via API climática

Esses dados influenciam:
- Intensidade do heatmap
- Aparição de eventos
- Respostas do sistema



## 🗺️ Mapas Base

### 🗺️ OpenStreetMap
- Contexto urbano
- Ruas, bairros e pontos de referência

### 🛰️ Satélite
- Visualização ambiental
- Ideal para análise territorial

📌 As **camadas de dados dependem do mapa base selecionado**.



## 🎛️ Camadas de Dados

| Camada    | Função no Jogo         |
| --------- | ---------------------- |
| Pontos    | Eventos e curiosidades |
| Polígonos | Áreas de decisão       |
| Heatmap   | Influência invisível   |

O jogador pode ativar ou desativar camadas livremente.



## 🧠 Sistema de Decisão Oculta

O jogo possui um motor interno que considera:
- Localização geográfica
- Tamanho e forma do polígono
- Intensidade do mapa de calor
- Histórico de interações

⚠️ A lógica **não é revelada ao jogador**.



## 🎮 Experiência do Jogador

O jogo estimula:
- Exploração livre
- Tentativa e erro
- Interpretação visual
- Aprendizado indireto

Não há:
- Pontuação explícita
- Caminhos lineares
- Respostas claramente corretas



## 📚 Aplicações Educacionais

- Geografia urbana
- Sensoriamento remoto
- Clima e meio ambiente
- Pensamento espacial
- Jogos sérios (serious games)



## ⚠️ Limitações

- Dados climáticos são aproximados
- Não substitui análises científicas
- Foco em experiência lúdica, não precisão técnica



## 🔮 Possíveis Evoluções

- Modos de jogo (exploração, desafio, mistério)
- Narrativa procedural
- Ranking oculto
- Integração completa com Google Earth Engine
- Eventos temporais automáticos



## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Folium
- APIs Climáticas
- Dados Geoespaciais



## 📝 Observação Final

> Este jogo não ensina respostas.  
> Ele ensina a **olhar para o espaço de outra forma**.

A lógica existe, mas não precisa ser compreendida para que o aprendizado aconteça.
