# Avaliação de Desempenho do Spring PetClinic (Microservices) com Locust

Este projeto tem como objetivo medir e relatar o desempenho básico da aplicação Spring PetClinic (versão microsserviços) utilizando a ferramenta de teste de carga Locust.

O experimento consiste em submeter a aplicação-alvo a três cenários de carga (Leve, Moderado e Pico) e analisar métricas-chave como tempo de resposta, requisições por segundo (RPS) e taxa de falha.

## 1. Tecnologias Utilizadas

* **Aplicação-Alvo:** [Spring PetClinic (Microservices)](https://github.com/spring-petclinic/spring-petclinic-microservices)
* **Contêineres:** Docker e Docker Compose
* **Ferramenta de Teste:** Locust (escrito em Python)
* **Linguagem do Script:** Python 3

## 2. Configuração do Ambiente

Para replicar este experimento, siga os passos abaixo:

### 2.1. Subir a Aplicação (Spring PetClinic)

A aplicação-alvo é executada inteiramente via Docker Compose.

1.  Clone o repositório oficial do Spring PetClinic:
    ```bash
    git clone [https://github.com/spring-petclinic/spring-petclinic-microservices.git](https://github.com/spring-petclinic/spring-petclinic-microservices.git)
    ```
2.  Entre na pasta do projeto e suba os contêineres:
    ```bash
    cd spring-petclinic-microservices
    docker-compose up -d
    ```
3.  Aguarde 1-2 minutos para que todos os microsserviços (Java) iniciem.
4.  Verifique se a aplicação está no ar acessando o API Gateway no navegador: `http://localhost:8080/api/customer/owners` (deve retornar um JSON com a lista de donos).

### 2.2. Configurar o Ambiente de Teste (Locust)

1.  Clone este repositório (o seu projeto).
2.  Instale o Locust:
    ```bash
    pip install locust
    ```

## 3. Plano de Teste

O comportamento do usuário virtual é definido no arquivo `locustfile.py`. O mix de requisições segue a proporção definida no trabalho:

* **40% (`@task(4)`):** `GET /api/customer/owners` (Listar todos os donos)
* **30% (`@task(3)`):** `GET /api/customer/owners/{id}` (Buscar um dono aleatório)
* **20% (`@task(2)`):** `GET /api/vet/vets` (Listar todos os veterinários)
* **10% (`@task(1)`):** `POST /api/customer/owners` (Cadastrar um novo dono com dados aleatórios)

Para evitar falhas em `GET /owners/{id}`, a função `on_start` é usada para buscar a lista de IDs de donos existentes assim que um usuário "nasce".

## 4. Executando os Cenários de Teste

Este repositório inclui 3 scripts `.bat` para executar os cenários de carga. Eles rodam o Locust em modo "headless" (linha de comando) e salvam os resultados automaticamente.

**⚠️ Nota Importante de Configuração:**
Os scripts foram ajustados com uma taxa de "nascimento" (`spawn-rate`) suave (10 ou 20 usuários por segundo) para evitar a sobrecarga imediata da aplicação (que anteriormente causava 100% de falhas na inicialização).

Basta executar os seguintes comandos no seu terminal:

### Cenário A: Leve
* **Descrição:** 50 usuários por 10 minutos (5 repetições).
* **Comando:**
    ```bash
    .\run_leve.bat
    ```

### Cenário B: Moderado
* [cite_start]**Descrição:** 100 usuários por 10 minutos (5 repetições). [cite: 1]
* **Comando:**
    ```bash
    .\run_medio.bat
    ```

### Cenário C: Pico
* [cite_start]**Descrição:** 200 usuários por 5 minutos (5 repetições). [cite: 3]
* **Comando:**
    ```bash
    .\run_pico.bat
    ```

## 5. Resultados

[cite_start]Os resultados de cada repetição são salvos automaticamente na pasta `/results`. [cite: 1, 3, 6]

[cite_start]Cada cenário cria sua própria subpasta (ex: `results/A_leve/`, `results/B_medio/`, `results/C_pico/`), contendo os arquivos CSV para análise posterior. 

## 6. Entregáveis do Trabalho

* **[✓] Repositório:** Contém:
    * `locustfile.py` 
    * `run_leve.bat`, `run_medio.bat`, `run_pico.bat` (scripts de execução)
    * `results/` 
    * `README.md` (este documento)
* **[ ] Vídeo:** Gravação de tela mostrando o setup (Docker), a execução do teste (Locust) e o monitoramento.
* **[ https://www.overleaf.com/read/njqdzchgzzvc#e73a7e] Artigo (Overleaf):** Artigo de 6 páginas (formato IEEE) com a análise dos resultados.
