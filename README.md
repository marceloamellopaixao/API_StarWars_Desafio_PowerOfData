# Documentação da API RESTful - Star Wars

## Descrição
Esta API RESTful permite consultar informações sobre o universo Star Wars usando dados da SWAPI (Star Wars API). Ela foi desenvolvida em Python com o framework Flask e utiliza JWT para autenticação. A API fornece endpoints para consultar filmes, personagens, planetas e naves estelares, além de gerar estatísticas relacionadas a esses dados.


---

## Desenvolvedor
Criado por Marcelo Augusto em 11/2024

---

## Links Úteis

[Aplicação API Funcional - Hospedada na AWS](https://)

---

## Estrutura da Aplicação
A aplicação está organizada em módulos, cada um responsável por diferentes funcionalidades:

- **auth.py**: Gerencia a autenticação de usuários, incluindo registro e login.
- **films.py**: MFornece dados sobre filmes, permitindo consultas e estatísticas.
- **people.py**: Fornece dados sobre personagens.
- **planets.py**: Fornece dados sobre planetas.
- **starships.py**: Fornece dados sobre naves estelares.
- **app.py**: Configuração principal da aplicação, incluindo rotas e integração com JWT.
- **utils.py**: Contém funções utilitárias para busca, filtragem e estatísticas.

---

### Funcionalidades - Endpoints

#### Autenticação
- **/register**: Registro de novos usuários.
- **/login**: Geração de token JWT para autenticação.

#### Filmes
- **/films**: Consulta com opções de filtragem dos filmes.
- **/films/statistics**: Retorna estatísticas sobre filmes.

#### Personagens
- **/people**: Consulta com opções de filtragem dos personagens.
- **/people/statistics**: Retorna estatísticas sobre personagens.

#### Planetas
- **/planets**: Consulta com opções de filtragem dos planetas.
- **/planets/statistics**: Retorna estatísticas sobre planetas.

#### Naves Estelares
- **/starships**: Consulta com opções de filtragem das naves estelares.
- **/starships/statistics**: Retorna estatísticas sobre naves.

---

## Tecnologias Utilizadas
- **Flask**: Framework web minimalista em Python, usado para criar a API de forma rápida e eficiente.
- **Python**: Linguagem escolhida por sua simplicidade e vasto ecossistema de bibliotecas.
- **JWT (JSON Web Tokens)**: Usado para autenticação, garantindo que apenas usuários autenticados possam acessar os endpoints protegidos.
- **AWS (Lambda e API Gateway)**: Hospedagem na nuvem com escalabilidade automática e sem necessidade de gerenciar servidores.
- **Flasgger**: Utilizado para gerar automaticamente a documentação da API com Swagger, facilitando a interação e os testes de endpoints.
---

## Exemplo de Uso

### Registro de Usuário
```bash
POST /register
{
    "username": "novo_usuario",
    "password": "senha123"
}
```

### Login
```bash
POST /login
{
    "username": "marcelo",
    "password": "marcelo1234"
}
```

### Consulta de Filmes com Filtragem de Titulo
```bash
GET /films?title=Star%20Wars
```

### Estatísticas de Personagens
```bash
GET /people/statistics
```

## Considerações Finais
A API foi construída para ser simples, segura e escalável. Utilizei Flask para garantir que a aplicação se adapte a diferentes necessidades. A documentação interativa gerada pelo Flasgger torna a API fácil de usar e explorar, enquanto a autenticação com JWT assegura o controle de acesso.