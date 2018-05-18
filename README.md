# Desafio de Backend com Python/Django da Estante Virtual

Esse repositório contém o [desafio de backend proposto pela Estante Virtual](https://github.com/estantevirtual/vagas/blob/master/desafios/backend.md). A aplicação em questão foi desenvolvida com o Django, e consiste de uma API para gerenciar competições e seus resultados.

## Versões do Python/Django

No desenvolvimento desta aplicação foram utilizadas as últimas versões do Python e do Django: Python 3.6.5 e Django 2.0.5.

## Instalação

### Clone inicial

Para a instalar a aplicação deve-se começar fazendo um clone do seu repositório:

```
git clone https://github.com/elomarns/desafio_backend_python_estante_virtual.git
```

### Criação do ambiente no virtualenv

Dentro do diretório da aplicação, é necessário criar um ambiente no virtualenv, de forma que as dependências da aplicação fiquem contidas dentro desse ambiente. Abaixo está o comando para realizar essa tarefa usando o virtualenvwrapper:

```
mkvirtualenv desafio_backend_python_estante_virtual
```

### Instalação das dependências

É preciso instalar também as dependências da aplicação:

```
pip install django
pip install restframework
```

### Preparação do banco de dados

A aplicação utiliza o SQLite 3 como banco de dados, logo é preciso antes criá-lo, juntamente com as tabelas necessárias. Para tal, é preciso executar a seguinte instrução dentro do diretório da aplicação:

```
python manage.py migrate
```

## Rodando a suíte de testes

Para rodar todos os testes da aplicação deve-se executar o comando abaixo no diretório da aplicação:

```
python manage.py test
```

## Iniciando a aplicação

Por fim, para iniciar a aplicação, basta executar o comando abaixo dentro do seu diretório:

```
python manage.py runserver
```

Feito isso, a aplicação irá rodar na porta 8000.

## API

A API gerencia competições e seus resultados.

### Competições

As competições possuem os seguintes campos:

* **name**: nome da competição (obrigatório)
* **unit**: unidade de medida (obrigatório)
* **finished**: flag que indica se a competição foi finalizada (obrigatório, mas com false como default)
* **results_limit_per_athlete**: limite de resultados por atleta dentro de uma competição (obrigatório, mas com 1 como default)
* **criterion_for_best_result**: critério para selecionar o melhor resultado, sendo *max* e *min* os possíveis valores (obrigatório, mas com *max* como default). Caso o valor seja *min*, um resultado numericamente inferior terá uma melhor colocação sobre resultados maiores, e vice-versa.

#### Cadastro de competições: POST /competitions/

Exemplo:

```
curl -X "POST" -d "name=Cuspe a distância&unit=m" http://localhost:8000/competitions/
```

##### Retorno:

```
{
    "id": 1,
    "ranking": [],
    "winner_result": null,
    "name": "Cuspe a distância",
    "unit": "m",
    "finished": false,
    "results_limit_per_athlete": 1,
    "criterion_for_best_result": "max"
}
```

Criando outras competições:

```
curl -X "POST" -d "name=Street Fighter 5&unit=wins" http://localhost:8000/competitions/
```

```
curl -X "POST" -d "name=Cochilo com Obstáculos&unit=horas" http://localhost:8000/competitions/
```

#### Visualização de competições: GET /competitions/id/

A visualização de uma competição exibe todos os seus dados, o ranking dos resultados (do melhor para o pior), e o resultado vencedor (caso a competição esteja finalizada).

Exemplo com competição recém criada:

```
curl http://localhost:8000/competitions/1/
```

Retorno:

```
{
    "id": 1,
    "ranking": [],
    "winner_result": null,
    "name": "Cuspe a distância",
    "unit": "m",
    "finished": false,
    "results_limit_per_athlete": 1,
    "criterion_for_best_result": "max"
}
```

Exemplo com competição com resultados e finalizada:

```
curl http://localhost:8000/competitions/2/
```

Retorno:

```
{
    "id": 2,
    "ranking": [
        {
            "id": 2,
            "athlete": {
                "id": 2,
                "name": "Daigo Umehara"
            },
            "value": 89891
        },
        {
            "id": 4,
            "athlete": {
                "id": 3,
                "name": "Lindomar, o Subzero Brasileiro"
            },
            "value": 92
        },
        {
            "id": 1,
            "athlete": {
                "id": 1,
                "name": "Elomar Nascimento dos Santos"
            },
            "value": 38
        }
    ],
    "winner_result": {
        "id": 2,
        "athlete": {
            "id": 2,
            "name": "Daigo Umehara"
        },
        "value": 89891
    },
    "name": "Street Fighter 5",
    "unit": "wins",
    "finished": true,
    "results_limit_per_athlete": 1,
    "criterion_for_best_result": "max"
}
```

#### Listagem de competições: GET /competitions/

A listagem de competições exibe os dados de todas as competições existentes no banco de dados.

Exemplo:

```
curl http://localhost:8000/competitions/
```

Retorno:

```
[
    {
        "id": 1,
        "ranking": [],
        "winner_result": null,
        "name": "Cuspe a distância",
        "unit": "m",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    {
        "id": 2,
        "ranking": [],
        "winner_result": null,
        "name": "Street Fighter 5",
        "unit": "wins",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    {
        "id": 3,
        "ranking": [],
        "winner_result": null,
        "name": "Cochilo com Obstáculos",
        "unit": "horas",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    }
]
```

#### Atualização de competições: PATCH/PUT /competitions/id/

Exemplo:

```
curl -X "PATCH" -d "name=Arremesso de saliva a distância" http://localhost:8000/competitions/1/
```

Retorno:

```
{
    "id": 1,
    "ranking": [],
    "winner_result": null,
    "name": "Arremesso de saliva a distância",
    "unit": "m",
    "finished": false,
    "results_limit_per_athlete": 1,
    "criterion_for_best_result": "max"
}
```

#### Finalização de competições: PATCH/PUT /competitions/id/finish/

Exemplo:

```
curl -X "PATCH" http://localhost:8000/competitions/3/finish/
```

Retorno:

```
{
    "id": 3,
    "ranking": [],
    "winner_result": null,
    "name": "Cochilo com Obstáculos",
    "unit": "horas",
    "finished": true,
    "results_limit_per_athlete": 1,
    "criterion_for_best_result": "max"
}
```

#### Remoção de competições: DELETE /competitions/id/

Exemplo:

```
curl -X "DELETE" http://localhost:8000/competitions/3/
```

Retorno:

```
```

É importante notar que a remoção de competições não retorna nenhum conteúdo, uma vez que ela retorna 204 como código de status. Esse código indica que a solicitação foi bem sucedida, e não haverá nenhum retorno.

### Resultados

A API de resultados é bastante flexível, permitindo cadastrar resultados tanto para competições e atletas já existentes, como também cadastrar a competição, o atleta e o resultado numa só requisição.

#### Competição e/ou atleta previamente existentes

Caso a competição e/ou o atleta já estejam cadastrados, basta passar os seguintes parâmetros:

* **competition_id** ou **competition**: id ou nome da competição a qual pertence o resultado (obrigatório)
* **athlete_id** ou **athlete**: id ou nome do atleta a qual pertence o resultado (obrigatório)
* **value**: valor do resultado (obrigatório)

#### Competição e/ou atleta ainda não cadastrados

Se a competição e/ou o atleta ainda não foram inseridos, pode-se passar os parâmetros abaixo para inseri-los juntamente com o resultado

* **competition**: nome da competição a qual pertence o resultado (obrigatório)
* **unit**: unidade de medida da competição a qual pertence o resultado (obrigatório)
* **athlete**: nome do atleta a qual pertence o resultado (obrigatório)
* **value**: valor do resultado (obrigatório)

No entanto, é importante observar que caso a competição seja criada na API de resultados, ela será criada com os valores default:

* finished: false
* results_limit_per_athlete: 1
* criterion_for_best_result: max

#### Cadastro de resultados: POST /results/

Exemplo com competição e atletas existentes:

```
curl -X "POST" -d "competition_id=2&athlete_id=1&value=38" http://localhost:8000/results/
```

Retorno:

```
{
    "id": 1,
    "competition": {
        "id": 2,
        "name": "Street Fighter 5",
        "unit": "wins",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    "athlete": {
        "id": 1,
        "name": "Elomar Nascimento dos Santos"
    },
    "value": 38
}
```

Exemplo com apenas a competição existente:

```
curl -X "POST" -d "competition_id=2&athlete=Daigo Umehara&value=89891" http://localhost:8000/results/
```

Retorno:

```
{
    "id": 2,
    "competition": {
        "id": 2,
        "name": "Street Fighter 5",
        "unit": "wins",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    "athlete": {
        "id": 2,
        "name": "Daigo Umehara"
    },
    "value": 89891
}
```

Exemplo com apenas o atleta existente:

```
curl -X "POST" -d "competition=200m rasos&unit=m&athlete_id=1&value=18.7" http://localhost:8000/results/
```

Retorno:

```
{
    "id": 3,
    "competition": {
        "id": 4,
        "name": "200m rasos",
        "unit": "m",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    "athlete": {
        "id": 1,
        "name": "Elomar Nascimento dos Santos"
    },
    "value": 18.7
}
```

#### Visualização de resultados: GET /results/id/

Exemplo:

```
curl http://localhost:8000/results/1/
```

Retorno:

```
{
    "id": 1,
    "competition": {
        "id": 2,
        "name": "Street Fighter 5",
        "unit": "wins",
        "finished": false,
        "results_limit_per_athlete": 1,
        "criterion_for_best_result": "max"
    },
    "athlete": {
        "id": 1,
        "name": "Elomar Nascimento dos Santos"
    },
    "value": 38
}
```

## Possibilidades de melhoria

Buscando manter a aplicação mais simples, e dentro do prazo, eu evitei fazer certas coisas que, embora não foram solicitadas, poderiam melhorar a aplicação. Abaixo eu listo algumas delas:

* Colocar a API num namespace, e versioná-la, de forma que suas URLs sejam precedidas por /api/v1/
* Aumentar a cobertura de testes
* Permitir que os usuários da API passem parêmetros adicionais, como limite, ordenação dos resultados, e até filtros

## Considerações sobre o idioma do código

Como não havia nenhuma especificação quanto ao idioma no qual a aplicação deveria ser codificada, e uma vez que eu também não sei a convenção adotada pela Estante Virtual, eu optei por desenvolvê-la usando o padrão ao qual eu estou acostumado: código em inglês. No entanto, é possível modificá-la facilmente para que o código fique em português.
