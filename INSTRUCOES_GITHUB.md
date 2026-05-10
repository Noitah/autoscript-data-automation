# Como publicar este projeto no seu GitHub

Ter este projeto no seu GitHub é essencial para mostrar aos clientes do Upwork/Workana que você sabe programar e organizar código profissionalmente.

Siga estes passos para publicar o projeto limpo (sanitizado):

## Passo 1: Preparar o repositório no GitHub

1. Acesse sua conta no [GitHub](https://github.com/)
2. Clique no botão verde **"New"** (Novo repositório)
3. Preencha os dados:
   - **Repository name:** `autoscript-data-automation` (ou outro nome profissional)
   - **Description:** `Plataforma desktop em Python para automação de dados, extração de PDFs e conciliação financeira.`
   - **Public/Private:** Escolha **Public** (para que clientes possam ver)
   - Não marque as opções de adicionar README ou .gitignore (nós já temos)
4. Clique em **"Create repository"**

## Passo 2: Enviar os arquivos do seu computador

Abra o terminal (Prompt de Comando ou Git Bash) na pasta onde você extraiu o projeto limpo e digite os seguintes comandos:

```bash
# 1. Inicializar o repositório local
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Criar o primeiro commit
git commit -m "Commit inicial: Plataforma de automação de dados"

# 4. Conectar com o repositório que você criou no GitHub
# (Substitua SEU_USUARIO pelo seu nome de usuário no GitHub)
git remote add origin https://github.com/SEU_USUARIO/autoscript-data-automation.git

# 5. Mudar o nome da branch principal para main (padrão atual)
git branch -M main

# 6. Enviar os arquivos para o GitHub
git push -u origin main
```

## Passo 3: Destacar no seu perfil

1. Vá até o seu perfil do GitHub
2. Clique em **"Customize your pins"** (Personalizar seus pins)
3. Selecione este repositório para que ele fique em destaque na sua página inicial

## Dica de Ouro para Freelancers 💡

Quando for enviar uma proposta no Upwork ou Workana para um trabalho de automação de Excel ou PDF, inclua o link deste repositório dizendo:

> *"Tenho experiência prática com automação de dados complexos. Recentemente desenvolvi uma plataforma completa em Python que automatiza conciliação financeira e extração de PDFs. Você pode ver a qualidade e organização do meu código no meu GitHub: [LINK DO REPOSITÓRIO]"*

Isso te coloca na frente de 90% dos concorrentes que não mostram código real!
